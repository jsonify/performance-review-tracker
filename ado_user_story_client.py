import requests
import json
import os
import base64
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Union
from pathlib import Path
import re
import hashlib
import argparse


class ADOUserStoryClient:
    """
    Enhanced Azure DevOps client for retrieving User Story information via REST API.
    
    Features:
    - Robust error handling with exponential backoff
    - Data transformation for performance review format
    - Field mapping and filtering capabilities
    - Request caching for performance
    - Comprehensive logging and validation
    """

    # Field mapping from Azure DevOps to Performance Review format
    DEFAULT_FIELD_MAPPING = {
        'System.Title': 'Title',
        'Microsoft.VSTS.Common.ClosedDate': 'Date', 
        'System.Description': 'Description',
        'Microsoft.VSTS.Common.AcceptanceCriteria': 'Acceptance Criteria',
        'System.Id': 'Work Item ID',
        'System.State': 'Status'
    }
    
    # Default fields to retrieve from Azure DevOps
    DEFAULT_FIELDS = [
        "System.Id",
        "System.Title",
        "Microsoft.VSTS.Common.ClosedDate",
        "System.Description", 
        "Microsoft.VSTS.Common.AcceptanceCriteria",
        "System.State",
        "System.AssignedTo",
        "Microsoft.VSTS.Common.Priority",
        "Microsoft.VSTS.Scheduling.StoryPoints",
        "System.Tags"
    ]
    
    # Rate limiting configuration
    MAX_RETRIES = 3
    BASE_DELAY = 1.0  # Base delay for exponential backoff
    MAX_DELAY = 60.0  # Maximum delay between retries
    REQUESTS_PER_MINUTE = 300  # Azure DevOps API rate limit
    
    def __init__(self, 
                 organization: str, 
                 project: str, 
                 personal_access_token: str,
                 enable_caching: bool = True,
                 cache_dir: str = ".ado_cache"):
        """
        Initialize the ADO client

        Args:
            organization: Azure DevOps organization name
            project: Project name
            personal_access_token: Personal Access Token for authentication
        """
        # Basic configuration
        self.organization = organization
        self.project = project
        self.base_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit"
        
        # Authentication setup
        if not personal_access_token or personal_access_token.strip() == "":
            raise ValueError("Personal Access Token cannot be empty")
        
        token_bytes = f":{personal_access_token}".encode('ascii')
        token_b64 = base64.b64encode(token_bytes).decode('ascii')
        self.headers = {
            'Authorization': f'Basic {token_b64}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'Performance-Review-Tracker/1.0'
        }
        
        # Caching configuration
        self.enable_caching = enable_caching
        self.cache_dir = Path(cache_dir)
        if enable_caching:
            self.cache_dir.mkdir(exist_ok=True)
        
        # Rate limiting tracking
        self._request_timestamps = []
        self._last_request_time = 0
        
        # Session for connection pooling
        self._session = requests.Session()
        self._session.headers.update(self.headers)
        
        print(f"Initialized enhanced ADO client:")
        print(f"  Organization: {organization}")
        print(f"  Project: {project}")
        print(f"  Base URL: {self.base_url}")
        print(f"  Caching: {'Enabled' if enable_caching else 'Disabled'}")
        print(f"  Token length: {len(personal_access_token)} characters")

    def _make_request_with_retry(self, url: str, method: str = "GET", 
                                json_data: Optional[Dict] = None,
                                params: Optional[Dict] = None) -> requests.Response:
        """
        Make HTTP request with exponential backoff retry logic.
        
        Args:
            url: Request URL
            method: HTTP method (GET, POST, etc.)
            json_data: JSON data for POST requests
            params: Query parameters
            
        Returns:
            Response object
            
        Raises:
            requests.RequestException: If all retry attempts fail
        """
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                # Rate limiting - ensure we don't exceed API limits
                self._enforce_rate_limit()
                
                # Make the request
                if method.upper() == "GET":
                    response = self._session.get(url, params=params, timeout=30)
                elif method.upper() == "POST":
                    response = self._session.post(url, json=json_data, params=params, timeout=30)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Handle rate limiting response
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', '60'))
                    print(f\"Rate limited. Waiting {retry_after} seconds before retry...\")\n                    time.sleep(retry_after)\n                    continue
                
                # Check for successful response or client errors that shouldn't be retried
                if response.status_code < 500:
                    return response
                
                # Server error - retry with backoff\n                if attempt < self.MAX_RETRIES:\n                    delay = min(self.BASE_DELAY * (2 ** attempt), self.MAX_DELAY)\n                    print(f\"Server error {response.status_code}, retrying in {delay:.1f}s (attempt {attempt + 1}/{self.MAX_RETRIES})\")\n                    time.sleep(delay)\n                    continue\n                else:\n                    response.raise_for_status()\n                    \n            except requests.exceptions.Timeout:\n                if attempt < self.MAX_RETRIES:\n                    delay = min(self.BASE_DELAY * (2 ** attempt), self.MAX_DELAY)\n                    print(f\"Request timeout, retrying in {delay:.1f}s (attempt {attempt + 1}/{self.MAX_RETRIES})\")\n                    time.sleep(delay)\n                    continue\n                else:\n                    raise\n                    \n            except requests.exceptions.ConnectionError:\n                if attempt < self.MAX_RETRIES:\n                    delay = min(self.BASE_DELAY * (2 ** attempt), self.MAX_DELAY)\n                    print(f\"Connection error, retrying in {delay:.1f}s (attempt {attempt + 1}/{self.MAX_RETRIES})\")\n                    time.sleep(delay)\n                    continue\n                else:\n                    raise\n        \n        raise requests.RequestException(\"All retry attempts exhausted\")\n    \n    def _enforce_rate_limit(self) -> None:\n        \"\"\"\n        Enforce rate limiting to stay within Azure DevOps API limits.\n        \"\"\"\n        current_time = time.time()\n        \n        # Clean old timestamps (older than 1 minute)\n        cutoff_time = current_time - 60\n        self._request_timestamps = [ts for ts in self._request_timestamps if ts > cutoff_time]\n        \n        # Check if we're approaching the rate limit\n        if len(self._request_timestamps) >= self.REQUESTS_PER_MINUTE - 10:  # Leave some buffer\n            sleep_time = 60 - (current_time - self._request_timestamps[0])\n            if sleep_time > 0:\n                print(f\"Rate limit protection: sleeping for {sleep_time:.1f}s\")\n                time.sleep(sleep_time)\n                current_time = time.time()\n        \n        # Record this request timestamp\n        self._request_timestamps.append(current_time)\n        self._last_request_time = current_time\n    \n    def _get_cache_key(self, request_type: str, **kwargs) -> str:\n        \"\"\"\n        Generate cache key for request caching.\n        \n        Args:\n            request_type: Type of request (e.g., 'work_items', 'user_id')\n            **kwargs: Request parameters\n            \n        Returns:\n            MD5 hash as cache key\n        \"\"\"\n        key_data = f\"{self.organization}:{self.project}:{request_type}:{sorted(kwargs.items())}\"\n        return hashlib.md5(key_data.encode()).hexdigest()\n    \n    def _get_cached_response(self, cache_key: str, max_age_minutes: int = 60) -> Optional[Dict]:\n        \"\"\"\n        Retrieve cached response if it exists and is not expired.\n        \n        Args:\n            cache_key: Cache key to look up\n            max_age_minutes: Maximum age of cached response in minutes\n            \n        Returns:\n            Cached response data or None if not found/expired\n        \"\"\"\n        if not self.enable_caching:\n            return None\n            \n        cache_file = self.cache_dir / f\"{cache_key}.json\"\n        if not cache_file.exists():\n            return None\n        \n        try:\n            # Check file age\n            file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)\n            if file_age > timedelta(minutes=max_age_minutes):\n                cache_file.unlink()  # Remove expired cache\n                return None\n            \n            # Load cached data\n            with open(cache_file, 'r', encoding='utf-8') as f:\n                return json.load(f)\n                \n        except Exception as e:\n            print(f\"Error reading cache file {cache_file}: {e}\")\n            return None\n    \n    def _save_cached_response(self, cache_key: str, data: Dict) -> None:\n        \"\"\"\n        Save response data to cache.\n        \n        Args:\n            cache_key: Cache key to save under\n            data: Response data to cache\n        \"\"\"\n        if not self.enable_caching:\n            return\n            \n        try:\n            cache_file = self.cache_dir / f\"{cache_key}.json\"\n            with open(cache_file, 'w', encoding='utf-8') as f:\n                json.dump(data, f, indent=2, ensure_ascii=False, default=str)\n        except Exception as e:\n            print(f\"Error saving to cache: {e}\")\n    \n    def clear_cache(self) -> None:\n        \"\"\"\n        Clear all cached responses.\n        \"\"\"\n        if not self.enable_caching:\n            return\n            \n        try:\n            for cache_file in self.cache_dir.glob(\"*.json\"):\n                cache_file.unlink()\n            print(\"Cache cleared successfully\")\n        except Exception as e:\n            print(f\"Error clearing cache: {e}\")\n\n    def test_connection(self) -> bool:"}
        """
        Test the connection and authentication with Azure DevOps

        Returns:
            True if connection is successful, False otherwise
        """
        # Try to get project information first
        test_url = f"https://dev.azure.com/{self.organization}/_apis/projects/{self.project}"
        params = {'api-version': '7.1'}

        print(f"Testing connection to: {test_url}")

        try:
            response = self._make_request_with_retry(test_url, \"GET\", params=params)
            print(f"Test response status: {response.status_code}")
            print(f"Test response headers: {dict(response.headers)}")

            if response.status_code == 200:
                print("✓ Connection and authentication successful!")
                project_data = response.json()
                print(f"✓ Project name: {project_data.get('name')}")
                print(f"✓ Project ID: {project_data.get('id')}")
                return True
            elif response.status_code == 401:
                print("✗ Authentication failed - check your Personal Access Token")
                print("Make sure your PAT has 'Work Items (Read)' permission")
            elif response.status_code == 404:
                print("✗ Project not found - check organization and project names")
            else:
                print(f"✗ Unexpected response: {response.status_code} - {response.text}")

            return False

        except requests.exceptions.RequestException as e:
            print(f"✗ Connection test failed: {e}")
            return False

    def get_current_user_id(self) -> Optional[str]:
        """
        Get the current user's ID based on the authentication token

        Returns:
            Current user ID or None if not found
        """
        url = f"https://vssps.dev.azure.com/{self.organization}/_apis/profile/profiles/me"
        params = {'api-version': '7.1'}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                user_id = data.get('id')
                print(f"Current user ID: {user_id}")
                return user_id
            else:
                print(f"Could not get current user ID: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error getting current user ID: {e}")
            return None

    def get_available_work_item_types(self) -> List[str]:
        """
        Get all available work item types in the project

        Returns:
            List of work item type names
        """
        url = f"{self.base_url}/workitemtypes"
        params = {'api-version': '7.1'}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            types = [item['name'] for item in data.get('value', [])]
            return sorted(types)

        except Exception as e:
            print(f"Error getting work item types: {e}")
            return []

    def query_work_items(self, wiql_query: str) -> List[int]:
        """
        Execute a WIQL query to get work item IDs

        Args:
            wiql_query: WIQL query string

        Returns:
            List of work item IDs
        """
        url = f"https://dev.azure.com/{self.organization}/{self.project}/_apis/wit/wiql"

        payload = {
            "query": wiql_query
        }

        params = {
            'api-version': '7.1'
        }

        print(f"Executing WIQL query...")
        print(f"Query: {wiql_query}")

        try:
            response = requests.post(url, headers=self.headers, json=payload, params=params)

            print(f"Query response status: {response.status_code}")

            if response.status_code != 200:
                print(f"Query failed: {response.text}")
                response.raise_for_status()

            data = response.json()
            work_items = data.get('workItems', [])
            work_item_ids = [item['id'] for item in work_items]

            print(f"Query returned {len(work_item_ids)} work items")
            return work_item_ids

        except requests.exceptions.RequestException as e:
            print(f"Error executing WIQL query: {e}")
            raise

    def get_work_items_with_fields(self, work_item_ids: List[int],
                                  fields: List[str]) -> List[Dict[str, Any]]:
        """
        Get multiple work items with only specific fields

        Args:
            work_item_ids: List of work item IDs
            fields: List of field names to retrieve

        Returns:
            List of work items with only requested fields
        """
        if not work_item_ids:
            return []

        # ADO batch API limit is 200 items per request
        batch_size = 200
        all_results = []

        for i in range(0, len(work_item_ids), batch_size):
            batch_ids = work_item_ids[i:i + batch_size]
            batch_results = self._get_work_items_batch_with_fields(batch_ids, fields)
            all_results.extend(batch_results)

        return all_results

    def _get_work_items_batch_with_fields(self, work_item_ids: List[int],
                                         fields: List[str]) -> List[Dict[str, Any]]:
        """Get a batch of work items with specific fields only"""
        if not work_item_ids:
            return []

        url = f"{self.base_url}/workitems"
        params = {
            'ids': ','.join(map(str, work_item_ids)),
            'fields': ','.join(fields),
            'api-version': '7.1'
        }

        print(f"Fetching {len(work_item_ids)} work items with fields: {', '.join(fields)}")

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get('value', []):
                # Create simplified structure with only requested fields
                simplified_item = {
                    'id': item.get('id'),
                    'fields': {}
                }

                # Extract only the requested fields
                item_fields = item.get('fields', {})
                for field in fields:
                    if field in item_fields:
                        simplified_item['fields'][field] = item_fields[field]

                # Store raw data for reference
                simplified_item['raw_data'] = {
                    'fields': item_fields
                }

                results.append(simplified_item)

            return results

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving work items batch: {e}")
            raise

    def get_work_items_by_criteria(self, assigned_to_id: str, state: str = "Closed",
                                  work_item_type: str = "User Story",
                                  fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Get work items matching specific criteria with only requested fields

        Args:
            assigned_to_id: The user ID to filter by (from System.AssignedTo.id)
            state: Work item state (e.g., "Closed", "Active", "Resolved")
            work_item_type: Type of work item (e.g., "User Story", "Bug", "Task")
            fields: List of specific fields to retrieve

        Returns:
            List of work items with only the requested fields
        """
        # Default fields if none specified
        if fields is None:
            fields = [
                "System.Id",
                "System.Title",
                "Microsoft.VSTS.Common.ClosedDate",
                "System.Description",
                "Microsoft.VSTS.Common.AcceptanceCriteria"
            ]

        # Try different WIQL query formats for the user
        query_variations = [
            # Format 1: Using user ID directly
            f"""
            SELECT [System.Id]
            FROM workitems
            WHERE [System.TeamProject] = '{self.project}'
            AND [System.WorkItemType] = '{work_item_type}'
            AND [System.State] = '{state}'
            AND [System.AssignedTo] = '{assigned_to_id}'
            ORDER BY [Microsoft.VSTS.Common.ClosedDate] DESC
            """,

            # Format 2: Using @Me if it's the current user
            f"""
            SELECT [System.Id]
            FROM workitems
            WHERE [System.TeamProject] = '{self.project}'
            AND [System.WorkItemType] = '{work_item_type}'
            AND [System.State] = '{state}'
            AND [System.AssignedTo] = @Me
            ORDER BY [Microsoft.VSTS.Common.ClosedDate] DESC
            """,

            # Format 3: Just get all work items of this type and state for debugging
            f"""
            SELECT [System.Id]
            FROM workitems
            WHERE [System.TeamProject] = '{self.project}'
            AND [System.WorkItemType] = '{work_item_type}'
            AND [System.State] = '{state}'
            ORDER BY [Microsoft.VSTS.Common.ClosedDate] DESC
            """
        ]

        work_item_ids = []
        successful_query = None

        for i, query in enumerate(query_variations):
            try:
                print(f"\nTrying query variation {i + 1}...")
                temp_ids = self.query_work_items(query)
                if temp_ids:
                    work_item_ids = temp_ids
                    successful_query = i + 1
                    print(f"✓ Query variation {i + 1} found {len(temp_ids)} work items")
                    break
                else:
                    print(f"✗ Query variation {i + 1} returned 0 results")
            except Exception as e:
                print(f"✗ Query variation {i + 1} failed: {e}")
                continue

        if not work_item_ids:
            print("\nNo work items found with any query variation.")
            print("This could mean:")
            print("1. No work items match the exact criteria")
            print("2. The user ID format is different")
            print("3. The work items are in a different state")
            print("4. The work item type name is different")
            return []

        print(f"\nUsing successful query variation {successful_query}")

        # Get work items with specific fields
        work_items = self.get_work_items_with_fields(work_item_ids, fields)

        # If we used the broad query (variation 3), filter by assigned user post-query
        if successful_query == 3 and assigned_to_id:
            print(f"Filtering {len(work_items)} items by assigned user post-query...")
            filtered_items = []
            for item in work_items:
                assigned_to = item.get('raw_data', {}).get('fields', {}).get('System.AssignedTo')
                if assigned_to and assigned_to.get('id') == assigned_to_id:
                    filtered_items.append(item)

            print(f"After filtering by user ID: {len(filtered_items)} items remain")
            work_items = filtered_items

        return work_items

    def diagnose_work_items(self, work_item_type: str = "User Story", limit: int = 10) -> None:
        """
        Diagnose what work items exist in the project to help troubleshoot filtering issues

        Args:
            work_item_type: Type of work item to examine
            limit: Maximum number of items to examine
        """
        print(f"\n" + "="*60)
        print(f"DIAGNOSING {work_item_type.upper()} WORK ITEMS")
        print("="*60)

        # Get a sample of work items of the specified type
        diagnostic_query = f"""
        SELECT [System.Id]
        FROM workitems
        WHERE [System.TeamProject] = '{self.project}'
        AND [System.WorkItemType] = '{work_item_type}'
        ORDER BY [System.ChangedDate] DESC
        """

        try:
            work_item_ids = self.query_work_items(diagnostic_query)

            if not work_item_ids:
                print(f"❌ No {work_item_type} work items found in project '{self.project}'")
                print("\nPossible issues:")
                print("1. Work item type name might be different (try 'Product Backlog Item', 'Feature', etc.)")
                print("2. You might not have permission to view work items")
                print("3. The project might not have any work items of this type")
                return

            print(f"✓ Found {len(work_item_ids)} {work_item_type} work items in total")

            # Get details for a sample of work items
            sample_ids = work_item_ids[:limit]
            print(f"\nExamining first {len(sample_ids)} work items...")

            # Get work items with diagnostic fields
            diagnostic_fields = [
                "System.Id", "System.Title", "System.State", "System.AssignedTo",
                "System.CreatedDate", "Microsoft.VSTS.Common.ClosedDate"
            ]

            sample_items = self.get_work_items_with_fields(sample_ids, diagnostic_fields)

            # Analyze the sample
            states = {}
            assigned_users = {}
            closed_count = 0

            print(f"\n{'ID':<8} {'State':<12} {'Assigned To':<30} {'Title':<50}")
            print("-" * 100)

            for item in sample_items:
                fields = item.get('raw_data', {}).get('fields', {})

                item_id = fields.get('System.Id', 'N/A')
                state = fields.get('System.State', 'N/A')
                title = fields.get('System.Title', 'No Title')[:47] + "..." if len(fields.get('System.Title', '')) > 50 else fields.get('System.Title', 'No Title')

                assigned_to = fields.get('System.AssignedTo')
                if assigned_to:
                    assigned_name = assigned_to.get('displayName', 'Unknown')
                    assigned_id = assigned_to.get('id', 'Unknown')
                    assigned_users[assigned_id] = assigned_name
                else:
                    assigned_name = 'Unassigned'
                    assigned_id = 'None'

                # Count states
                states[state] = states.get(state, 0) + 1

                # Count closed items
                if state.lower() == 'closed':
                    closed_count += 1

                print(f"{item_id:<8} {state:<12} {assigned_name:<30} {title:<50}")

            # Summary
            print(f"\n" + "="*60)
            print("SUMMARY:")
            print(f"✓ Total {work_item_type} items examined: {len(sample_items)}")
            print(f"✓ Items in 'Closed' state: {closed_count}")

            print(f"\nStates found:")
            for state, count in sorted(states.items()):
                print(f"  • {state}: {count} items")

            print(f"\nUnique assigned users found:")
            for user_id, display_name in list(assigned_users.items())[:10]:  # Show first 10 users
                print(f"  • {display_name} (ID: {user_id})")

            if len(assigned_users) > 10:
                print(f"  ... and {len(assigned_users) - 10} more users")

            print(f"\nYour user ID: 99ab0929-d361-441b-b573-83589a0caff0")
            if "99ab0929-d361-441b-b573-83589a0caff0" in assigned_users:
                print("✓ Your user ID was found in the assigned users!")
            else:
                print("❌ Your user ID was NOT found in the assigned users")
                print("This might explain why no results were returned.")

        except Exception as e:
            print(f"❌ Error during diagnosis: {e}")

    def save_work_items_to_file(self, work_items: List[Dict[str, Any]],
                               output_dir: str = "ado_data",
                               filename_prefix: str = "filtered_work_items") -> str:
        """
        Save multiple work items to a JSON file

        Args:
            work_items: List of work item data dictionaries
            output_dir: Directory to save the file
            filename_prefix: Prefix for the filename

        Returns:
            Path to the saved file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)

        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(work_items, f, indent=2, ensure_ascii=False, default=str)

        print(f"Saved {len(work_items)} work items to: {filepath}")
        return filepath


def load_config(config_file: str = "config.json") -> Dict[str, str]:
    """
    Load configuration from JSON file

    Args:
        config_file: Path to the configuration file

    Returns:
        Dictionary containing configuration values
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)

        print(f"Loaded configuration from {config_file}")
        print(f"  Organization: {config.get('organization', 'Not specified')}")
        print(f"  Project: {config.get('project', 'Not specified')}")
        print(f"  Output Directory: {config.get('output_directory', 'Not specified')}")
        print(f"  Token: {'*' * (len(config.get('personal_access_token', '')) - 4) + config.get('personal_access_token', '')[-4:] if config.get('personal_access_token') else 'Not specified'}")

        return config

    except FileNotFoundError:
        print(f"Configuration file '{config_file}' not found.")
        print("Please create a config.json file with your Azure DevOps settings.")
        raise
    except json.JSONDecodeError as e:
        print(f"Error parsing configuration file '{config_file}': {e}")
        raise
    except Exception as e:
        print(f"Error loading configuration: {e}")
        raise


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='Retrieve Azure DevOps User Story information')

    # Configuration options
    parser.add_argument('--config', default='config.json', help='Path to configuration JSON file')
    parser.add_argument('--organization', help='Azure DevOps organization (overrides config file)')
    parser.add_argument('--project', help='Project name (overrides config file)')
    parser.add_argument('--token', help='Personal Access Token (overrides config file)')

    # Work item options
    parser.add_argument('--work-item-id', type=int, help='Work item ID to retrieve')
    parser.add_argument('--work-item-ids', nargs='+', type=int, help='Multiple work item IDs to retrieve')

    # Filtering options
    parser.add_argument('--filter-assigned-to-me', action='store_true',
                       help='Get all work items assigned to current user')
    parser.add_argument('--filter-user-id', help='Filter by specific user ID')
    parser.add_argument('--filter-state', default='Closed',
                       help='Filter by work item state (default: Closed)')
    parser.add_argument('--filter-type', default='User Story',
                       help='Filter by work item type (default: User Story)')
    parser.add_argument('--fields', nargs='+',
                       default=['System.Title', 'Microsoft.VSTS.Common.ClosedDate',
                               'System.Description', 'Microsoft.VSTS.Common.AcceptanceCriteria'],
                       help='Specific fields to retrieve')

    # Output options
    parser.add_argument('--output-dir', help='Output directory for saved files (overrides config file)')
    parser.add_argument('--raw', action='store_true', help='Save raw JSON instead of formatted data')
    parser.add_argument('--test-connection', action='store_true', help='Test connection only')
    parser.add_argument('--get-my-user-id', action='store_true', help='Get current user ID')
    parser.add_argument('--diagnose', action='store_true', help='Diagnose work items in project')
    parser.add_argument('--list-work-item-types', action='store_true', help='List available work item types')
    parser.add_argument('--debug-query', action='store_true', help='Use alternative query methods for debugging')

    args = parser.parse_args()

    try:
        # Load configuration from file
        config = load_config(args.config)

        # Override config with command line arguments if provided
        organization = args.organization or config.get('organization')
        project = args.project or config.get('project')
        token = args.token or config.get('personal_access_token')
        output_dir = args.output_dir or config.get('output_directory', 'ado_data')

        # Validate required parameters
        if not organization:
            print("Error: Organization is required. Set it in config.json or use --organization")
            return 1
        if not project:
            print("Error: Project is required. Set it in config.json or use --project")
            return 1
        if not token:
            print("Error: Personal Access Token is required. Set it in config.json or use --token")
            return 1

        # Initialize client
        client = ADOUserStoryClient(organization, project, token)

        # Test connection first
        print("\n" + "="*50)
        print("Testing connection...")
        if not client.test_connection():
            print("Connection test failed. Please check your credentials and try again.")
            return 1

        if args.test_connection:
            print("Connection test completed successfully!")
            return 0

        if args.get_my_user_id:
            print("\n" + "="*50)
            print("Getting current user ID...")
            user_id = client.get_current_user_id()
            if user_id:
                print(f"Your user ID is: {user_id}")
                print("You can use this ID with --filter-user-id parameter")
            return 0

        if args.list_work_item_types:
            print("\n" + "="*50)
            print("Available work item types in this project:")
            types = client.get_available_work_item_types()
            for work_type in types:
                print(f"  • {work_type}")
            return 0

        if args.diagnose:
            print("\n" + "="*50)
            print("Running diagnostic...")
            client.diagnose_work_items(args.filter_type)
            return 0

        if args.filter_assigned_to_me or args.filter_user_id:
            # Filter work items by criteria
            print(f"\n" + "="*50)
            print("Filtering work items...")

            if args.filter_assigned_to_me:
                # Get current user ID
                user_id = client.get_current_user_id()
                if not user_id:
                    print("Could not get current user ID. Try using --filter-user-id instead.")
                    return 1
            else:
                user_id = args.filter_user_id

            print(f"Filtering criteria:")
            print(f"  User ID: {user_id}")
            print(f"  State: {args.filter_state}")
            print(f"  Type: {args.filter_type}")
            print(f"  Fields: {', '.join(args.fields)}")

            work_items = client.get_work_items_by_criteria(
                assigned_to_id=user_id,
                state=args.filter_state,
                work_item_type=args.filter_type,
                fields=args.fields
            )

            if work_items:
                filepath = client.save_work_items_to_file(
                    work_items,
                    output_dir,
                    f"{args.filter_type.lower().replace(' ', '_')}_{args.filter_state.lower()}"
                )
                print(f"Successfully saved {len(work_items)} work items to {filepath}")

                # Display summary
                print(f"\nSummary of retrieved work items:")
                for item in work_items[:5]:  # Show first 5 items
                    title = item['fields'].get('System.Title', 'No Title')[:60]
                    closed_date = item['fields'].get('Microsoft.VSTS.Common.ClosedDate', 'No Date')
                    if closed_date != 'No Date' and 'T' in closed_date:
                        closed_date = closed_date.split('T')[0]  # Just the date part
                    print(f"  ID {item['id']}: {title} (Closed: {closed_date})")

                if len(work_items) > 5:
                    print(f"  ... and {len(work_items) - 5} more items")
            else:
                print("No work items found matching the criteria")

        else:
            print("Please specify one of the following options:")
            print("  --work-item-id <ID>         : Get a single work item")
            print("  --work-item-ids <ID1 ID2>   : Get multiple work items by ID")
            print("  --filter-assigned-to-me     : Get work items assigned to you")
            print("  --filter-user-id <USER_ID>  : Get work items assigned to specific user")
            print("  --test-connection           : Test connection only")
            print("  --get-my-user-id           : Get your user ID")
            print("  --list-work-item-types      : List available work item types")
            print("  --diagnose                  : Diagnose work items in project")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

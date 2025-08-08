# API Specification

This is the API specification for the spec detailed in @.agent-os/specs/2025-08-07-ado-integration/spec.md

> Created: 2025-08-07
> Version: 1.0.0

## Azure DevOps API Integration

### Authentication Endpoint

**Personal Access Token Validation**
- **Method**: GET
- **URL**: `https://dev.azure.com/{organization}/_apis/projects/{project}?api-version=7.1`
- **Purpose**: Validate PAT and organization/project access
- **Headers**: `Authorization: Basic {base64(":token")}`
- **Response**: Project details or authentication error

### User Identity Endpoint

**GET /profile/profiles/me**
- **Method**: GET  
- **URL**: `https://vssps.dev.azure.com/{organization}/_apis/profile/profiles/me?api-version=7.1`
- **Purpose**: Get current user ID for filtering work items
- **Response**: User profile with unique ID
- **Error Handling**: Fallback to manual user ID configuration

### Work Item Query Endpoint

**POST /wit/wiql**
- **Method**: POST
- **URL**: `https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.1`
- **Purpose**: Execute WIQL queries to find User Stories
- **Parameters**: 
  - `query`: WIQL query string
- **Query Examples**:
  ```sql
  SELECT [System.Id] FROM workitems 
  WHERE [System.TeamProject] = 'ProjectName'
  AND [System.WorkItemType] = 'User Story'
  AND [System.State] = 'Closed'
  AND [System.AssignedTo] = @Me
  ORDER BY [Microsoft.VSTS.Common.ClosedDate] DESC
  ```
- **Response**: Array of work item IDs

### Work Items Batch Retrieval

**GET /wit/workitems**
- **Method**: GET
- **URL**: `https://dev.azure.com/{organization}/{project}/_apis/wit/workitems?api-version=7.1`
- **Purpose**: Retrieve detailed work item information
- **Parameters**:
  - `ids`: Comma-separated list of work item IDs (max 200)
  - `fields`: Comma-separated list of field names
- **Response**: Detailed work item data with requested fields
- **Batch Processing**: Handle >200 items with multiple requests

## Internal API Enhancements

### Configuration Management API

**load_config(config_file: str) -> Dict[str, Any]**
- **Purpose**: Load and validate configuration from JSON file
- **Parameters**: Path to config.json file
- **Returns**: Validated configuration dictionary
- **Errors**: FileNotFoundError, JSONDecodeError, ValidationError

**validate_config(config: Dict[str, Any]) -> bool**
- **Purpose**: Validate configuration structure and required fields
- **Parameters**: Configuration dictionary
- **Returns**: Boolean success status
- **Side Effects**: Raises ConfigurationError for invalid configs

### Data Transformation API

**transform_ado_to_performance_data(work_items: List[Dict]) -> pd.DataFrame**
- **Purpose**: Transform Azure DevOps work items to performance review format
- **Parameters**: List of work item dictionaries from ADO API
- **Returns**: pandas DataFrame in expected performance review structure
- **Field Mappings**: Apply field mapping dictionary and generate derived fields

**calculate_impact_rating(work_item: Dict[str, Any]) -> str**
- **Purpose**: Analyze work item content to determine impact level
- **Parameters**: Single work item dictionary
- **Returns**: Impact rating ("High", "Medium", "Low")
- **Logic**: Keyword analysis of title, description, and acceptance criteria

### LLM Integration API

**analyze_with_llm(data: pd.DataFrame, provider: str, review_type: str) -> str**
- **Purpose**: Send processed data to selected LLM provider for analysis
- **Parameters**: 
  - `data`: Processed performance data
  - `provider`: LLM provider ("openai", "anthropic", "roo_code")
  - `review_type`: Analysis type ("competency", "annual")
- **Returns**: Formatted analysis text
- **Errors**: APIError, RateLimitError, AuthenticationError

## Enhanced ADOUserStoryClient Methods

### Connection and Authentication

**test_connection_comprehensive() -> Dict[str, Any]**
- **Purpose**: Comprehensive connection testing with detailed diagnostics
- **Returns**: Connection status, user info, project details, permissions
- **Error Recovery**: Specific guidance for common authentication issues

### Data Retrieval Enhancements

**get_user_stories_for_review(date_range: Tuple[str, str], **kwargs) -> List[Dict[str, Any]]**
- **Purpose**: Get User Stories optimized for performance review data
- **Parameters**: 
  - `date_range`: Start and end dates for filtering
  - `kwargs`: Additional filtering options (state, work_item_type)
- **Returns**: List of work items with performance-relevant fields
- **Optimization**: Single API call with optimal field selection

**cache_query_results(query_key: str, results: List[Dict], ttl_hours: int = 24) -> None**
- **Purpose**: Cache API results to reduce redundant calls
- **Parameters**: Cache key, results data, time-to-live
- **Storage**: Local JSON file with timestamp validation

### Error Recovery

**retry_with_backoff(func: Callable, max_retries: int = 3) -> Any**
- **Purpose**: Retry API calls with exponential backoff
- **Parameters**: Function to retry, maximum retry attempts
- **Returns**: Function result or raises final exception
- **Backoff Strategy**: 1s, 2s, 4s delays with jitter

## Main Pipeline Integration

### Enhanced main.py Functions

**load_data_source(source: str, config: Dict[str, Any], **kwargs) -> pd.DataFrame**
- **Purpose**: Unified data loading supporting multiple sources
- **Parameters**:
  - `source`: Data source type ("csv", "ado", "hybrid")
  - `config`: Configuration dictionary
  - `kwargs`: Source-specific parameters
- **Returns**: Standardized pandas DataFrame
- **Error Handling**: Graceful fallback between sources

**generate_review_with_source(source: str, config: Dict[str, Any], **kwargs) -> str**
- **Purpose**: End-to-end review generation with configurable data source
- **Parameters**: Source type, configuration, review parameters  
- **Returns**: Path to generated report
- **Integration**: Seamless integration with existing template system

## Error Handling Patterns

### API Error Responses

**Azure DevOps API Errors:**
- `401 Unauthorized`: Invalid or expired PAT token
- `403 Forbidden`: Insufficient permissions for operation
- `404 Not Found`: Organization, project, or work item not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Azure DevOps service issue

**Error Recovery Actions:**
- Authentication errors → Prompt for token refresh
- Rate limiting → Exponential backoff retry
- Network errors → Cache fallback if available
- Service errors → Automatic fallback to CSV processing

### Configuration Validation Errors

**Common Configuration Issues:**
- Missing required fields (organization, project, PAT)
- Invalid organization or project names
- Expired or insufficient PAT permissions
- Network connectivity issues

**User Guidance:**
- Step-by-step PAT creation instructions
- Organization and project name validation
- Permission requirements documentation
- Connectivity troubleshooting guide
#!/usr/bin/env python3
"""
Configuration validation module for Performance Review Tracking System.

This module provides utilities for loading, validating, and testing configuration
settings including Azure DevOps authentication and LLM integration settings.
"""

import json
import os
import sys
from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path


class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""
    pass


class ConfigValidator:
    """
    Configuration validator for the Performance Review Tracking System.
    Handles loading, validation, and testing of configuration settings.
    """
    
    # Required configuration structure
    REQUIRED_SCHEMA = {
        "azure_devops": {
            "required_fields": ["organization", "project", "personal_access_token"],
            "optional_fields": ["user_id", "work_item_type", "states", "fields"]
        },
        "llm_integration": {
            "required_fields": ["provider"],
            "optional_fields": ["api_key", "model", "fallback_to_roo", "options"]
        },
        "processing": {
            "required_fields": [],
            "optional_fields": ["output_directory", "backup_csv", "date_range_months", "default_source"]
        }
    }
    
    # Optional sections - these don't require validation but will get defaults if missing
    OPTIONAL_SECTIONS = ["processing"]
    
    # Valid values for specific fields
    VALID_VALUES = {
        "llm_integration.provider": ["openai", "anthropic", "google", "roo_code"],
        "processing.default_source": ["csv", "ado", "hybrid"]
    }
    
    # Default values for missing optional fields
    DEFAULT_VALUES = {
        "azure_devops": {
            "work_item_type": "User Story",
            "states": ["Closed", "Resolved"],
            "fields": [
                "System.Id",
                "System.Title", 
                "Microsoft.VSTS.Common.ClosedDate",
                "System.Description",
                "Microsoft.VSTS.Common.AcceptanceCriteria"
            ]
        },
        "llm_integration": {
            "fallback_to_roo": True,
            "options": {
                "temperature": 0.7,
                "max_tokens": 4000
            }
        },
        "processing": {
            "output_directory": "data",
            "backup_csv": True,
            "date_range_months": 12,
            "default_source": "csv"
        }
    }

    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the configuration validator.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config_data = {}
        
    def load_config(self, create_if_missing: bool = False) -> Dict:
        """
        Load configuration from file with validation.
        
        Args:
            create_if_missing: If True, create example config if file doesn't exist
            
        Returns:
            Dictionary containing validated configuration
            
        Raises:
            ConfigValidationError: If configuration is invalid or missing
        """
        try:
            # Check if config file exists
            if not os.path.exists(self.config_path):
                if create_if_missing:
                    self._create_example_config()
                    raise ConfigValidationError(
                        f"Configuration file '{self.config_path}' was missing and has been created. "
                        f"Please edit the file with your actual settings and try again."
                    )
                else:
                    raise ConfigValidationError(
                        f"Configuration file '{self.config_path}' not found. "
                        f"Please create it using the provided config.json.example as a template."
                    )
            
            # Load configuration data
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
                
            # Validate configuration structure and values
            self._validate_structure()
            self._apply_defaults()
            self._validate_values()
            
            print(f"✓ Configuration loaded successfully from {self.config_path}")
            return self.config_data
            
        except json.JSONDecodeError as e:
            raise ConfigValidationError(
                f"Invalid JSON in configuration file '{self.config_path}': {str(e)}"
            )
        except FileNotFoundError:
            raise ConfigValidationError(
                f"Configuration file '{self.config_path}' not found"
            )
        except Exception as e:
            raise ConfigValidationError(
                f"Error loading configuration: {str(e)}"
            )
    
    def _create_example_config(self) -> None:
        """Create an example configuration file."""
        example_config = {
            "azure_devops": {
                "organization": "your-org-name",
                "project": "your-project-name", 
                "personal_access_token": "your-pat-token-here",
                "user_id": "auto-detected",
                "work_item_type": "User Story",
                "states": ["Closed", "Resolved"],
                "fields": [
                    "System.Id",
                    "System.Title",
                    "Microsoft.VSTS.Common.ClosedDate", 
                    "System.Description",
                    "Microsoft.VSTS.Common.AcceptanceCriteria"
                ]
            },
            "llm_integration": {
                "provider": "roo_code",
                "api_key": "",
                "model": "",
                "fallback_to_roo": True,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            },
            "processing": {
                "output_directory": "data",
                "backup_csv": True,
                "date_range_months": 12,
                "default_source": "csv"
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(example_config, f, indent=2, ensure_ascii=False)
    
    def _validate_structure(self) -> None:
        """Validate the configuration structure against required schema."""
        for section_name, schema in self.REQUIRED_SCHEMA.items():
            # Skip optional sections if they don't exist - defaults will be applied
            if section_name in self.OPTIONAL_SECTIONS and section_name not in self.config_data:
                continue
                
            # Check if section exists
            if section_name not in self.config_data:
                raise ConfigValidationError(
                    f"Missing required configuration section: '{section_name}'"
                )
            
            section_data = self.config_data[section_name]
            
            # Check required fields
            for field in schema["required_fields"]:
                if field not in section_data or not section_data[field]:
                    raise ConfigValidationError(
                        f"Missing required field: '{section_name}.{field}'"
                    )
    
    def _apply_defaults(self) -> None:
        """Apply default values for missing optional fields."""
        for section_name, defaults in self.DEFAULT_VALUES.items():
            if section_name not in self.config_data:
                self.config_data[section_name] = {}
            
            section_data = self.config_data[section_name]
            
            for field, default_value in defaults.items():
                if field not in section_data:
                    section_data[field] = default_value
                    
    def _validate_values(self) -> None:
        """Validate specific field values against allowed values."""
        for field_path, valid_values in self.VALID_VALUES.items():
            section, field = field_path.split(".")
            
            if (section in self.config_data and 
                field in self.config_data[section]):
                
                value = self.config_data[section][field]
                if value not in valid_values:
                    raise ConfigValidationError(
                        f"Invalid value for '{field_path}': '{value}'. "
                        f"Valid values are: {', '.join(valid_values)}"
                    )
    
    def validate_azure_devops_connection(self) -> Tuple[bool, str]:
        """
        Test Azure DevOps connection and authentication.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Import ADO client here to avoid circular imports
            import sys
            import os
            ado_client_path = os.path.join(os.path.dirname(__file__), '..', 'ado_user_story_client.py')
            if os.path.exists(ado_client_path):
                sys.path.append(os.path.dirname(ado_client_path))
                from ado_user_story_client import ADOUserStoryClient
            else:
                # Try relative import for testing
                try:
                    from ado_user_story_client import ADOUserStoryClient
                except ImportError:
                    return False, "✗ ADO client module not found"
            
            ado_config = self.config_data.get("azure_devops", {})
            
            # Check required fields
            required_fields = ["organization", "project", "personal_access_token"]
            for field in required_fields:
                if not ado_config.get(field):
                    return False, f"Azure DevOps configuration missing required field: {field}"
            
            # Test connection
            client = ADOUserStoryClient(
                organization=ado_config["organization"],
                project=ado_config["project"],
                personal_access_token=ado_config["personal_access_token"]
            )
            
            if client.test_connection():
                # Get user ID if not already set
                if not ado_config.get("user_id") or ado_config.get("user_id") == "auto-detected":
                    user_id = client.get_current_user_id()
                    if user_id:
                        self.config_data["azure_devops"]["user_id"] = user_id
                        self._save_config()
                        return True, f"✓ Connection successful. User ID auto-detected: {user_id}"
                    else:
                        return True, "✓ Connection successful, but could not auto-detect user ID"
                else:
                    return True, "✓ Azure DevOps connection successful"
            else:
                return False, "✗ Azure DevOps connection failed. Check credentials and permissions."
                
        except ImportError:
            return False, "✗ ADO client module not found"
        except Exception as e:
            return False, f"✗ Error testing Azure DevOps connection: {str(e)}"
    
    def validate_llm_integration(self) -> Tuple[bool, str]:
        """
        Validate LLM integration configuration.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            llm_config = self.config_data.get("llm_integration", {})
            provider = llm_config.get("provider")
            
            if provider == "roo_code":
                # For Roo Code, we don't need API keys
                return True, "✓ Roo Code integration configured (no API key required)"
            
            elif provider in ["openai", "anthropic"]:
                api_key = llm_config.get("api_key")
                if not api_key or api_key.strip() == "":
                    return False, f"✗ {provider} provider requires api_key configuration"
                
                # Basic API key format validation
                if provider == "openai" and not api_key.startswith("sk-"):
                    return False, "✗ OpenAI API key should start with 'sk-'"
                
                return True, f"✓ {provider} integration configured (API key present)"
            
            else:
                return False, f"✗ Unknown LLM provider: {provider}"
                
        except Exception as e:
            return False, f"✗ Error validating LLM integration: {str(e)}"
    
    def _save_config(self) -> None:
        """Save the current configuration back to file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save updated configuration: {e}", file=sys.stderr)
    
    def get_config(self) -> Dict:
        """Get the loaded configuration data."""
        return self.config_data
    
    def get_azure_devops_config(self) -> Dict:
        """Get Azure DevOps configuration section."""
        return self.config_data.get("azure_devops", {})
    
    def get_llm_integration_config(self) -> Dict:
        """Get LLM integration configuration section."""
        return self.config_data.get("llm_integration", {})
    
    def get_processing_config(self) -> Dict:
        """Get processing configuration section."""
        return self.config_data.get("processing", {})
    
    def mask_sensitive_values(self, config: Optional[Dict] = None) -> Dict:
        """
        Create a copy of configuration with sensitive values masked for logging.
        
        Args:
            config: Configuration to mask. If None, uses loaded config.
            
        Returns:
            Configuration with sensitive values masked
        """
        if config is None:
            config = self.config_data
        
        masked_config = json.loads(json.dumps(config))  # Deep copy
        
        # Mask Azure DevOps PAT
        if "azure_devops" in masked_config and "personal_access_token" in masked_config["azure_devops"]:
            token = masked_config["azure_devops"]["personal_access_token"]
            if len(token) > 8:
                masked_config["azure_devops"]["personal_access_token"] = (
                    token[:4] + "*" * (len(token) - 8) + token[-4:]
                )
            else:
                masked_config["azure_devops"]["personal_access_token"] = "*" * len(token)
        
        # Mask LLM API keys
        if "llm_integration" in masked_config and "api_key" in masked_config["llm_integration"]:
            api_key = masked_config["llm_integration"]["api_key"]
            if len(api_key) > 8:
                masked_config["llm_integration"]["api_key"] = (
                    api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
                )
            else:
                masked_config["llm_integration"]["api_key"] = "*" * len(api_key)
        
        return masked_config
    
    def print_config_summary(self) -> None:
        """Print a summary of the current configuration."""
        masked_config = self.mask_sensitive_values()
        
        print("\nConfiguration Summary:")
        print("=" * 50)
        
        # Azure DevOps section
        ado_config = masked_config.get("azure_devops", {})
        print(f"Azure DevOps:")
        print(f"  Organization: {ado_config.get('organization', 'Not set')}")
        print(f"  Project: {ado_config.get('project', 'Not set')}")
        print(f"  Token: {ado_config.get('personal_access_token', 'Not set')}")
        print(f"  User ID: {ado_config.get('user_id', 'Not set')}")
        print(f"  Work Item Type: {ado_config.get('work_item_type', 'Not set')}")
        
        # LLM Integration section  
        llm_config = masked_config.get("llm_integration", {})
        print(f"LLM Integration:")
        print(f"  Provider: {llm_config.get('provider', 'Not set')}")
        print(f"  API Key: {llm_config.get('api_key', 'Not set')}")
        print(f"  Model: {llm_config.get('model', 'Not set')}")
        print(f"  Fallback to Roo: {llm_config.get('fallback_to_roo', 'Not set')}")
        
        # Processing section
        processing_config = masked_config.get("processing", {})
        print(f"Processing:")
        print(f"  Output Directory: {processing_config.get('output_directory', 'Not set')}")
        print(f"  Backup CSV: {processing_config.get('backup_csv', 'Not set')}")
        print(f"  Date Range (months): {processing_config.get('date_range_months', 'Not set')}")
        print(f"  Default Source: {processing_config.get('default_source', 'Not set')}")
        print("=" * 50)


def load_and_validate_config(config_path: str = "config.json", 
                           create_if_missing: bool = False,
                           test_connections: bool = True) -> Dict:
    """
    Convenience function to load and validate configuration.
    
    Args:
        config_path: Path to configuration file
        create_if_missing: Create example config if missing
        test_connections: Test Azure DevOps connection
        
    Returns:
        Validated configuration dictionary
        
    Raises:
        ConfigValidationError: If configuration is invalid
    """
    validator = ConfigValidator(config_path)
    config = validator.load_config(create_if_missing)
    
    if test_connections:
        # Test Azure DevOps connection
        ado_success, ado_message = validator.validate_azure_devops_connection()
        print(ado_message)
        
        # Validate LLM integration
        llm_success, llm_message = validator.validate_llm_integration()
        print(llm_message)
        
        if not ado_success:
            print("Warning: Azure DevOps connection validation failed. "
                 "CSV mode will be used as fallback.", file=sys.stderr)
    
    return config


if __name__ == "__main__":
    """Command-line interface for configuration validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Performance Review configuration")
    parser.add_argument("--config", default="config.json", help="Path to configuration file")
    parser.add_argument("--create", action="store_true", help="Create example config if missing")
    parser.add_argument("--no-test", action="store_true", help="Skip connection testing")
    parser.add_argument("--summary", action="store_true", help="Print configuration summary")
    
    args = parser.parse_args()
    
    try:
        validator = ConfigValidator(args.config)
        config = validator.load_config(create_if_missing=args.create)
        
        if args.summary:
            validator.print_config_summary()
        
        if not args.no_test:
            print("\nTesting connections...")
            
            # Test Azure DevOps
            ado_success, ado_message = validator.validate_azure_devops_connection()
            print(ado_message)
            
            # Test LLM integration
            llm_success, llm_message = validator.validate_llm_integration()
            print(llm_message)
        
        print(f"\n✓ Configuration validation completed successfully!")
        
    except ConfigValidationError as e:
        print(f"✗ Configuration validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
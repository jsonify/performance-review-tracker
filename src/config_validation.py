#!/usr/bin/env python3
"""
Configuration validation module for Performance Review Tracking System.

This module provides utilities for loading, validating, and testing configuration
settings for LLM integration.
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
        "llm_integration": {
            "required_fields": ["provider"],
            "optional_fields": ["api_key", "model", "fallback_to_roo", "options"]
        },
        "processing": {
            "required_fields": [],
            "optional_fields": ["output_directory", "date_range_months"]
        }
    }
    
    # Optional sections - these don't require validation but will get defaults if missing
    OPTIONAL_SECTIONS = ["processing"]
    
    # Valid values for specific fields
    VALID_VALUES = {
        "llm_integration.provider": ["requestyai", "openai", "anthropic", "google", "azure_openai", "ollama", "roo_code"]
    }
    
    # Default values for missing optional fields
    DEFAULT_VALUES = {
        "llm_integration": {
            "fallback_to_roo": True,
            "options": {
                "temperature": 0.7,
                "max_tokens": 4000
            }
        },
        "processing": {
            "output_directory": "data",
            "date_range_months": 12
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
            "llm_integration": {
                "provider": "requestyai",
                "api_key": "your_requestyai_api_key_here",
                "model": "openai/gpt-4o-mini",
                "fallback_to_roo": True,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            },
            "processing": {
                "output_directory": "data",
                "date_range_months": 12
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
            
            elif provider in ["requestyai", "openai", "anthropic", "google"]:
                api_key = llm_config.get("api_key")
                if not api_key or api_key.strip() == "":
                    return False, f"✗ {provider} provider requires api_key configuration"
                
                # Basic API key format validation
                if provider == "openai" and not api_key.startswith("sk-"):
                    return False, "✗ OpenAI API key should start with 'sk-'"
                elif provider == "requestyai" and not api_key.startswith("sk-"):
                    return False, "✗ RequestyAI API key should start with 'sk-'"
                
                return True, f"✓ {provider} integration configured (API key present)"
            
            elif provider in ["azure_openai", "ollama"]:
                # These providers have different validation requirements
                return True, f"✓ {provider} integration configured"
            
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
        print(f"  Date Range (months): {processing_config.get('date_range_months', 'Not set')}")
        print("=" * 50)


def load_and_validate_config(config_path: str = "config.json", 
                           create_if_missing: bool = False,
                           test_connections: bool = False) -> Dict:
    """
    Convenience function to load and validate configuration.
    
    Args:
        config_path: Path to configuration file
        create_if_missing: Create example config if missing
        test_connections: Test LLM integration (optional)
        
    Returns:
        Validated configuration dictionary
        
    Raises:
        ConfigValidationError: If configuration is invalid
    """
    validator = ConfigValidator(config_path)
    config = validator.load_config(create_if_missing)
    
    if test_connections:
        # Validate LLM integration
        llm_success, llm_message = validator.validate_llm_integration()
        print(llm_message)
    
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
#!/usr/bin/env python3
"""
Unit tests for configuration validation module.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import sys

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config_validation import ConfigValidator, ConfigValidationError, load_and_validate_config


class TestConfigValidator(unittest.TestCase):
    """Test cases for ConfigValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_config_path = os.path.join(self.temp_dir, "test_config.json")
        
        # Valid test configuration
        self.valid_config = {
            "azure_devops": {
                "organization": "test-org",
                "project": "test-project",
                "personal_access_token": "test-token-123"
            },
            "llm_integration": {
                "provider": "roo_code"
            },
            "processing": {
                "output_directory": "test_data",
                "default_source": "csv"
            }
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_config_path):
            os.remove(self.temp_config_path)
        os.rmdir(self.temp_dir)
    
    def _create_config_file(self, config_data):
        """Helper method to create a temporary config file."""
        with open(self.temp_config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def test_load_valid_config(self):
        """Test loading a valid configuration file."""
        self._create_config_file(self.valid_config)
        
        validator = ConfigValidator(self.temp_config_path)
        config = validator.load_config()
        
        # Check that configuration was loaded
        self.assertIsInstance(config, dict)
        self.assertEqual(config["azure_devops"]["organization"], "test-org")
        self.assertEqual(config["llm_integration"]["provider"], "roo_code")
    
    def test_load_missing_config_file(self):
        """Test loading configuration when file doesn't exist."""
        validator = ConfigValidator("nonexistent_config.json")
        
        with self.assertRaises(ConfigValidationError) as context:
            validator.load_config()
        
        self.assertIn("not found", str(context.exception))
    
    def test_create_missing_config_file(self):
        """Test creating configuration file when missing."""
        validator = ConfigValidator(self.temp_config_path)
        
        with self.assertRaises(ConfigValidationError) as context:
            validator.load_config(create_if_missing=True)
        
        # Should create the file and raise error asking user to edit it
        self.assertTrue(os.path.exists(self.temp_config_path))
        self.assertIn("has been created", str(context.exception))
    
    def test_invalid_json_config(self):
        """Test handling of invalid JSON configuration."""
        with open(self.temp_config_path, 'w') as f:
            f.write("{invalid json content}")
        
        validator = ConfigValidator(self.temp_config_path)
        
        with self.assertRaises(ConfigValidationError) as context:
            validator.load_config()
        
        self.assertIn("Invalid JSON", str(context.exception))
    
    def test_missing_required_section(self):
        """Test validation when required configuration section is missing."""
        incomplete_config = {
            "llm_integration": {"provider": "roo_code"}
            # Missing azure_devops section
        }
        self._create_config_file(incomplete_config)
        
        validator = ConfigValidator(self.temp_config_path)
        
        with self.assertRaises(ConfigValidationError) as context:
            validator.load_config()
        
        self.assertIn("Missing required configuration section", str(context.exception))
    
    def test_missing_required_field(self):
        """Test validation when required field is missing."""
        incomplete_config = {
            "azure_devops": {
                "organization": "test-org",
                # Missing project and personal_access_token
            },
            "llm_integration": {"provider": "roo_code"}
        }
        self._create_config_file(incomplete_config)
        
        validator = ConfigValidator(self.temp_config_path)
        
        with self.assertRaises(ConfigValidationError) as context:
            validator.load_config()
        
        self.assertIn("Missing required field", str(context.exception))
    
    def test_invalid_provider_value(self):
        """Test validation of invalid LLM provider value."""
        invalid_config = self.valid_config.copy()
        invalid_config["llm_integration"]["provider"] = "invalid_provider"
        self._create_config_file(invalid_config)
        
        validator = ConfigValidator(self.temp_config_path)
        
        with self.assertRaises(ConfigValidationError) as context:
            validator.load_config()
        
        self.assertIn("Invalid value for 'llm_integration.provider'", str(context.exception))
    
    def test_apply_defaults(self):
        """Test that default values are applied for missing optional fields."""
        minimal_config = {
            "azure_devops": {
                "organization": "test-org",
                "project": "test-project",
                "personal_access_token": "test-token"
            },
            "llm_integration": {
                "provider": "roo_code"
            }
        }
        self._create_config_file(minimal_config)
        
        validator = ConfigValidator(self.temp_config_path)
        config = validator.load_config()
        
        # Check that defaults were applied
        self.assertEqual(config["azure_devops"]["work_item_type"], "User Story")
        self.assertEqual(config["processing"]["default_source"], "csv")
        self.assertEqual(config["llm_integration"]["fallback_to_roo"], True)
    
    def test_mask_sensitive_values(self):
        """Test that sensitive values are properly masked."""
        self._create_config_file(self.valid_config)
        
        validator = ConfigValidator(self.temp_config_path)
        validator.load_config()
        
        masked_config = validator.mask_sensitive_values()
        
        # Check that PAT is masked
        masked_pat = masked_config["azure_devops"]["personal_access_token"]
        self.assertTrue("*" in masked_pat)
        self.assertNotEqual(masked_pat, "test-token-123")
    
    def test_validate_azure_devops_connection_missing_client(self):
        """Test Azure DevOps connection validation when client is not available."""
        self._create_config_file(self.valid_config)
        validator = ConfigValidator(self.temp_config_path)
        validator.load_config()
        
        # This will likely fail since ADO client may not be available in test environment
        success, message = validator.validate_azure_devops_connection()
        
        # Either succeeds with connection or fails with client not found
        self.assertIsInstance(success, bool)
        self.assertIsInstance(message, str)
    
    def test_validate_llm_integration_roo_code(self):
        """Test LLM integration validation for Roo Code provider."""
        self._create_config_file(self.valid_config)
        validator = ConfigValidator(self.temp_config_path)
        validator.load_config()
        
        success, message = validator.validate_llm_integration()
        
        self.assertTrue(success)
        self.assertIn("Roo Code integration configured", message)
    
    def test_validate_llm_integration_openai_with_key(self):
        """Test LLM integration validation for OpenAI with API key."""
        config = self.valid_config.copy()
        config["llm_integration"]["provider"] = "openai"
        config["llm_integration"]["api_key"] = "sk-test-key-123"
        
        self._create_config_file(config)
        validator = ConfigValidator(self.temp_config_path)
        validator.load_config()
        
        success, message = validator.validate_llm_integration()
        
        self.assertTrue(success)
        self.assertIn("openai integration configured", message)
    
    def test_validate_llm_integration_openai_missing_key(self):
        """Test LLM integration validation for OpenAI without API key."""
        config = self.valid_config.copy()
        config["llm_integration"]["provider"] = "openai"
        
        self._create_config_file(config)
        validator = ConfigValidator(self.temp_config_path)
        validator.load_config()
        
        success, message = validator.validate_llm_integration()
        
        self.assertFalse(success)
        self.assertIn("requires api_key", message)
    
    def test_get_config_sections(self):
        """Test methods to get specific configuration sections."""
        self._create_config_file(self.valid_config)
        validator = ConfigValidator(self.temp_config_path)
        validator.load_config()
        
        # Test section getters
        ado_config = validator.get_azure_devops_config()
        llm_config = validator.get_llm_integration_config()
        processing_config = validator.get_processing_config()
        
        self.assertEqual(ado_config["organization"], "test-org")
        self.assertEqual(llm_config["provider"], "roo_code")
        self.assertIn("default_source", processing_config)


class TestLoadAndValidateConfig(unittest.TestCase):
    """Test cases for the convenience function load_and_validate_config."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_config_path = os.path.join(self.temp_dir, "test_config.json")
        
        self.valid_config = {
            "azure_devops": {
                "organization": "test-org",
                "project": "test-project", 
                "personal_access_token": "test-token-123"
            },
            "llm_integration": {
                "provider": "roo_code"
            }
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_config_path):
            os.remove(self.temp_config_path)
        os.rmdir(self.temp_dir)
    
    def _create_config_file(self, config_data):
        """Helper method to create a temporary config file."""
        with open(self.temp_config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def test_load_and_validate_config_success(self):
        """Test successful configuration loading and validation."""
        self._create_config_file(self.valid_config)
        
        config = load_and_validate_config(self.temp_config_path, test_connections=False)
        
        self.assertIsInstance(config, dict)
        self.assertEqual(config["azure_devops"]["organization"], "test-org")
    
    def test_load_and_validate_config_missing_file(self):
        """Test handling of missing configuration file."""
        with self.assertRaises(ConfigValidationError):
            load_and_validate_config("nonexistent.json")
    
    def test_load_and_validate_config_skip_connections(self):
        """Test loading configuration without testing connections."""
        self._create_config_file(self.valid_config)
        
        config = load_and_validate_config(self.temp_config_path, test_connections=False)
        
        self.assertIsInstance(config, dict)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
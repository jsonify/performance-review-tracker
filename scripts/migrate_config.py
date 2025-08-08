#!/usr/bin/env python3
"""
Configuration Migration Utility

This script helps migrate old config.json format to the new enhanced structure
required for the Azure DevOps integration and LLM configuration.
"""

import json
import os
import sys
import shutil
from datetime import datetime


def migrate_config(old_config_path="config.json", backup=True):
    """
    Migrate old configuration format to new structure.
    
    Args:
        old_config_path: Path to existing configuration file
        backup: Whether to create backup of old config
    """
    
    # Check if old config exists
    if not os.path.exists(old_config_path):
        print(f"No existing configuration file found at {old_config_path}")
        return False
    
    # Load old configuration
    try:
        with open(old_config_path, 'r') as f:
            old_config = json.load(f)
    except Exception as e:
        print(f"Error reading old configuration: {e}")
        return False
    
    print("Old configuration detected:")
    print(json.dumps(old_config, indent=2))
    print()
    
    # Create backup if requested
    if backup:
        backup_path = f"{old_config_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(old_config_path, backup_path)
        print(f"✓ Backup created at: {backup_path}")
    
    # Migrate to new structure
    new_config = {
        "azure_devops": {
            "organization": old_config.get("organization", "your-org-name"),
            "project": old_config.get("project", "your-project-name"),
            "personal_access_token": old_config.get("personal_access_token", "your-pat-token-here"),
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
            "output_directory": old_config.get("output_directory", "data"),
            "backup_csv": True,
            "date_range_months": 12,
            "default_source": "csv"
        }
    }
    
    # Save new configuration
    try:
        with open(old_config_path, 'w') as f:
            json.dump(new_config, f, indent=2)
        print(f"✓ Configuration migrated successfully to new format")
        print(f"✓ Updated configuration saved at: {old_config_path}")
    except Exception as e:
        print(f"Error saving new configuration: {e}")
        return False
    
    print("\nNew configuration structure:")
    print(json.dumps(new_config, indent=2))
    print()
    print("✓ Migration completed successfully!")
    print("Please review the new configuration and adjust any settings as needed.")
    
    return True


def main():
    """Command line interface for configuration migration."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrate old config.json to new structure")
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file to migrate (default: config.json)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Skip creating backup of original file"
    )
    
    args = parser.parse_args()
    
    print("Performance Review Configuration Migration Utility")
    print("=" * 50)
    print()
    
    if migrate_config(args.config, backup=not args.no_backup):
        print("\n🎉 Configuration migration completed successfully!")
        print("\nNext steps:")
        print("1. Review the migrated configuration")
        print("2. Test the configuration: python src/config_validation.py --test-config")
        print("3. Generate reports: python src/main.py --type competency --source ado")
        return 0
    else:
        print("\n❌ Configuration migration failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
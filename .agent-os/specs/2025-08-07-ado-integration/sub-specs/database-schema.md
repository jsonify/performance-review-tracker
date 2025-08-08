# Database Schema

This is the database schema implementation for the spec detailed in @.agent-os/specs/2025-08-07-ado-integration/spec.md

> Created: 2025-08-07
> Version: 1.0.0

## Schema Changes

**No database changes required** - This implementation uses file-based data processing with JSON intermediate formats, maintaining the existing pandas DataFrame approach.

## Data Structure Enhancements

**Azure DevOps Raw Data Storage (JSON):**
```json
{
    "source": "azure_devops",
    "query_timestamp": "2025-08-07T10:30:00Z",
    "user_id": "99ab0929-d361-441b-b573-83589a0caff0",
    "query_criteria": {
        "work_item_type": "User Story",
        "state": "Closed",
        "date_range": {
            "start": "2024-09-01",
            "end": "2025-08-31"
        }
    },
    "work_items": [
        {
            "id": 12345,
            "fields": {
                "System.Title": "Implement user authentication",
                "System.Description": "...",
                "Microsoft.VSTS.Common.ClosedDate": "2025-06-15T14:30:00Z",
                "Microsoft.VSTS.Common.AcceptanceCriteria": "...",
                "System.State": "Closed"
            },
            "raw_data": {
                "fields": { /* Full API response */ }
            }
        }
    ]
}
```

**Processed Performance Data (JSON):**
```json
[
    {
        "Date": "2025-06-15",
        "Title": "Implement user authentication", 
        "Description": "Developed secure authentication system with OAuth2 integration...",
        "Acceptance Criteria": "User can login with corporate credentials...",
        "Success Notes": "Successfully closed User Story #12345 - Authentication system deployed",
        "Impact": "High",
        "Self Rating": 2,
        "Rating Justification": "Complex authentication implementation with significant business impact",
        "_metadata": {
            "source": "azure_devops",
            "work_item_id": 12345,
            "original_state": "Closed",
            "query_timestamp": "2025-08-07T10:30:00Z"
        }
    }
]
```

## File Structure Organization

**Data Directory Structure:**
```
data/
├── raw/
│   └── ado_raw_YYYYMMDD_HHMMSS.json       # Raw Azure DevOps responses
├── processed/
│   ├── processed_competency.json          # Processed for competency analysis
│   ├── processed_annual.json              # Processed for annual review  
│   └── backup_csv/                        # CSV backups for fallback
│       └── accomplishments_backup.csv
├── analyzed/
│   ├── analyzed_competency.md             # LLM analysis output
│   └── analyzed_annual.md
└── cache/
    └── ado_cache_30days.json             # Cached queries for performance
```

## Data Validation Schema

**Input Validation Rules:**
```python
VALIDATION_SCHEMA = {
    "required_fields": [
        "System.Title", 
        "Microsoft.VSTS.Common.ClosedDate",
        "System.Description"
    ],
    "date_formats": ["ISO8601", "YYYY-MM-DDTHH:mm:ssZ"],
    "impact_calculation": {
        "high_indicators": ["critical", "major", "complex"],
        "medium_indicators": ["moderate", "standard", "improvement"], 
        "low_indicators": ["minor", "simple", "bug fix"]
    },
    "rating_defaults": {
        "self_rating": 2,  # Default to "Good"
        "impact": "Medium"  # Default impact level
    }
}
```

## Migration Strategy

**Phase 1: Parallel Processing**
1. Maintain existing CSV workflow
2. Add Azure DevOps processing alongside
3. Generate both data sources for comparison

**Phase 2: Primary Integration** 
1. Make Azure DevOps the default data source
2. CSV becomes backup/fallback option
3. Automated migration tools for existing CSV data

**Phase 3: Full Integration**
1. Azure DevOps as primary source
2. CSV export capabilities for backup
3. Data archival and retention policies

## Backup and Recovery

**Backup Strategy:**
- Automatic CSV export of all processed data
- Raw API responses stored for 90 days
- Configuration backup with credentials masked
- Rollback capability to CSV processing if API fails

**Recovery Procedures:**
1. API failure → automatic fallback to last known good CSV backup
2. Configuration corruption → restore from backup with re-authentication
3. Data loss → regenerate from cached raw API responses
4. Complete system failure → manual CSV processing with existing templates
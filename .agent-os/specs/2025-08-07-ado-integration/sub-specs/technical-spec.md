# Technical Specification

This is the technical specification for the spec detailed in @.agent-os/specs/2025-08-07-ado-integration/spec.md

> Created: 2025-08-07
> Version: 1.0.0

## Technical Requirements

- **Azure DevOps API Integration** - REST API integration using Personal Access Token authentication
- **Data Transformation Layer** - Map User Story fields to existing performance review data structure
- **Configuration Management** - JSON-based config system with validation and error handling
- **Main Pipeline Integration** - Modify src/main.py to support Azure DevOps as primary data source
- **Backward Compatibility** - Maintain existing CSV processing workflow as fallback option
- **LLM Integration Evaluation** - Compare Roo Code vs direct API approaches with implementation recommendation
- **Error Recovery** - Graceful degradation and informative error messages for API failures

## Approach Options

**Option A: Roo Code Integration (Current)**
- Pros: Already implemented, VS Code integration, familiar workflow
- Cons: Dependency on VS Code, subprocess complexity, potential reliability issues, limited programmatic control

**Option B: Direct LLM API Integration (Recommended)**
- Pros: Programmatic control, better error handling, API reliability, tool flexibility (Requesty, direct OpenAI/Anthropic)
- Cons: Requires API key management, potentially higher costs, new implementation required

**Option C: Hybrid Approach**
- Pros: Best of both worlds, fallback mechanisms, user choice
- Cons: Higher complexity, maintenance overhead

**Rationale:** Option B is recommended for production reliability and programmatic control. The current Roo Code integration has shown subprocess complexity and reliability challenges that direct API integration can resolve.

## Data Mapping Strategy

**Azure DevOps User Story Fields → Performance Review Structure:**

```python
FIELD_MAPPING = {
    'System.Title': 'Title',
    'Microsoft.VSTS.Common.ClosedDate': 'Date',
    'System.Description': 'Description', 
    'Microsoft.VSTS.Common.AcceptanceCriteria': 'Acceptance Criteria',
    'System.Id': 'Work Item ID',  # Additional tracking
    'System.State': 'Status'      # For validation
}
```

**Derived Fields:**
- 'Success Notes': Generated from completion status and closure details
- 'Impact': Calculated based on User Story complexity, size, and business value
- 'Self Rating': Default to 2 (Good) with option for user override
- 'Rating Justification': Generated from accomplishment details and impact analysis

## Configuration Architecture

**config.json Structure:**
```json
{
    "azure_devops": {
        "organization": "your-org",
        "project": "your-project", 
        "personal_access_token": "your-pat",
        "user_id": "auto-detected",
        "work_item_type": "User Story",
        "states": ["Closed", "Resolved"],
        "fields": ["System.Title", "System.Description", ...]
    },
    "llm_integration": {
        "provider": "openai|anthropic|roo_code",
        "api_key": "your-key",
        "model": "gpt-4|claude-3-sonnet",
        "fallback_to_roo": true
    },
    "processing": {
        "output_directory": "data",
        "backup_csv": true,
        "date_range_months": 12
    }
}
```

## Integration Points

**main.py Modifications:**
1. Add `--source` parameter: `csv|ado|hybrid`
2. Implement `load_data_from_ado()` function
3. Add configuration validation and connection testing
4. Integrate LLM provider selection logic

**ado_user_story_client.py Enhancements:**
1. Add data transformation methods
2. Implement caching for repeated queries
3. Enhanced error handling and retry logic
4. Batch processing optimization

**LLM Integration Module (New):**
1. Abstract LLM provider interface
2. Provider-specific implementations (OpenAI, Anthropic, Roo Code)
3. Prompt templates and response parsing
4. Error handling and fallback mechanisms

## External Dependencies

**Python Packages:**
- **requests** - Already included for Azure DevOps API calls
- **openai** - For direct OpenAI API integration (if selected)
- **anthropic** - For direct Anthropic API integration (if selected)

**Justification:** 
- requests: Essential for REST API communication
- openai/anthropic: Required for direct LLM API integration, provides better control than subprocess calls
- Minimal new dependencies maintain system stability

## Performance Considerations

- **API Rate Limiting** - Implement exponential backoff and request batching
- **Caching Strategy** - Cache User Story queries for repeated analysis runs
- **Parallel Processing** - Batch API calls where possible to reduce latency
- **Memory Management** - Process large User Story datasets in chunks

## Security Requirements

- **Credential Management** - Store sensitive tokens in config.json with file permissions 600
- **API Security** - Validate all API responses and sanitize inputs
- **Error Information** - Avoid logging sensitive credentials in error messages
- **Token Rotation** - Support for updating PAT tokens without system restart
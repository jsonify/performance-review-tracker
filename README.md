# Performance Review Tracker

A comprehensive workplace productivity tool that helps professionals articulate their work accomplishments effectively for performance evaluations, career advancement, and salary negotiations through automated competency assessment and AI-assisted analysis.

## Core Features

- **Automated Competency Assessment**: Maps accomplishments to 13 professional competency areas using intelligent keyword analysis
- **Dual Analysis Modes**: Choose between automated Python processing or AI-assisted deep analysis
- **Multi-Format Output**: Professional Markdown and DOCX reports with customizable templates  
- **Impact-Based Rating System**: 5-point scale (Learning → Developing → Practicing → Mastering → Leading) with evidence-based scoring
- **Azure DevOps Integration**: Fully functional integration with automatic work item import and real-time data processing
- **Validation Framework**: Comprehensive quality checks with automatic data normalization and flexible validation
- **Smart Data Handling**: Automatic column detection, missing data normalization, and hybrid data source support

## Installation

1. Clone the repository
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Complete Configuration File

Create a `config.json` file in the project root with the following structure:

```json
{
    "azure_devops": {
        "organization": "YourOrgName",
        "project": "YourProjectName",
        "personal_access_token": "your_pat_token_here",
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
        "fallback_to_roo": true,
        "options": {
            "temperature": 0.7,
            "max_tokens": 4000
        }
    },
    "processing": {
        "output_directory": "data",
        "backup_csv": true,
        "date_range_months": 12,
        "default_source": "csv"
    }
}
```

**Configuration Sections:**
- **azure_devops**: Required for ADO integration
- **llm_integration**: Required for AI analysis (set to "roo_code" for current system)
- **processing**: Optional processing settings (defaults applied if missing)

### Quick Configuration Setup

The fastest way to get started:

```bash
# Generate example config.json file
python src/config_validation.py --create

# Edit the generated config.json with your actual settings
# Then validate your configuration and test connections
python src/config_validation.py

# Test configuration through main script
python src/main.py --test-config
```

### Configuration Validation

Additional validation commands:

```bash
# Validate config and test connections (default behavior)
python src/config_validation.py

# Show config summary without testing connections
python src/config_validation.py --summary --no-test
```

## Usage

### Quick Start

Generate a competency assessment with test data:
```bash
./scripts/run_assessment.sh --fresh
```

Or use existing data:
```bash
./scripts/run_assessment.sh
```

### Data Format

Prepare your accomplishments in CSV format with these columns:
- **Date**: When the accomplishment occurred (Required)
- **Title**: Brief description of the accomplishment (Required)
- **Description**: Detailed explanation of what was done (Optional - auto-filled if missing)
- **Acceptance Criteria**: Success criteria or requirements met (Optional - auto-filled if missing)
- **Success Notes**: Additional context about the success (Optional - auto-filled if missing)
- **Impact**: Business impact level (High/Medium/Low) (Optional - defaults to "Medium")
- **Self Rating**: Self-assessment (1-3 scale) (Optional - defaults to 2 "Good")
- **Rating Justification**: Reasoning for self-rating (Optional - auto-generated if missing)

**Note**: The system automatically handles missing columns by adding them with sensible defaults, making it flexible for various CSV formats.

### Data Source Options

#### Option 1: Azure DevOps Integration (Recommended)
Automatically import your work items from Azure DevOps:

```bash
# Generate competency assessment from ADO data
python src/main.py --source ado --type competency --format markdown

# Generate annual review from ADO data
python src/main.py --source ado --type annual --year 2025 --format docx
```

**Benefits**: Zero data entry, real-time accuracy, comprehensive work history

#### Option 2: CSV File Import
Use manually prepared CSV data:

```bash
# Generate from CSV file
python src/main.py --source csv --file data/accomplishments.csv --type competency --format markdown
```

**Benefits**: Full control over data, works without external integrations, automatic data normalization for incomplete files

#### Option 3: Hybrid Mode
Try Azure DevOps first, fallback to CSV if ADO fails:

```bash
# Hybrid mode with fallback
python src/main.py --source hybrid --file data/backup.csv --type competency --format markdown
```

**Benefits**: Best of both worlds - automatic data retrieval with manual backup

### Analysis Options

#### 1. Automated Python System
Fast, reliable processing using keyword analysis and statistical scoring:

Best for: Batch processing, consistent results, quick assessments

#### 2. AI-Assisted Analysis  
Advanced analysis with nuanced insights (requires compatible AI tools):

Best for: Detailed insights, strategic recommendations, complex scenarios

### Azure DevOps Standalone Usage

You can also use the ADO integration directly for data exploration:

```bash
# Test your ADO connection
python ado_user_story_client.py --config config.json --test-connection

# Get your user ID (needed for filtering)
python ado_user_story_client.py --config config.json --get-my-user-id

# Export all your closed work items
python ado_user_story_client.py --config config.json --filter-assigned-to-me --filter-state Closed

# Diagnose available work items in your project
python ado_user_story_client.py --config config.json --diagnose
```

## Output & Reports

### Report Structure
- **Executive Summary**: Overall performance metrics and key strengths
- **Competency Analysis**: Detailed assessment across 13 professional competency areas
- **Evidence-Based Ratings**: 1-5 scale with supporting accomplishments
- **Development Recommendations**: Specific areas for growth and career advancement

### Supported Formats
- **Markdown**: Clean, readable format for web and documentation
- **DOCX**: Professional Microsoft Word format for formal submissions
- **JSON**: Structured data for integration with other tools

## Competency Framework

### 13 Professional Competency Areas
1. **Programming/Software Development**: Coding, technical implementation, software engineering
2. **Solution Architecture**: System design, technical architecture, platform decisions  
3. **Systems Design**: Infrastructure, scalability, performance optimization
4. **Project Management**: Planning, execution, resource management, delivery
5. **Requirements Definition**: Analysis, specification, stakeholder management
6. **Testing**: Quality assurance, validation, test automation
7. **Problem Management**: Issue resolution, root cause analysis, troubleshooting
8. **Innovation**: Creative solutions, process improvement, new technology adoption
9. **Release/Deployment**: CI/CD, production deployment, release management
10. **Accountability**: Ownership, reliability, commitment to outcomes
11. **Influence**: Leadership, mentoring, cross-team collaboration
12. **Agility**: Adaptability, learning, response to change
13. **Inclusion**: Team building, diversity support, inclusive practices

### Rating Scale
1. **Learning** - Beginning to apply the competency with guidance
2. **Developing** - Building proficiency with occasional support
3. **Practicing** - Demonstrating consistent competency independently
4. **Mastering** - Advanced proficiency, able to guide others
5. **Leading** - Expert level, driving innovation and setting standards

## Customization

### Keyword Mapping
Modify `src/competency_keywords.py` to adjust automatic competency detection:
```python
COMPETENCY_KEYWORDS = {
    "Programming/Software Development": ["code", "develop", "programming"],
    "Solution Architecture": ["architecture", "design", "system"]
}
```

### Report Templates
Customize output by editing templates in `src/competency_formatter.py` and `templates/` directory.

## Testing

Run the test suite:
```bash
pytest
```

For test coverage:
```bash
pytest --cov=src tests/
```

## Integration

### Azure DevOps (Fully Functional)

The Azure DevOps integration is production-ready and provides:

- **Automatic Authentication**: Uses Personal Access Tokens for secure API access
- **Work Item Filtering**: Retrieves closed/resolved work items assigned to you
- **Real-time Data**: No manual CSV maintenance required
- **Flexible Configuration**: Configurable work item types, states, and fields
- **Connection Validation**: Built-in connection testing and diagnostics
- **Rate Limiting**: Respects Azure DevOps API limits with intelligent throttling
- **Caching**: Optional response caching for improved performance

#### Setup Steps

1. **Generate PAT**: Create a Personal Access Token in Azure DevOps with "Work Items (Read)" permission
2. **Configure**: Add your settings to `config.json` (see Configuration section above)
3. **Validate**: Run `python src/config_validation.py` to test connections
4. **Use**: Run `python src/main.py --source ado --type competency --format markdown`

#### Advanced Configuration Options

```json
{
    "azure_devops": {
        "organization": "YourOrg",
        "project": "YourProject", 
        "personal_access_token": "your_pat_here",
        "user_id": "auto-detected",
        "work_item_type": "User Story",
        "states": ["Closed", "Resolved", "Done"],
        "fields": [
            "System.Id",
            "System.Title",
            "Microsoft.VSTS.Common.ClosedDate",
            "System.Description",
            "Microsoft.VSTS.Common.AcceptanceCriteria",
            "Microsoft.VSTS.Scheduling.StoryPoints",
            "System.Tags"
        ]
    }
}
```

### Planned Integrations
- **Jira**: Issue and project tracking integration
- **GitHub**: Pull request and contribution analysis  
- **GitLab**: Merge request and pipeline integration
- **Direct LLM APIs**: Enhanced AI analysis capabilities

## Project Architecture

### Core Components
- **src/main.py**: Primary orchestration and entry point with multi-source data handling
- **src/competency_formatter.py**: Report generation and template system
- **src/competency_keywords.py**: Keyword-based competency mapping
- **src/config_validation.py**: Configuration validation and connection testing framework
- **ado_user_story_client.py**: Azure DevOps integration client with comprehensive API support
- **scripts/run_assessment.sh**: Automated workflow scripts

### Data Flow
```
Data Source (ADO/CSV/Hybrid) → Data Normalization → Data Validation → 
Competency Mapping → Rating Calculation → Template Application → Report Output
```

**Azure DevOps Flow**:
```
ADO API → Work Item Retrieval → Field Mapping → Data Transformation → 
Automatic Normalization → Standard Processing Pipeline → Report Generation
```

**Enhanced Processing Pipeline**:
```
Raw Data → Missing Column Detection → Default Value Assignment → 
Validation → Analysis → Template Rendering → Multi-Format Output
```

### Directory Structure
```
performance-review-tracker/
├── .agent-os/              # Agent OS product documentation
├── src/                    # Core Python modules  
├── scripts/                # Automation scripts
├── data/                   # Input CSV files and processed data
├── output/                 # Generated reports
├── templates/              # Report templates
├── criteria/               # Evaluation criteria definitions
├── tests/                  # Test suite
└── docs/                   # Documentation and guides
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License. See LICENSE file for details.

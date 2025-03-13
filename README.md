# Performance Review Tracking System

A Python-based system that helps employees track work accomplishments and generate structured reports for Annual Reviews and Competency Assessments.

## Overview

The Performance Review Tracking System streamlines the process of documenting and reporting work accomplishments by:
- Using a CSV file for continuous documentation
- Processing data through automated Python scripts
- Leveraging Roo Code's Performance Review Analyst mode for analysis
- Producing formatted reports for Annual Reviews and Competency Assessments

## Features

- **Continuous Documentation**: Track work accomplishments as they occur
- **Automated Analysis**: AI-powered analysis using Roo Code to map accomplishments to review criteria
- **Automated Report Generation**: Generate structured reports with specific examples and action plans
- **Multiple Output Formats**: Support for both Markdown and DOCX formats
- **VS Code Integration**: Easy-to-use tasks for common operations
- **Comprehensive Error Handling**: Clear error messages and progress reporting
- **Batch Processing**: Support for processing multiple entries

## Requirements

- Python 3.9+
- VS Code with Roo Code extension
- Required Python packages (see `requirements.txt`):
  - pandas (data processing)
  - python-docx (document creation)
  - markdown (markdown processing)
  - argparse (command line interface)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install VS Code and the Roo Code extension
3. Open the project in VS Code

## Usage

### Using VS Code Tasks

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Run Task" and select:
   - "Generate Annual Review" for annual reviews
   - "Generate Competency Assessment" for competency assessments
3. Enter the requested information (year, output format)

### Using Command Line

Generate an Annual Review report:
```bash
python src/main.py --file data/accomplishments.csv --type annual --year 2025 --format docx
```

Generate a Competency Assessment report:
```bash
python src/main.py --file data/accomplishments.csv --type competency --format markdown
```

### Using Performance Review Analyst Mode

The system now uses dedicated system prompt files for different review types, allowing for much simpler user prompts.

#### System Prompt Files

Two specialized system prompt files are included:
- `.roo/system-prompt-annual-analyst` - Contains the 7 Annual Review criteria with structured formatting instructions
- `.roo/system-prompt-competency-analyst` - Contains the 13 Competency Assessment criteria with structured formatting instructions

#### Using Annual Review Analysis

To generate an Annual Review report, use this simple prompt in Roo Code:

```text
@/data/accomplishments.csv @/.roo/system-prompt-annual-analyst Please generate my annual review report for 2025.
```

#### Using Competency Assessment Analysis

To generate a Competency Assessment report, use this prompt:

```text
@/data/accomplishments.csv @/.roo/system-prompt-competency-analyst Please generate my competency assessment.
```

#### Customizing for Different Job Roles

When your job role changes, simply edit the "COMPETENCY ASSESSMENT CRITERIA" section in the `.roo/system-prompt-competency-analyst` file. The system prompt is designed with clear section boundaries to make updates straightforward.

### Command Line Options

- `--file`: Path to the input CSV file (required)
- `--type`: Type of review ('annual' or 'competency') (required)
- `--year`: Year for annual review (required for annual reviews)
- `--format`: Output format ('markdown' or 'docx', default: markdown)
- `--output`: Custom output path for the generated report (optional)

## CSV File Format

The input CSV file should have the following columns:
- `Date`: When the work was completed
- `Title`: Brief title of the accomplishment
- `Description`: Detailed description of the work
- `Acceptance Criteria`: What defined success for this work
- `Success Notes`: How the work met or exceeded expectations
- `Impact`: Significance of the accomplishment (High/Medium/Low)

## Documentation

For detailed information about the system:
- Design Document: `docs/performance-review-tracking-system-design-document.md`
- Project Tasks: `docs/todo-list.md`
- Automation Plan: `docs/automation-implementation-plan.md`
- Workflow Automation: `docs/workflow-automation-plan.md`
- Performance Review Analyst Prompt: `docs/roo-code-annual-review-prompt.txt`
  - This file contains the main prompt to use in the Performance Review Analyst role.

## Testing

Run the automated tests to verify the system:
```bash
pytest tests/test_automation.py
```

## Security Considerations

- All processing is done locally within VS Code
- No external API calls required
- Data remains on the local system
- No persistent storage of sensitive information

## Future Enhancements

- Direct Google Sheets API integration
- Web-based interface
- Automated scheduling of monthly milestone reports
- Analytics on accomplishment distribution
- Integration with task tracking systems (e.g., Azure DevOps)

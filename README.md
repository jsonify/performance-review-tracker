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

### Performance Review Analyst Prompt

To use the Performance Review Analyst mode, use the following prompt, replacing `'data/accomplishments.csv'` with the path to your CSV file and adjusting the year as needed:

```text
'data/accomplishments.csv' I need to generate an Annual Review report for 2025. Please follow these instructions EXACTLY:

1. For EACH of these 7 criteria ONLY:
   - Communication
   - Flexibility
   - Initiative
   - Member Service
   - Personal Credibility
   - Quality and Quantity of Work
   - Teamwork

2. For EACH criterion, follow this EXACT structure:

   ## [Criterion Name]

   ### How I Met This Criterion
   - [Select ONLY 2-3 most relevant examples that demonstrate this criterion]
   - [For each example, include brief details and impact]
   - [DO NOT list all accomplishments - be selective]

   ### Areas for Improvement
   - [Identify 1-2 specific areas to improve for this criterion]
   - [Be specific and constructive]

   ### Improvement Plan
   - [Provide 3-5 concrete, actionable steps for improvement]
   - [Include measurable goals and timelines]

   ### Summary
   - [Write a concise paragraph summarizing performance in this area]
   - [Include key strengths and improvement opportunities]

3. IMPORTANT:
   - Select only the MOST RELEVANT examples for each criterion
   - If there's limited data for a criterion, make reasonable inferences
   - Provide improvement areas and plans even if they must be inferred
   - Be balanced and constructive
   - Follow the specified format precisely

4. End with an Overall Summary section that highlights key achievements and development areas.

DO NOT reorganize by accomplishment or impact level. Focus on analyzing by criteria.
```

**To use this prompt:**

1.  Open the `.roo/system-prompt-analyst` file.
2.  Copy and paste the prompt into the file.
3.  Modify the file path and year as needed.
4.  Run the "Generate Annual Review" VS Code task.

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

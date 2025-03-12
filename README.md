# Performance Review Tracking System

A Python-based system that helps employees track work accomplishments and generate structured reports for Annual Reviews and Competency Assessments.

## Overview

The Performance Review Tracking System streamlines the process of documenting and reporting work accomplishments by:
- Using Google Sheets for continuous documentation
- Processing data through a Python script
- Leveraging Claude AI for analysis and report generation
- Producing formatted reports for Annual Reviews and Competency Assessments

## Features

- **Continuous Documentation**: Track work accomplishments as they occur using Google Sheets
- **Flexible Tagging**: Tag entries with relevant Annual Review and Competency Assessment criteria
- **Smart Analysis**: AI-powered analysis to map accomplishments to review criteria
- **Automated Report Generation**: Generate structured reports with specific examples and action plans
- **Multiple Report Types**: Support for both Annual Reviews and Competency Assessments

## Requirements

- Python 3.9+
- Google Sheets API access
- Claude API access
- Required Python packages (see `requirements.txt`):
  - gspread (Google Sheets API)
  - google-auth (Authentication)
  - anthropic (Claude API)
  - python-docx (Document creation)
  - argparse (Command line interface)

## Usage

### Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API access:
   - Set up Google Sheets API credentials
   - Configure Claude API key
   - Store credentials securely (use environment variables)

### Running Reports

Generate an Annual Review report:
```bash
python src/main.py --file data/accomplishments.csv --type annual --year 2025 --format docx
```

Generate a Competency Assessment report:
```bash
python src/main.py --file data/accomplishments.csv --type competency --format markdown
```

## Documentation

For detailed information about the system:
- Design Document: `docs/performance-review-tracking-system-design-document.md`
- Project Tasks: `todo-list.md`

## Security Considerations

- API keys stored securely using environment variables
- Limited Google Sheets permissions (read-only for script)
- Data remains within user's Google account
- No persistent storage of work data by the script
- Implemented rate limiting for API calls

## Future Enhancements

- Web-based interface
- Email notifications
- Integration with task tracking systems
- Automated scheduling
- Analytics features
- Team collaboration features

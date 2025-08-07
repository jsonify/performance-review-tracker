# Competency Assessment System

A system for analyzing work accomplishments and generating comprehensive competency assessments with ratings and justifications.

## Assessment Options

You have two ways to generate competency assessments:

### 1. Automated System (Python-based)

This approach uses the Python scripts to automatically:
- Map accomplishments to competencies using keyword analysis
- Calculate ratings based on impact and evidence
- Generate formatted Markdown reports

### 2. Roo Performance Review Analyst Mode

Use Roo's custom Performance Review Analyst mode which:
- Provides more nuanced analysis
- Offers deeper insights into accomplishments
- Uses the updated system-prompt-competency-analyst with rating system

Choose the approach based on your needs:
- Automated System: Best for batch processing or quick assessments
- Roo Analyst Mode: Best for detailed, nuanced analysis with human-like insights

## Features

- Automatic mapping of accomplishments to competencies using keyword analysis
- 1-5 rating system with detailed justifications
- Evidence-based assessment with impact analysis
- Comprehensive Markdown report generation
- Clear, maintainable output format

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

This configuration file is used to set up the Azure DevOps client and should be stored in the root of the repo named `config.json`.

```json
{
    "organization": "CostcoWholesale",
    "project": "CloudModernization",
    "personal_access_token": "your_github_pat",
    "output_directory": "ado_user_stories"
}

```

## Usage

### Option 1: Automated System

1. Prepare your accomplishments data in CSV format with the following columns:
   - Title
   - Description
   - Success Notes
   - Impact (High/Medium/Low)
   - Date

2. Generate an assessment:
   ```bash
   # Generate fresh test data and run assessment
   ./scripts/run_assessment.sh --fresh

   # Or run with existing data
   ./scripts/run_assessment.sh
   ```

The system will:
1. Load accomplishments from data/accomplishments.csv
2. Map them to competencies using keyword analysis
3. Calculate ratings based on impact and evidence
4. Generate a comprehensive Markdown report in output/competency_assessment.md

### Option 2: Roo Analyst Mode

See [Roo Usage Guide](docs/roo-usage-guide.md) for detailed instructions on using Roo's Performance Review Analyst mode.

To generate a competency assessment in Roo:

1. Open VS Code
2. Switch to Performance Review Analyst mode
3. Use this exact format:
   ```
   'data/accomplishments.csv' (see below for file content)
   '.roo/system-prompt-competency-analyst' (see below for file content)
   Please generate my competency assessment.
   ```

Important: This specific format distinguishes competency assessments from annual reviews and ensures proper analysis.

The analysis will provide:
- 1-5 rating scale for each competency
- Evidence-based justifications
- Impact analysis
- Comprehensive explanations

For more details on the differences between competency assessments and annual reviews, see the [Roo Usage Guide](docs/roo-usage-guide.md).

## Report Structure

The generated report includes:

### Overall Summary
- Average competency rating
- Key strengths
- Total impact metrics

### Per Competency
- Rating (1-5)
- Supporting evidence
- Comprehensive justification including:
  - Rating context
  - Key achievements
  - Business impact
  - Growth trajectory (for high performers)

## Customization

### Adding Keywords

Edit `src/competency_keywords.py` to modify the keyword mappings for each competency:

```python
COMPETENCY_KEYWORDS = {
    "Programming/Software Development": [
        "code", "develop", "programming", ...
    ],
    ...
}
```

### Modifying Output Format

The output format can be customized by editing the templates in `CompetencyFormatter` class (`src/competency_formatter.py`).

## Testing

Run the test suite:
```bash
pytest
```

For test coverage:
```bash
pytest --cov=src tests/
```

## Project Structure

```
.
├── data/                       # Input data
│   ├── accomplishments.csv     # Work accomplishments
│   └── competencies-formatted.csv  # Rating definitions
├── src/
│   ├── competency_formatter.py # Output formatting
│   ├── competency_keywords.py  # Keyword mappings
│   └── example_assessment.py   # Main script
├── templates/                  # Example templates
├── tests/                     # Test suite
└── output/                    # Generated reports
```

## Rating Scale

1. **Learning** - Beginning to apply the competency
2. **Developing** - Building basic competency
3. **Practicing** - Demonstrating solid competency
4. **Mastering** - Leading and teaching others
5. **Leading** - Setting direction and driving innovation

Each rating includes specific evidence and comprehensive justification based on demonstrated accomplishments.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License. See LICENSE file for details.

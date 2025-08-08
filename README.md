# Performance Review Tracker

A comprehensive workplace productivity tool that helps professionals articulate their work accomplishments effectively for performance evaluations, career advancement, and salary negotiations through automated competency assessment and AI-assisted analysis.

## Core Features

- **Automated Competency Assessment**: Maps accomplishments to 13 professional competency areas using intelligent keyword analysis
- **Dual Analysis Modes**: Choose between automated Python processing or AI-assisted deep analysis
- **Multi-Format Output**: Professional Markdown and DOCX reports with customizable templates  
- **Impact-Based Rating System**: 5-point scale (Learning → Developing → Practicing → Mastering → Leading) with evidence-based scoring
- **Integration Ready**: Azure DevOps integration with planned support for Jira, GitHub, and other platforms
- **Validation Framework**: Comprehensive quality checks for report completeness and accuracy

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
    "organization": "OrganizationName",
    "project": "ProjectName",
    "personal_access_token": "your_github_pat",
    "output_directory": "ado_user_stories"
}

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
- **Date**: When the accomplishment occurred
- **Title**: Brief description of the accomplishment
- **Description**: Detailed explanation of what was done
- **Acceptance Criteria**: Success criteria or requirements met
- **Success Notes**: Additional context about the success
- **Impact**: Business impact level (High/Medium/Low)
- **Self Rating**: Optional self-assessment
- **Rating Justification**: Optional reasoning for self-rating

### Analysis Options

#### 1. Automated Python System
Fast, reliable processing using keyword analysis and statistical scoring:
```bash
python src/main.py --file data/accomplishments.csv --type competency --format markdown
```

Best for: Batch processing, consistent results, quick assessments

#### 2. AI-Assisted Analysis
Advanced analysis with nuanced insights (requires compatible AI tools):
```bash
python src/main.py --file data/accomplishments.csv --type annual --year 2025 --format docx
```

Best for: Detailed insights, strategic recommendations, complex scenarios

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

### Azure DevOps
Configure `config.json` for automatic work item import:
```json
{
    "organization": "YourOrg",
    "project": "YourProject", 
    "personal_access_token": "your_pat",
    "output_directory": "ado_user_stories"
}
```

### Planned Integrations
- **Jira**: Issue and project tracking integration
- **GitHub**: Pull request and contribution analysis
- **GitLab**: Merge request and pipeline integration
- **Direct LLM APIs**: Enhanced AI analysis capabilities

## Project Architecture

### Core Components
- **src/main.py**: Primary orchestration and entry point
- **src/competency_formatter.py**: Report generation and template system
- **src/competency_keywords.py**: Keyword-based competency mapping
- **src/validation.py**: Quality assurance and validation framework
- **ado_user_story_client.py**: Azure DevOps integration client
- **scripts/run_assessment.sh**: Automated workflow scripts

### Data Flow
```
CSV Input → Data Validation → Competency Mapping → 
Rating Calculation → Template Application → Report Output
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

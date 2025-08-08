# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

### Setup
```bash
# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Assessments
```bash
# Generate competency assessment with fresh test data
./scripts/run_assessment.sh --fresh

# Run with existing data
./scripts/run_assessment.sh

# Generate using main script
python src/main.py --file data/accomplishments.csv --type competency --format markdown
python src/main.py --file data/accomplishments.csv --type annual --year 2025 --format docx
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Code formatting and linting
black src/
flake8 src/
mypy src/
```

## Architecture Overview

This is a **Performance Review Tracking System** with dual functionality:
1. **Automated Python-based competency assessment**
2. **AI-assisted analysis using Roo Code integration**

### Core Architecture

**Data Flow Pipeline**: CSV Input → Processing → Analysis → Report Generation

**Key Components**:
- **src/main.py**: Primary orchestration script for end-to-end processing
- **src/competency_formatter.py**: Report formatting and template system
- **src/competency_keywords.py**: Keyword-based accomplishment-to-competency mapping
- **src/validation.py**: Report structure and content validation
- **templates/**: Markdown templates for different report types
- **criteria/**: JSON configuration files defining evaluation criteria

### Data Architecture

**Input Format** (CSV with required columns):
- Date, Title, Description, Acceptance Criteria, Success Notes, Impact, Self Rating, Rating Justification

**Processing Stages**:
1. **Data Loading & Validation**: Validates structure, date formats, and impact values
2. **Competency Mapping**: Uses keyword analysis to map accomplishments to 13 competency areas
3. **Rating Calculation**: Impact-based scoring (1-5 scale) with evidence aggregation
4. **Report Generation**: Template-driven Markdown/DOCX output

**Configuration System**:
- `config.json`: Azure DevOps integration settings (organization, project, PAT)
- Competency keyword mappings in `src/competency_keywords.py`
- Rating definitions in `data/competencies-formatted.csv`

## Dual Analysis Approaches

### 1. Automated Python System
**Entry Point**: `./scripts/run_assessment.sh` or `python src/example_assessment.py`
- Keyword-based competency mapping
- Statistical impact analysis
- Automated rating calculation
- Batch processing capabilities

### 2. Roo Code Integration
**Entry Point**: VS Code with Performance Review Analyst mode
- AI-driven analysis with nuanced insights
- Two distinct prompts: competency assessment vs annual review
- Manual but more sophisticated analysis
- Integration through `src/main.py` subprocess calls

**Roo Usage Pattern**:
```
# For competency assessment
@data/accomplishments.csv
@.roo/system-prompt-competency-analyst
Please generate my competency assessment.

# For annual review
@data/accomplishments.csv
@.roo/system-prompt-annual-review
Please generate my annual review.
```

## Key Implementation Details

### Competency System
- **13 Competency Areas**: Programming, Solution Architecture, Systems Design, Project Management, Requirements Definition, Testing, Problem Management, Innovation, Release/Deployment, Accountability, Influence, Agility, Inclusion
- **5-Point Rating Scale**: Learning (1) → Developing (2) → Practicing (3) → Mastering (4) → Leading (5)
- **Keyword-Based Mapping**: Each competency has associated keywords for automatic matching

### Report Generation Pipeline
1. **Data Processing**: `prepare_data_for_analysis()` validates and filters data
2. **Analysis Phase**: Either automated (`example_assessment.py`) or Roo Code integration
3. **Template Application**: Combines analysis with templates for final formatting
4. **Multi-Format Output**: Supports Markdown and DOCX through `markdown_to_docx()`

### Validation System
- **Structure Validation**: Checks for required headers, sections, hierarchy
- **Content Validation**: Ensures minimum length, impact mentions, accomplishment details
- **Criteria Coverage**: Validates against loaded criteria definitions

## Development Notes

### File Structure
- **src/**: Core Python modules
- **scripts/**: Bash automation scripts
- **data/**: Input CSV files and processed JSON
- **output/**: Generated reports
- **templates/**: Report templates
- **criteria/**: Evaluation criteria definitions
- **tests/**: Test suite (currently mostly commented out)
- **docs/**: Implementation plans and usage guides

### Key Dependencies
- **pandas**: Data processing and CSV handling
- **python-docx**: DOCX file generation
- **markdown**: Markdown processing
- **pytest**: Testing framework

### Error Handling Patterns
- Comprehensive input validation with descriptive error messages
- Graceful fallback to manual Roo Code instructions when subprocess fails
- File existence checks before processing
- Date format validation and conversion handling

### Testing Strategy
The codebase includes validation utilities but main test suite is currently disabled. When working with tests, focus on:
- Data structure validation
- Criteria coverage verification
- Report format validation
- Integration testing for the dual-path architecture

## Azure DevOps Integration

The system includes `ado_user_story_client.py` for Azure DevOps integration requiring:
- Organization and project configuration
- Personal Access Token authentication
- Output directory specification in `config.json`

## Agent OS Documentation

### Product Context
- **Mission & Vision:** @.agent-os/product/mission.md
- **Technical Architecture:** @.agent-os/product/tech-stack.md
- **Development Roadmap:** @.agent-os/product/roadmap.md
- **Decision History:** @.agent-os/product/decisions.md

### Development Standards
- **Code Style:** @~/.agent-os/standards/code-style.md
- **Best Practices:** @~/.agent-os/standards/best-practices.md

### Project Management
- **Active Specs:** @.agent-os/specs/
- **Spec Planning:** Use `@~/.agent-os/instructions/create-spec.md`
- **Tasks Execution:** Use `@~/.agent-os/instructions/execute-tasks.md`

## Workflow Instructions

When asked to work on this codebase:

1. **First**, check @.agent-os/product/roadmap.md for current priorities
2. **Then**, follow the appropriate instruction file:
   - For new features: @.agent-os/instructions/create-spec.md
   - For tasks execution: @.agent-os/instructions/execute-tasks.md
3. **Always**, adhere to the standards in the files listed above

## Important Notes

- Product-specific files in `.agent-os/product/` override any global standards
- User's specific instructions override (or amend) instructions found in `.agent-os/specs/...`
- Always adhere to established patterns, code style, and best practices documented above.
- Always update the @README.md as new features are added.
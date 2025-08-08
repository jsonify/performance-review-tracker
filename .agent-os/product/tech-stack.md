# Technical Stack

> Last Updated: 2025-08-07
> Version: 1.0.0

## Core Technologies

### Application Framework
- **Framework:** Python
- **Version:** 3.x
- **Language:** Python 3.8+

### Database
- **Primary:** File-based (CSV/JSON)
- **Version:** Pandas DataFrame processing
- **ORM:** Native Python data structures

## Data Processing Stack

### Data Pipeline
- **Input Format:** CSV with structured accomplishment data
- **Processing Engine:** Pandas for data manipulation and analysis
- **Intermediate Format:** JSON for processed analysis results
- **Validation:** Custom validation framework with comprehensive error handling

### Document Generation
- **Markdown Processing:** Python markdown library
- **DOCX Generation:** python-docx for Microsoft Word compatible output
- **Template Engine:** Jinja2-style template system for customizable report formats

## AI Integration

### Current Implementation
- **AI Assistant:** Roo Code (VS Code extension integration)
- **Integration Method:** Subprocess calls to main.py with analysis modes
- **Analysis Types:** Competency assessment and annual review generation

### Planned Enhancement
- **Direct LLM API:** Considering migration to direct API integration
- **Tool Options:** Evaluating Requesty or similar LLM API tools
- **Integration Strategy:** Replace VS Code dependency with direct API calls

## Development Tools

### Code Quality
- **Formatter:** Black for code formatting
- **Linter:** Flake8 for style and error checking
- **Type Checking:** MyPy for static type analysis
- **Testing Framework:** Pytest for comprehensive test coverage

### Automation
- **Build Tool:** Bash scripts for workflow orchestration
- **Entry Points:** Shell scripts in scripts/ directory for common operations
- **Task Runner:** Custom bash automation for assessment generation

## External Integrations

### Version Control Integration
- **Platform:** Git-based version control
- **Repository Structure:** Standard Python project layout with src/ organization

### Azure DevOps Integration
- **Service:** Azure DevOps REST API
- **Authentication:** Personal Access Token (PAT)
- **Data Source:** User stories and work items
- **Implementation:** ado_user_story_client.py module

### File System
- **Input Directory:** data/ for CSV accomplishment files
- **Output Directory:** output/ for generated reports
- **Templates:** templates/ for markdown report templates
- **Criteria:** criteria/ for JSON evaluation framework definitions

## Architecture Patterns

### Data Flow Architecture
- **Pipeline Pattern:** CSV Input → Processing → Analysis → Report Generation
- **Validation Gates:** Comprehensive data validation at each processing stage
- **Error Handling:** Graceful fallbacks with descriptive error messages
- **Modular Design:** Separate modules for competency mapping, formatting, and validation

### Dual Analysis System
- **Automated Path:** Python-based keyword analysis with statistical scoring
- **AI-Assisted Path:** Integration with external AI tools for nuanced analysis
- **Template System:** Shared template infrastructure for consistent output formatting

## Deployment Strategy

### Development Environment
- **Setup:** Virtual environment (venv) for dependency isolation
- **Dependencies:** requirements.txt for package management
- **Development Tools:** Integrated testing and validation framework

### Distribution
- **Format:** Source distribution with setup scripts
- **Entry Points:** Command-line scripts for assessment generation
- **Configuration:** JSON configuration files for customization

## Security Considerations

### Data Handling
- **Input Validation:** Comprehensive CSV and data structure validation
- **File Security:** Local file system operations with path validation
- **API Security:** Secure token handling for Azure DevOps integration

### Authentication
- **Azure DevOps:** Personal Access Token with limited scope
- **Local Security:** File system permissions for data directories
- **Configuration:** Secure storage of sensitive configuration data
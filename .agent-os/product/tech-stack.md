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
- **AI Integration:** Direct LLM API integration with multiple providers
- **Supported Providers:** OpenAI, Anthropic, Google, Azure OpenAI, Ollama, RequestyAI
- **Integration Method:** Native API calls through llm_client module
- **Analysis Types:** Competency assessment and annual review generation

### Provider Features
- **RequestyAI Gateway:** Unified access to multiple models with cost optimization
- **Fallback Strategy:** Graceful degradation to manual analysis if LLM fails
- **Configuration:** Flexible provider and model selection via config.json

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
- **API Security:** Secure token handling for LLM API integrations

### Authentication
- **LLM APIs:** Secure API key management for AI providers
- **Local Security:** File system permissions for data directories
- **Configuration:** Secure storage of sensitive configuration data
# Performance Review Tracker

A comprehensive workplace productivity tool that helps professionals articulate their work accomplishments effectively for performance evaluations, career advancement, and salary negotiations through automated competency assessment and AI-assisted analysis.

## 🌟 Key Features

### 🖥️ **Modern Web Interface**
- **Intuitive Web UI**: Complete browser-based interface with step-by-step workflow
- **Dual Input Methods**: Choose between JSON file upload OR user-friendly form entry for criteria
- **Real-time Validation**: Smart form validation with helpful error messages and duplicate prevention
- **Secure API Key Management**: Encrypted storage for LLM provider API keys with visual indicators
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### 🧠 **Advanced AI Integration**
- **Multiple LLM Providers**: OpenAI, Anthropic, Google, Azure OpenAI, Ollama, and RequestyAI unified gateway
- **Smart Fallbacks**: Graceful degradation ensures reliable report generation
- **Cost Optimization**: RequestyAI gateway provides up to 40% cost savings across providers
- **Flexible Configuration**: Use environment variables or secure web form entry for API keys

### 📊 **Comprehensive Analysis**
- **Automated Competency Assessment**: Maps accomplishments to 13 professional competency areas using intelligent keyword analysis
- **Impact-Based Rating System**: 5-point scale (Learning → Developing → Practicing → Mastering → Leading) with evidence-based scoring
- **Professional Report Generation**: High-quality Markdown and DOCX reports with customizable templates
- **Evidence-Based Ratings**: Detailed assessment with supporting accomplishments for each competency

### 🔗 **Data Processing**
- **Smart Data Handling**: Automatic column detection, missing data normalization, and flexible data processing
- **Validation Framework**: Comprehensive quality checks with automatic data normalization and flexible validation
- **CSV Upload Support**: Easy drag-and-drop CSV file upload with real-time validation

## 🚀 Quick Start

### 1. Installation

Clone the repository and set up your environment:
```bash
git clone <repository-url>
cd performance-review-tracker

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install core dependencies
pip install -r requirements.txt

# Install LLM provider dependencies (choose what you need)
pip install -r requirements-llm.txt
```

### 2. Launch Web Interface (Recommended)

Start the web interface for the easiest experience:
```bash
./scripts/run_ui.sh
```

Then open your browser to: **`http://localhost:8888`**

The web UI provides:
- **Step-by-Step Wizard**: Guided workflow from criteria setup to final report
- **Drag & Drop File Upload**: Easy CSV and JSON file handling
- **Secure API Key Storage**: Encrypted storage with visual management
- **Live Progress Tracking**: Real-time feedback during analysis
- **Direct Download**: Professional reports ready for immediate use

**📖 For detailed web UI guide, see [ui/README.md](ui/README.md)**

### 💻 Command Line Interface

For advanced users, automation, or CI/CD integration:

```bash
# Quick start with existing data
./scripts/run_assessment.sh

# Generate from CSV file  
python src/main.py --source csv --file data/accomplishments.csv --type competency --format markdown

# Test configuration
python src/main.py --test-config
```

## Usage Options

### 🌐 Web UI (Recommended)
The easiest way to use the Performance Review Tracker is through the web interface:

```bash
./scripts/run_ui.sh
```

Then open your browser to: `http://localhost:8888`

The web UI provides:
- **Intuitive Interface**: Step-by-step wizard for all functionality
- **Drag & Drop**: Easy file uploads for criteria and CSV data
- **LLM Configuration**: Support for all major AI providers with secure API key management
- **Real-time Progress**: Live feedback during analysis
- **Professional Output**: Direct download of Markdown and Word documents

For detailed web UI documentation, see [ui/README.md](ui/README.md).

### 💻 Command Line Interface
For advanced users or automation, use the command line interface:

```bash
# Quick start with existing data
./scripts/run_assessment.sh

# Or use the main script directly
python src/main.py --source csv --file data/accomplishments.csv --type competency --format markdown
```

## Configuration

### Option 1: Web UI Configuration (Recommended)

The web interface handles all configuration through intuitive forms:
- **LLM Providers**: Select provider, model, and enter API keys with secure storage
- **Review Settings**: Choose review type, year, and output format through dropdowns

### Option 2: JSON Configuration File

For advanced users or automation, create a `config.json` file in the project root:

```json
{
    "llm_integration": {
        "provider": "requestyai",
        "api_key": "your_requestyai_api_key_here",
        "model": "openai/gpt-4o-mini",
        "options": {
            "temperature": 0.7,
            "max_tokens": 4000
        }
    },
    "processing": {
        "output_directory": "data",
        "date_range_months": 12
    }
}
```

**Configuration Sections:**
- **llm_integration**: Required for AI analysis. Use `"requestyai"` for the unified gateway
- **processing**: Optional processing settings (defaults applied if missing)

**RequestyAI Configuration:**
To use RequestyAI as your unified LLM provider:
1. Sign up at [app.requesty.ai](https://app.requesty.ai) and get your API key
2. Set `"provider": "requestyai"` in your config
3. Choose from any supported model: `openai/gpt-4o`, `anthropic/claude-3-5-sonnet-20241022`, `google/gemini-1.5-pro`, etc.
4. Use a single API key to access all providers and models

### Quick Configuration Setup

The fastest way to get started:

```bash
# Generate example config file
python src/config_validation.py --create

# Validate configuration and test connections
python src/config_validation.py
```

## 📋 How To Use

### Web Interface Workflow (Recommended)

1. **Start the Web UI**: Run `./scripts/run_ui.sh` and open `http://localhost:8888`

2. **Configure Criteria** (Optional - skip to use defaults):
   - **Upload JSON Files**: Drag and drop criteria files for annual review or competency assessment
   - **Use Forms**: Fill out user-friendly forms to define criteria with real-time validation
   - **Mix & Match**: Upload for one type, use forms for another

3. **Choose Review Type**: Select "Competency Assessment" or "Annual Review" and set the year

4. **Upload Data**:
   - **CSV Upload**: Drag and drop your accomplishments CSV file with automatic validation

5. **Configure AI**:
   - Select LLM provider (RequestyAI recommended for cost savings)
   - Choose model appropriate for your needs
   - Enter API key (securely stored with encryption)

6. **Generate & Download**: Click generate, monitor real-time progress, and download your professional report

### Command Line Usage

For automation or advanced workflows:

```bash
# Quick start with existing data
./scripts/run_assessment.sh --fresh

# Generate from CSV files
python src/main.py --source csv --file data/accomplishments.csv --type competency --format markdown

### Analysis Options

#### 1. RequestyAI Unified Gateway (Recommended) 🌟
Access to multiple LLM providers through a single API key and unified interface:

- **Providers**: OpenAI, Anthropic, Google, Meta, Mistral, Cohere
- **Benefits**: Cost optimization (up to 40% savings), intelligent routing, 99.99% uptime SLA
- **Models**: All major models including GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro
- **Best for**: Production use, cost-conscious users, maximum reliability

#### 2. Individual Provider Integration
Direct integration with specific providers (OpenAI, Anthropic, Google, etc.):

Best for: Users with existing API relationships, specific model requirements

#### 3. Automated Python System (No AI)
Fast, reliable processing using keyword analysis and statistical scoring:

Best for: Batch processing, consistent results, quick assessments without AI costs


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

### Planned Integrations
- **Jira**: Issue and project tracking integration
- **GitHub**: Pull request and contribution analysis  
- **GitLab**: Merge request and pipeline integration
- **Direct LLM APIs**: Enhanced AI analysis capabilities

## 🏗️ Architecture

### Modern Web-First Design

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   Python Core   │    │   Data Sources  │
│                 │    │                 │    │                 │
│ • Drag & Drop   │◄──►│ • Main Engine   │◄──►│ • CSV Files     │
│ • Form Entry    │    │ • LLM Client    │    │ • JSON Config   │
│ • API Keys      │    │ • Validation    │    │ • Criteria      │
│ • Progress      │    │ • Keywords      │    │ • Templates     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

#### 🌐 **Web Interface Layer**
- **ui/app.py**: Flask web server with REST API endpoints
- **ui/templates/**: Modern Bootstrap-based responsive UI
- **ui/key_storage.py**: Encrypted API key management

#### 🐍 **Python Processing Core**  
- **src/main.py**: CSV processing orchestration with LLM integration
- **src/llm_client.py**: Unified LLM provider interface (OpenAI, Anthropic, Google, etc.)
- **src/competency_formatter.py**: Professional report generation with templates
- **src/config_validation.py**: Configuration validation and connection testing

#### 🔗 **Processing Layer**
- **src/competency_keywords.py**: Intelligent accomplishment-to-competency mapping

#### 🛠️ **Automation Scripts**
- **scripts/run_ui.sh**: Web interface startup with environment setup
- **scripts/run_assessment.sh**: Command-line assessment generation

### Data Processing Flow

```
┌─────────────────┐
│   Data Input    │
│ • CSV Upload    │
│ • Form Entry    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Normalization   │
│ • Column Detect │
│ • Missing Data  │
│ • Format Clean  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐
│   Analysis      │◄──►│ LLM Integration │
│ • Keyword Map   │    │ • Multi-Provider│
│ • Impact Score  │    │ • Smart Fallback│
│ • Evidence      │    │ • Cost Optimize │
└─────────┬───────┘    └─────────────────┘
          │
          ▼
┌─────────────────┐
│ Report Generate │
│ • Markdown      │
│ • DOCX Export   │
│ • Professional │
└─────────────────┘
```

### Directory Structure
```
performance-review-tracker/
├── ui/                     # 🌐 Web interface and templates
├── src/                    # 🐍 Core Python processing modules
├── scripts/                # 🛠️ Automation and startup scripts
├── data/                   # 📊 Sample data and outputs
├── templates/              # 📄 Report templates
├── criteria/               # 📋 Evaluation frameworks
├── tests/                  # 🧪 Test suite
├── requirements.txt        # 📦 Core dependencies
├── requirements-llm.txt    # 🧠 LLM provider dependencies
└── config.json.example     # ⚙️ Configuration template
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License. See LICENSE file for details.

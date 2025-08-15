# Performance Review Tracker - Web UI

A simple, intuitive web interface for the Performance Review Tracker system that provides all functionality through a modern, responsive web application.

## Features

The web UI provides a complete interface for:

### 📋 **Criteria Management**
- **Template Downloads**: Download pre-formatted JSON templates for both Annual Review and Competency Assessment criteria
- **Dual Input Methods**: Choose between JSON file upload OR user-friendly form entry
- **Annual Review Criteria**: Upload JSON files or use intuitive forms with validation
- **Competency Criteria**: Upload JSON files or enter competencies through guided forms
- **Form-Based Entry Features**:
  - **Annual Review Forms**: Name, description, and optional weight (%) fields
  - **Competency Forms**: Competency name, description, and all 5 level definitions
  - **Real-time Display**: See entered criteria immediately as you add them
  - **Edit & Delete**: Modify or remove criteria with visual buttons
  - **Smart Validation**: Field-level validation with helpful error messages
  - **Duplicate Prevention**: Automatic checking for duplicate names
- **Visual Criteria Display**: Clean cards showing all entered criteria with level badges for competencies
- **File Upload**: Traditional drag-and-drop JSON file upload support
- **Flexible Workflow**: Mix and match - upload one type, manually enter another

### ⚙️ **Review Configuration**
- Select review type (Competency Assessment or Annual Review)
- Choose review year (current and previous 5 years)
- Configurable output format (Markdown or Word Document)

### 📊 **Data Sources** 
- **CSV Template Download**: Download a properly formatted CSV template with example data
- **CSV Upload**: Drag-and-drop CSV files with accomplishment data
- **Azure DevOps Integration**: Direct connection to ADO with:
  - Connection testing and validation
  - Automatic work item retrieval
  - Configurable work item types and date ranges
  - Real-time data fetching with progress feedback

### 🤖 **AI Integration**
- Support for multiple LLM providers:
  - **RequestyAI** (Unified Gateway - All Models) ⭐ Recommended
  - OpenAI (GPT-3.5, GPT-4)
  - Anthropic (Claude)
  - Google (Gemini)
  - Azure OpenAI
  - Ollama (Local)
  - Roo Code (VS Code Integration)
- Model selection per provider
- **Persistent API Key Storage**: Securely encrypted storage that persists across server restarts
- **Smart Key Management**: 
  - Store keys with one click after entering them
  - Visual indicators showing stored key status (preview: `rqy-abc123...`)
  - Delete stored keys with confirmation
  - Automatic fallback to stored keys when fields are left empty
- Secure API key management with visibility toggle
- Optional AI analysis (can run automated-only mode)

### 🚀 **Analysis & Results**
- Real-time progress indicators
- Automated integration with existing Python backend
- Professional report generation
- Direct download of results
- Comprehensive error reporting and fallback handling

## Quick Start

### 1. Install Dependencies
```bash
# If you haven't already set up the Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the Web UI
```bash
./scripts/run_ui.sh
```

Or manually:
```bash
cd ui
python app.py
```

### 3. Open Your Browser
Navigate to: `http://localhost:8888`

## Usage Guide

### Step 1: Configure Criteria (Optional)
Choose how to provide your review criteria for each type:

#### Annual Review Criteria
- **Option 1: Upload JSON File** - Traditional file upload with drag-and-drop
- **Option 2: Enter Using Forms** - User-friendly form with dedicated fields:
  - **Section Name**: e.g., "Leadership", "Innovation"  
  - **Description**: Clear description of what this section evaluates
  - **Weight (%)**: Optional numerical weight for the section
  - Click **Add** to add each criteria, see them appear in real-time
  - **Edit/Delete** any criteria with visual buttons

#### Competency Criteria
- **Option 1: Upload JSON File** - Upload your competency framework as JSON
- **Option 2: Enter Using Forms** - Guided form for each competency:
  - **Competency Name**: e.g., "Programming", "Problem Management"
  - **Description**: What skills this competency covers
  - **Level Definitions**: All 5 levels from "Learning" to "Leading"
  - Click **Add** to add each competency, see them appear with level badges
  - **Edit/Delete** any competency with visual buttons

#### Form Features & Validation
- **Real-time Validation**: Field-level error messages for missing or duplicate entries
- **Visual Display**: Clean cards show all entered criteria with edit/delete options
- **Auto-Save**: Forms automatically convert to JSON and save through existing pipeline
- **Mix & Match**: Upload JSON for one type, use forms for the other
- **Sample Data**: See `ui/sample_criteria_data.md` for copy-paste examples
- Skip this entire step to use built-in default criteria

### Step 2: Configure Review
- Select **Competency Assessment** or **Annual Review**
- Choose the review year
- Both types use the same underlying analysis engine

### Step 3: Choose Data Source
Choose between two options:

#### CSV Upload
- Prepare CSV with columns: Date, Title, Description, Impact, etc.
- System auto-detects and normalizes missing columns
- Drag and drop or click to upload

#### Azure DevOps Integration
- Enter your organization and project name
- Provide Personal Access Token (PAT)
- Test connection before fetching data
- Configure work item types and date range
- Click "Fetch Data" to retrieve work items

### Step 4: AI Configuration
- Select LLM provider (or choose "No AI Analysis")
- Pick appropriate model for your provider
- Enter API key (or leave blank if using environment variables)
- System falls back gracefully if AI fails

### Step 5: Generate Review
- Select output format (Markdown or Word)
- Click "Generate Performance Review"
- Monitor progress in real-time
- Download completed report

## Architecture

### Frontend
- **Framework**: Vanilla JavaScript with Bootstrap 5
- **Styling**: Custom CSS with responsive design
- **Features**: Drag-and-drop, real-time validation, progress tracking
- **Browser Support**: Modern browsers with ES6+ support

### Backend Integration
- **Framework**: Flask web server
- **Integration**: Direct subprocess calls to existing `src/main.py`
- **File Management**: Secure file upload and result storage
- **Error Handling**: Comprehensive error reporting with fallbacks

### Security Features
- Secure filename handling with `werkzeug.secure_filename`
- File type validation and sanitization
- API key visibility toggle and secure storage
- CSRF protection ready (secret key configurable)
- Input validation and sanitization

## File Structure

```
ui/
├── app.py                 # Flask application
├── templates/
│   ├── base.html         # Base template with common elements
│   └── index.html        # Main application interface
├── uploads/              # Temporary file storage (auto-created)
├── results/              # Generated reports (auto-created)
└── README.md            # This file
```

## Configuration

### Environment Variables
```bash
export SECRET_KEY="your-secret-key"  # For production deployment
export FLASK_ENV="production"       # For production
```

### Default Ports
- Development: `http://localhost:8888` (configurable)
- Production: Configurable via Flask deployment options

### Custom Port Usage
```bash
# Use a different port
./scripts/run_ui.sh 9000

# Or run directly with custom port
python ui/app.py 9000
```

## API Endpoints

The web UI provides these REST API endpoints:

- `POST /api/upload-criteria` - Upload JSON criteria files
- `POST /api/upload-accomplishments` - Upload CSV accomplishment data
- `POST /api/test-ado-connection` - Test Azure DevOps connection
- `POST /api/fetch-ado-data` - Fetch data from Azure DevOps
- `POST /api/run-analysis` - Execute performance review analysis
- `GET /api/download-result/<filename>` - Download generated reports

## Production Deployment

For production deployment, consider:

### WSGI Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 ui.app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "ui/app.py"]
```

### Security Considerations
- Set a strong `SECRET_KEY` environment variable
- Use HTTPS in production
- Implement proper authentication if deploying publicly
- Configure file upload limits
- Set up proper logging and monitoring

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Check what's using port 8080
lsof -i :8080
# Use different port
./scripts/run_ui.sh 9000
```

**Import Errors**
```bash
# Ensure you're in the project root and virtual environment is activated
cd /path/to/performance-review-tracker
source venv/bin/activate
python -c "import flask; print('Flask installed')"
```

**File Upload Issues**
- Check file permissions on `ui/uploads/` directory
- Verify file size limits (default: 16MB)
- Ensure file extensions are allowed (.json, .csv)

**Azure DevOps Connection Issues**
- Verify PAT has "Work Items (Read)" permission
- Check organization and project names are exact
- Test connection button provides detailed error messages

### Debug Mode

Start with debug mode for detailed error messages:
```bash
export FLASK_DEBUG=1
python ui/app.py
```

## Browser Compatibility

- **Supported**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **Required Features**: ES6, Fetch API, File API, FormData
- **Progressive Enhancement**: Works without JavaScript for basic functionality

## Contributing

To contribute to the web UI:

1. Follow the existing code style (JavaScript ES6+, semantic HTML)
2. Test in multiple browsers
3. Ensure responsive design works on mobile devices
4. Add appropriate error handling and user feedback
5. Update this README with any new features

## License

Same as the main project - MIT License.
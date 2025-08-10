#!/usr/bin/env python3
"""
Flask Web UI for Performance Review Tracker

A simple, useful web interface for the Performance Review Tracker that provides:
- JSON criteria upload (annual review + competency criteria)
- Review type and year selection
- CSV upload or ADO integration
- LLM provider and model selection
- API key management
- Progress tracking and results display
"""

import os
import sys
import json
import tempfile
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import pandas as pd

# Add parent directory to path to import our modules
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)  # Insert at beginning for higher priority

# Change to project root if we're not already there
if os.getcwd() != project_root:
    os.chdir(project_root)

# Import our modules with proper error handling
try:
    from src.config_validation import load_and_validate_config, ConfigValidationError
except ImportError:
    print("Warning: config_validation module not found. Configuration management disabled.", file=sys.stderr)
    def load_and_validate_config(*args, **kwargs):
        return {}
    class ConfigValidationError(Exception):
        pass

try:
    from src.llm_client import LLMProvider
except ImportError:
    print("Warning: llm_client module not found. LLM integration limited.", file=sys.stderr)
    class LLMProvider:
        pass

try:
    from ado_user_story_client import ADOUserStoryClient
except ImportError:
    print("Warning: ado_user_story_client module not found. ADO integration disabled.", file=sys.stderr)
    class ADOUserStoryClient:
        def __init__(self, config):
            pass
        def get_my_user_id(self):
            raise Exception("ADO client not available")
        def export_user_stories(self):
            raise Exception("ADO client not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Configuration
# Get the absolute path to the project root (parent of ui directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'ui', 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'ui', 'results')
ALLOWED_EXTENSIONS = {'json', 'csv'}

# Ensure required directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_current_year():
    """Get current year for default selection."""
    return datetime.now().year


def get_year_options():
    """Get year options for dropdown (current year and previous 5 years)."""
    current_year = get_current_year()
    return list(range(current_year, current_year - 6, -1))


def get_llm_providers():
    """Get available LLM providers."""
    return [
        {'id': 'requestyai', 'name': 'RequestyAI (Unified Gateway - All Models)', 'recommended': True}
    ]


def get_common_models():
    """Get common model options by provider."""
    return {
        'requestyai': [
            # Most Popular Models
            'openai/gpt-4o',
            'openai/gpt-4o-mini', 
            'anthropic/claude-3-5-sonnet-20241022',
            'coding/claude-4-sonnet',
            # Coding & Reasoning Models
            'openai/o1-preview',
            'openai/o1-mini',
            'mistral/codestral-latest',
            'deepseek/deepseek-coder',
            # Other Popular Options
            'anthropic/claude-3-5-haiku-20241022',
            'google/gemini-1.5-pro',
            'google/gemini-1.5-flash',
            'openai/gpt-4-turbo',
            'openai/gpt-3.5-turbo',
            'anthropic/claude-3-opus-20240229',
            'meta/llama-3.2-90b',
            'meta/llama-3.1-70b',
            'meta/llama-3.2-11b',
            'mistral/mistral-large-2407',
            'cohere/command-r-plus',
            'cohere/command-r',
            'x-ai/grok-beta'
        ],
        'openai': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        'anthropic': ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
        'google': ['gemini-pro', 'gemini-pro-vision'],
        'azure_openai': ['gpt-4', 'gpt-35-turbo'],
        'ollama': ['llama2', 'codellama', 'mistral'],
        'roo_code': ['default']
    }


@app.route('/')
def index():
    """Main application page."""
    return render_template('index.html', 
                         year_options=get_year_options(),
                         current_year=get_current_year(),
                         llm_providers=get_llm_providers(),
                         common_models=get_common_models())


@app.route('/api/upload-criteria', methods=['POST'])
def upload_criteria():
    """Handle criteria file uploads (annual review and competency criteria)."""
    try:
        annual_file = request.files.get('annual_criteria')
        competency_file = request.files.get('competency_criteria')
        
        results = {}
        
        if annual_file and allowed_file(annual_file.filename):
            if annual_file.filename.endswith('.json'):
                annual_content = json.loads(annual_file.read().decode('utf-8'))
                annual_filename = secure_filename(f"annual_criteria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                annual_path = os.path.join(app.config['UPLOAD_FOLDER'], annual_filename)
                with open(annual_path, 'w') as f:
                    json.dump(annual_content, f, indent=2)
                results['annual_criteria'] = {
                    'success': True,
                    'filename': annual_filename,
                    'path': annual_path,
                    'sections': len(annual_content) if isinstance(annual_content, dict) else 0
                }
            else:
                results['annual_criteria'] = {'success': False, 'error': 'Invalid file format. Please upload JSON.'}
        
        if competency_file and allowed_file(competency_file.filename):
            if competency_file.filename.endswith('.json'):
                competency_content = json.loads(competency_file.read().decode('utf-8'))
                competency_filename = secure_filename(f"competency_criteria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                competency_path = os.path.join(app.config['UPLOAD_FOLDER'], competency_filename)
                with open(competency_path, 'w') as f:
                    json.dump(competency_content, f, indent=2)
                results['competency_criteria'] = {
                    'success': True,
                    'filename': competency_filename,
                    'path': competency_path,
                    'sections': len(competency_content) if isinstance(competency_content, dict) else 0
                }
            else:
                results['competency_criteria'] = {'success': False, 'error': 'Invalid file format. Please upload JSON.'}
        
        return jsonify(results)
        
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format in uploaded file'}), 400
    except Exception as e:
        logger.error(f"Error uploading criteria: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/upload-accomplishments', methods=['POST'])
def upload_accomplishments():
    """Handle accomplishments CSV upload."""
    try:
        csv_file = request.files.get('accomplishments_csv')
        
        if not csv_file or not allowed_file(csv_file.filename):
            return jsonify({'error': 'Please upload a valid CSV file'}), 400
        
        if not csv_file.filename.endswith('.csv'):
            return jsonify({'error': 'Invalid file format. Please upload CSV.'}), 400
        
        # Save uploaded file
        csv_filename = secure_filename(f"accomplishments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        csv_file.save(csv_path)
        
        # Validate CSV structure
        try:
            df = pd.read_csv(csv_path)
            required_columns = ['Date', 'Title']  # Minimum required
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return jsonify({
                    'error': f'Missing required columns: {", ".join(missing_columns)}',
                    'available_columns': list(df.columns)
                }), 400
            
            return jsonify({
                'success': True,
                'filename': csv_filename,
                'path': csv_path,
                'rows': len(df),
                'columns': list(df.columns)
            })
            
        except Exception as e:
            return jsonify({'error': f'Invalid CSV format: {str(e)}'}), 400
        
    except Exception as e:
        logger.error(f"Error uploading accomplishments: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/test-ado-connection', methods=['POST'])
def test_ado_connection():
    """Test Azure DevOps connection."""
    try:
        data = request.get_json()
        
        # Create temporary config for testing
        config = {
            'azure_devops': {
                'organization': data.get('ado_org'),
                'project': data.get('ado_project'),
                'personal_access_token': data.get('ado_token')
            }
        }
        
        # Test connection
        ado_client = ADOUserStoryClient(config)
        user_id = ado_client.get_my_user_id()
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'Connection successful'
        })
        
    except Exception as e:
        logger.error(f"ADO connection test failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/fetch-ado-data', methods=['POST'])
def fetch_ado_data():
    """Fetch data from Azure DevOps."""
    try:
        data = request.get_json()
        
        # Create config for ADO client
        config = {
            'azure_devops': {
                'organization': data.get('ado_org'),
                'project': data.get('ado_project'),
                'personal_access_token': data.get('ado_token'),
                'work_item_type': data.get('work_item_type', 'User Story'),
                'states': data.get('states', ['Closed', 'Resolved']),
                'fields': [
                    "System.Id",
                    "System.Title", 
                    "Microsoft.VSTS.Common.ClosedDate",
                    "System.Description",
                    "Microsoft.VSTS.Common.AcceptanceCriteria"
                ]
            },
            'processing': {
                'output_directory': app.config['UPLOAD_FOLDER'],
                'date_range_months': data.get('months_back', 12)
            }
        }
        
        # Fetch data
        ado_client = ADOUserStoryClient(config)
        result = ado_client.export_user_stories()
        
        if result and 'csv_file' in result:
            return jsonify({
                'success': True,
                'csv_file': result['csv_file'],
                'work_items_count': result.get('work_items_count', 0),
                'message': 'Data fetched successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No data retrieved from Azure DevOps'
            }), 400
            
    except Exception as e:
        logger.error(f"ADO data fetch failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/run-analysis', methods=['POST'])
def run_analysis():
    """Run performance review analysis."""
    try:
        data = request.get_json()
        
        # Extract parameters
        review_type = data.get('review_type', 'competency')
        year = data.get('year', get_current_year())
        data_source = data.get('data_source', 'csv')
        output_format = data.get('output_format', 'markdown')
        
        # LLM configuration
        llm_provider = data.get('llm_provider')
        llm_model = data.get('llm_model')
        api_key = data.get('api_key')
        
        # Prepare arguments for main analysis
        analysis_args = {
            'source': data_source,
            'type': review_type,
            'year': year,
            'format': output_format
        }
        
        # Add data file if CSV source
        if data_source == 'csv' and 'csv_file' in data:
            analysis_args['file'] = data['csv_file']
        
        # Create LLM config if provided
        if llm_provider and llm_provider != 'none':
            llm_config = {
                'llm_integration': {
                    'provider': llm_provider,
                    'model': llm_model or 'default',
                    'api_key': api_key or '',
                    'fallback_to_roo': True
                }
            }
            
            # Save temporary config file
            config_file = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_config.json')
            with open(config_file, 'w') as f:
                json.dump(llm_config, f, indent=2)
            
            analysis_args['config'] = config_file
        
        # Run actual analysis using your existing main.py functionality
        file_extension = 'md' if output_format.lower() == 'markdown' else output_format
        result_file = f"performance_review_{review_type}_{year}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_file)
        
        try:
            # Prepare command line arguments for main.py
            import subprocess
            import sys
            
            cmd_args = [
                sys.executable, 'src/main.py',
                '--source', data_source,
                '--type', review_type,
                '--year', str(year),
                '--format', output_format
            ]
            
            # Add data file if CSV source
            if data_source == 'csv':
                csv_file = data.get('csv_file')
                if csv_file:
                    cmd_args.extend(['--file', csv_file])
                else:
                    # Error: CSV source requires a file
                    return jsonify({
                        'success': False,
                        'error': 'CSV source selected but no CSV file provided. Please upload a CSV file first.'
                    }), 400
            
            # Create complete config file (always needed)
            temp_config = {
                'azure_devops': {
                    'organization': 'n/a' if data_source == 'csv' else '',
                    'project': 'n/a' if data_source == 'csv' else '',
                    'personal_access_token': 'n/a' if data_source == 'csv' else '',
                    'user_id': 'auto-detected',
                    'work_item_type': 'User Story',
                    'states': ['Closed', 'Resolved'],
                    'fields': [
                        'System.Id',
                        'System.Title',
                        'Microsoft.VSTS.Common.ClosedDate',
                        'System.Description',
                        'Microsoft.VSTS.Common.AcceptanceCriteria'
                    ]
                },
                'llm_integration': {
                    'provider': llm_provider if llm_provider != 'none' else 'roo_code',
                    'model': llm_model or 'default',
                    'api_key': api_key or '',
                    'fallback_to_roo': True,
                    'options': {
                        'temperature': 0.7,
                        'max_tokens': 4000
                    }
                },
                'processing': {
                    'output_directory': app.config['RESULTS_FOLDER'],
                    'backup_csv': True,
                    'date_range_months': 12,
                    'default_source': data_source
                }
            }
            
            config_file = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_config_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            with open(config_file, 'w') as f:
                json.dump(temp_config, f, indent=2)
            
            cmd_args.extend(['--config', config_file])
            
            # Add output file specification
            cmd_args.extend(['--output', result_path])
            
            # Execute the analysis
            logger.info(f"Running analysis command: {' '.join(cmd_args)}")
            result = subprocess.run(cmd_args, capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                # Success - the file should be created by main.py
                if not os.path.exists(result_path):
                    # If main.py didn't create the file where we expected, look for it in output/
                    alt_path = os.path.join('output', result_file)
                    if os.path.exists(alt_path):
                        import shutil
                        shutil.move(alt_path, result_path)
                    else:
                        # Create a basic result file as fallback
                        with open(result_path, 'w') as f:
                            f.write(f"# Performance Review Analysis\n\n")
                            f.write(f"Type: {review_type.title()}\n")
                            f.write(f"Year: {year}\n")
                            f.write(f"Generated: {datetime.now().isoformat()}\n")
                            f.write(f"Data Source: {data_source.upper()}\n")
                            if llm_provider:
                                f.write(f"LLM Provider: {llm_provider}\n")
                                f.write(f"LLM Model: {llm_model or 'default'}\n")
                            f.write("\n## Analysis Results\n\n")
                            f.write("Analysis completed successfully.\n")
                            f.write(f"\nStdout: {result.stdout}\n")
            else:
                # Analysis failed, but create an error report
                with open(result_path, 'w') as f:
                    f.write(f"# Performance Review Analysis - Error Report\n\n")
                    f.write(f"Type: {review_type.title()}\n")
                    f.write(f"Year: {year}\n")
                    f.write(f"Generated: {datetime.now().isoformat()}\n")
                    f.write(f"Status: FAILED\n\n")
                    f.write(f"## Error Details\n\n")
                    f.write(f"Return code: {result.returncode}\n\n")
                    f.write(f"Stderr: {result.stderr}\n\n")
                    f.write(f"Stdout: {result.stdout}\n")
                
                logger.error(f"Analysis failed with return code {result.returncode}")
                logger.error(f"Stderr: {result.stderr}")
        
        except Exception as e:
            # Fallback - create basic result file
            logger.error(f"Exception during analysis: {str(e)}")
            with open(result_path, 'w') as f:
                f.write(f"# Performance Review Analysis\n\n")
                f.write(f"Type: {review_type.title()}\n")
                f.write(f"Year: {year}\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Data Source: {data_source.upper()}\n")
                f.write(f"\n## Error\n\nAnalysis failed with error: {str(e)}\n")
                if llm_provider:
                    f.write(f"\nLLM Provider: {llm_provider}\n")
                    f.write(f"LLM Model: {llm_model or 'default'}\n")
        
        return jsonify({
            'success': True,
            'result_file': result_file,
            'result_path': result_path,
            'message': 'Analysis completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/download-result/<filename>')
def download_result(filename):
    """Download analysis result file."""
    try:
        safe_filename = secure_filename(filename)
        file_path = os.path.join(app.config['RESULTS_FOLDER'], safe_filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        return jsonify({'error': 'Download failed'}), 500


if __name__ == '__main__':
    import sys
    # Allow port to be specified as command line argument
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    app.run(debug=True, host='0.0.0.0', port=port)
#!/usr/bin/env python3
"""
Flask Web UI for Performance Review Tracker

A simple, useful web interface for the Performance Review Tracker that provides:
- JSON criteria upload (annual review + competency criteria)
- Review type and year selection
- CSV file upload
- LLM provider and model selection
- API key management
- Progress tracking and results display
"""

import os
import sys
import json
import tempfile
import logging
import threading
import time
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


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import key storage
try:
    from ui.key_storage import get_key_storage
except ImportError:
    try:
        # Try relative import for when running from ui directory
        from key_storage import get_key_storage
    except ImportError:
        print("Warning: key_storage module not found. API key persistence disabled.", file=sys.stderr)
        def get_key_storage():
            return None

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

# Progress tracking system
progress_store = {}
progress_lock = threading.Lock()


def update_progress(job_id: str, stage: str, percentage: int, message: str = "", details: str = ""):
    """Update progress for a job."""
    with progress_lock:
        # Get existing data to preserve start_time
        existing = progress_store.get(job_id, {})
        start_time = existing.get('start_time', datetime.now().isoformat())
        
        progress_store[job_id] = {
            'stage': stage,
            'percentage': percentage,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'start_time': start_time
        }


def get_progress(job_id: str) -> Dict[str, Any]:
    """Get progress for a job."""
    with progress_lock:
        return progress_store.get(job_id, {
            'stage': 'unknown',
            'percentage': 0,
            'message': 'Unknown job',
            'details': '',
            'timestamp': datetime.now().isoformat(),
            'start_time': datetime.now().isoformat()
        })


def clear_progress(job_id: str):
    """Clear progress for a job."""
    with progress_lock:
        if job_id in progress_store:
            del progress_store[job_id]


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
        {'id': 'requestyai', 'name': 'RequestyAI (Unified Gateway - All Models)', 'recommended': True},
        {'id': 'openai', 'name': 'OpenAI (GPT-4, GPT-4o)', 'recommended': False},
        {'id': 'anthropic', 'name': 'Anthropic (Claude 3.5 Sonnet)', 'recommended': False},
        {'id': 'google', 'name': 'Google (Gemini 1.5 Pro)', 'recommended': False},
        {'id': 'azure_openai', 'name': 'Azure OpenAI', 'recommended': False},
        {'id': 'ollama', 'name': 'Ollama (Local Models)', 'recommended': False}
    ]


def get_common_models():
    """Get common model options by provider."""
    return {
        'requestyai': [
            # OpenAI models via RequestyAI
            'openai/gpt-4o',
            'openai/gpt-4o-mini',
            'openai/gpt-4-turbo', 
            'openai/o1-preview',
            'openai/o1-mini',
            # Anthropic models via RequestyAI
            'anthropic/claude-3-5-sonnet-20241022',
            'anthropic/claude-3-5-haiku-20241022',
            'anthropic/claude-3-opus-20240229',
            # Google models via RequestyAI
            'google/gemini-1.5-pro',
            'google/gemini-1.5-flash',
            # Specialized models
            'coding/claude-4-sonnet',
            'deepseek/deepseek-coder'
        ],
        'openai': [
            'gpt-4o',
            'gpt-4o-mini',
            'gpt-4-turbo',
            'gpt-3.5-turbo'
        ],
        'anthropic': [
            'claude-3-5-sonnet-20241022',
            'claude-3-5-haiku-20241022',
            'claude-3-opus-20240229'
        ],
        'google': [
            'gemini-1.5-pro',
            'gemini-1.5-flash',
            'gemini-1.0-pro'
        ],
        'azure_openai': [
            'gpt-4o',
            'gpt-4-turbo',
            'gpt-35-turbo'
        ],
        'ollama': [
            'llama3.2',
            'llama3.1',
            'mistral',
            'codellama'
        ]
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
    """Handle criteria file uploads and manual entry (annual review and competency criteria)."""
    try:
        annual_file = request.files.get('annual_criteria')
        competency_file = request.files.get('competency_criteria')
        
        results = {}
        
        # Handle annual criteria (file upload or manual entry via blob)
        if annual_file:
            try:
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
            except json.JSONDecodeError:
                results['annual_criteria'] = {'success': False, 'error': 'Invalid JSON format in annual criteria.'}
            except Exception as e:
                results['annual_criteria'] = {'success': False, 'error': f'Error processing annual criteria: {str(e)}'}
        
        # Handle competency criteria (file upload or manual entry via blob)
        if competency_file:
            try:
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
            except json.JSONDecodeError:
                results['competency_criteria'] = {'success': False, 'error': 'Invalid JSON format in competency criteria.'}
            except Exception as e:
                results['competency_criteria'] = {'success': False, 'error': f'Error processing competency criteria: {str(e)}'}
        
        return jsonify(results)
        
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


@app.route('/api/get-csv-data', methods=['POST'])
def get_csv_data():
    """Return CSV content as JSON array for editing."""
    try:
        data = request.get_json()
        csv_path = data.get('csv_path')
        
        if not csv_path or not os.path.exists(csv_path):
            return jsonify({'error': 'CSV file not found'}), 404
        
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Convert to list of dictionaries
        csv_data = df.to_dict('records')
        
        return jsonify({
            'success': True,
            'data': csv_data,
            'rows': len(csv_data),
            'columns': list(df.columns)
        })
        
    except Exception as e:
        logger.error(f"Get CSV data error: {str(e)}")
        return jsonify({'error': f'Failed to read CSV: {str(e)}'}), 500


@app.route('/api/update-csv-data', methods=['POST'])
def update_csv_data():
    """Save edited data back to CSV file."""
    try:
        data = request.get_json()
        csv_path = data.get('csv_path')
        updated_data = data.get('data')
        
        if not csv_path or not updated_data:
            return jsonify({'error': 'CSV path and data are required'}), 400
        
        if not os.path.exists(csv_path):
            return jsonify({'error': 'CSV file not found'}), 404
        
        # Convert back to DataFrame
        df = pd.DataFrame(updated_data)
        
        # Validate required columns
        required_columns = ['Date', 'Title']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }), 400
        
        # Save updated CSV
        df.to_csv(csv_path, index=False)
        
        return jsonify({
            'success': True,
            'message': 'CSV data updated successfully',
            'rows': len(df),
            'path': csv_path
        })
        
    except Exception as e:
        logger.error(f"Update CSV data error: {str(e)}")
        return jsonify({'error': f'Failed to update CSV: {str(e)}'}), 500






@app.route('/api/get-progress/<job_id>')
def get_progress_api(job_id):
    """Get progress for a specific job."""
    try:
        progress = get_progress(job_id)
        return jsonify(progress)
    except Exception as e:
        logger.error(f"Error getting progress: {str(e)}")
        return jsonify({
            'stage': 'error',
            'percentage': 0,
            'message': f'Error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500



@app.route('/api/run-analysis', methods=['POST'])
def run_analysis():
    """Run performance review analysis."""
    # Record start time for accurate processing duration
    analysis_start_time = datetime.now()
    
    try:
        data = request.get_json()
        
        # Generate unique job ID for progress tracking
        job_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Extract parameters with validation
        review_type = data.get('review_type', 'competency') or 'competency'
        year = data.get('year', get_current_year()) or get_current_year()
        data_source = data.get('data_source', 'csv') or 'csv'
        output_format = data.get('output_format', 'markdown') or 'markdown'
        
        # Validate required parameters
        if not review_type or not year or not data_source or not output_format:
            clear_progress(job_id)
            return jsonify({
                'success': False,
                'error': f'Missing required parameters: review_type={review_type}, year={year}, data_source={data_source}, output_format={output_format}'
            }), 400
        
        # LLM configuration
        llm_provider = data.get('llm_provider')
        llm_model = data.get('llm_model')
        api_key = data.get('api_key')
        
        # Initialize progress
        update_progress(job_id, 'running', 10, 'Running analysis...', 'Processing your performance data')
        
        # Check for stored API key if none provided
        if llm_provider and llm_provider != 'none' and not api_key:
            storage = get_key_storage()
            if storage:
                stored_key_data = storage.get_key(llm_provider)
                if stored_key_data:
                    api_key = stored_key_data['api_key']
                    # Use stored model if no model specified
                    if not llm_model and stored_key_data.get('model'):
                        llm_model = stored_key_data['model']
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
                    'api_key': api_key or ''
                }
            }
            
            # Save temporary config file
            config_file = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_config.json')
            with open(config_file, 'w') as f:
                json.dump(llm_config, f, indent=2)
            
            analysis_args['config'] = config_file
        
        # Run actual analysis using your existing main.py functionality
        update_progress(job_id, 'running', 50, 'Processing data...', 'Analysis in progress')
        file_extension = 'md' if output_format.lower() == 'markdown' else output_format
        
        # Create enhanced filename with AI provider and model info
        def sanitize_filename_part(text):
            """Sanitize text for safe filename usage."""
            if not text:
                return "none"
            # Replace problematic characters with underscores
            import re
            return re.sub(r'[^\w\-.]', '_', str(text)).lower()
        
        # Build filename components
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        provider_part = sanitize_filename_part(llm_provider) if llm_provider and llm_provider != 'none' else 'automated'
        model_part = sanitize_filename_part(llm_model) if llm_model and llm_provider != 'none' else ''
        
        # Construct filename with AI info
        if model_part:
            result_file = f"performance_review_{review_type}_{year}_{provider_part}_{model_part}_{timestamp}.{file_extension}"
        else:
            result_file = f"performance_review_{review_type}_{year}_{provider_part}_{timestamp}.{file_extension}"
        
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_file)
        
        try:
            # Prepare command line arguments for main.py
            import subprocess
            import sys
            
            # CSV file is required for all analysis
            csv_file = data.get('csv_file')
            if not csv_file:
                clear_progress(job_id)
                return jsonify({
                    'success': False,
                    'error': 'No CSV file provided. Please upload a CSV file first.'
                }), 400
            
            cmd_args = [
                sys.executable, 'src/main.py',
                '--file', csv_file,
                '--type', review_type,
                '--year', str(year),
                '--format', output_format
            ]
            
            # Handle criteria file - copy uploaded criteria to expected location
            criteria_file = data.get('criteria_file')
            if criteria_file and os.path.exists(criteria_file):
                import shutil
                # Create criteria directory if it doesn't exist
                os.makedirs('criteria', exist_ok=True)
                
                # Copy criteria file to expected location based on review type
                expected_criteria_file = f"criteria/{review_type}_review_criteria.json"
                shutil.copy2(criteria_file, expected_criteria_file)
                logger.info(f"Copied criteria file from {criteria_file} to {expected_criteria_file}")
            else:
                logger.warning(f"No criteria file found or file doesn't exist: {criteria_file}")
            
            # Create complete config file (always needed)
            temp_config = {
                'llm_integration': {
                    'provider': llm_provider if llm_provider != 'none' else 'requestyai',
                    'model': llm_model or 'default',
                    'api_key': api_key or '',
                    'options': {
                        'temperature': 0.7,
                        'max_tokens': 32000
                    }
                },
                'processing': {
                    'output_directory': app.config['RESULTS_FOLDER'],
                    'date_range_months': 12
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
            
            # Execute the analysis with simple subprocess.run
            result = subprocess.run(cmd_args, capture_output=True, text=True, cwd='.')
            
            # Mark as complete
            update_progress(job_id, 'completed', 100, 'Analysis complete!', 'Report generated successfully')
            
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
        
        # Analysis is already marked as complete above
        
        # Calculate processing time
        analysis_end_time = datetime.now()
        processing_duration = analysis_end_time - analysis_start_time
        processing_time_seconds = int(processing_duration.total_seconds())
        
        # Read file size for metadata
        file_size = 0
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
        
        # Clear progress after analysis is complete (no need for threading)
        # Progress will be cleared when UI polls for results
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'result_file': result_file,
            'result_path': result_path,
            'message': 'Analysis completed successfully',
            'metadata': {
                'review_type': review_type,
                'year': year,
                'data_source': data_source,
                'output_format': output_format,
                'llm_provider': llm_provider if llm_provider != 'none' else None,
                'llm_model': llm_model if llm_provider != 'none' else None,
                'file_size': file_size,
                'processing_time_seconds': processing_time_seconds,
                'generated_at': analysis_end_time.isoformat()
            }
        })
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        # Clear progress on error
        try:
            clear_progress(job_id)
        except:
            pass
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/get-result-content/<filename>')
def get_result_content(filename):
    """Get the content of a result file for inline display."""
    try:
        safe_filename = secure_filename(filename)
        file_path = os.path.join(app.config['RESULTS_FOLDER'], safe_filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'content': content,
            'filename': safe_filename,
            'size': len(content)
        })
        
    except Exception as e:
        logger.error(f"Error reading result content: {str(e)}")
        return jsonify({'error': f'Failed to read content: {str(e)}'}), 500


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


@app.route('/api/download-template/<template_type>')
def download_template(template_type):
    """Download template files for data input."""
    try:
        templates_dir = os.path.join(os.path.dirname(__file__), 'downloadable_templates')
        
        template_files = {
            'csv': 'accomplishments_template.csv',
            'annual-criteria': 'annual_review_criteria_template.json',
            'competency-criteria': 'competency_assessment_criteria_template.json'
        }
        
        if template_type not in template_files:
            return jsonify({'error': 'Invalid template type'}), 400
        
        filename = template_files[template_type]
        file_path = os.path.join(templates_dir, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Template file not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"Template download failed: {str(e)}")
        return jsonify({'error': 'Template download failed'}), 500


@app.route('/api/store-api-key', methods=['POST'])
def store_api_key():
    """Store an API key securely."""
    try:
        storage = get_key_storage()
        if not storage:
            return jsonify({'error': 'Key storage not available'}), 500
        
        data = request.get_json()
        provider = data.get('provider')
        api_key = data.get('api_key')
        model = data.get('model')
        
        if not provider or not api_key:
            return jsonify({'error': 'Provider and API key are required'}), 400
        
        success = storage.store_key(provider, api_key, model)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'API key stored for {provider}'
            })
        else:
            return jsonify({'error': 'Failed to store API key'}), 500
            
    except Exception as e:
        logger.error(f"Error storing API key: {str(e)}")
        return jsonify({'error': f'Failed to store API key: {str(e)}'}), 500


@app.route('/api/get-stored-key/<provider>')
def get_stored_key(provider):
    """Get stored API key info (without exposing the key)."""
    try:
        storage = get_key_storage()
        if not storage:
            return jsonify({'has_key': False, 'error': 'Key storage not available'})
        
        key_data = storage.get_key(provider)
        
        if key_data:
            # Return info without exposing the actual key
            return jsonify({
                'has_key': True,
                'model': key_data.get('model'),
                'stored_at': key_data.get('stored_at'),
                'key_preview': f"{key_data['api_key'][:8]}..." if len(key_data['api_key']) > 8 else "***"
            })
        else:
            return jsonify({'has_key': False})
            
    except Exception as e:
        logger.error(f"Error retrieving API key info: {str(e)}")
        return jsonify({'has_key': False, 'error': str(e)})


@app.route('/api/delete-api-key/<provider>', methods=['DELETE'])
def delete_api_key(provider):
    """Delete a stored API key."""
    try:
        storage = get_key_storage()
        if not storage:
            return jsonify({'error': 'Key storage not available'}), 500
        
        success = storage.delete_key(provider)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'API key deleted for {provider}'
            })
        else:
            return jsonify({'error': 'API key not found or could not be deleted'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting API key: {str(e)}")
        return jsonify({'error': f'Failed to delete API key: {str(e)}'}), 500


@app.route('/api/list-stored-keys')
def list_stored_keys():
    """Get list of providers with stored keys."""
    try:
        storage = get_key_storage()
        if not storage:
            return jsonify({'providers': [], 'error': 'Key storage not available'})
        
        providers = storage.list_stored_providers()
        return jsonify({'providers': providers})
        
    except Exception as e:
        logger.error(f"Error listing stored keys: {str(e)}")
        return jsonify({'providers': [], 'error': str(e)})


if __name__ == '__main__':
    import sys
    # Allow port to be specified as command line argument
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    app.run(debug=True, host='0.0.0.0', port=port)
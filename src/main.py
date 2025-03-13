#!/usr/bin/env python3
"""
Main script for the Performance Review Tracking System.

This script provides end-to-end automation for generating performance review reports,
including data processing, Roo Code analysis, and report generation.
"""

import argparse
import json
import os
import sys
import subprocess
from datetime import datetime
from typing import Optional, Union
import pandas as pd
from docx import Document
import markdown
from markdown.extensions import fenced_code, tables
import site

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Site packages: {site.getsitepackages()}")

# Data processor functions
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from CSV or Excel file.
    """
    print("DEBUG: load_data - START", file_path) # DEBUG LOG
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()
    try:
        if file_ext == '.csv':
            print("DEBUG: load_data - Loading CSV", file_path) # DEBUG LOG
            df = pd.read_csv(file_path)
            print("DEBUG: load_data - CSV loaded successfully", file_path) # DEBUG LOG
            return df
        elif file_ext in ['.xlsx', '.xls']:
            print("DEBUG: load_data - Loading Excel", file_path) # DEBUG LOG
            df = pd.read_excel(file_path)
            print("DEBUG: load_data - Excel loaded successfully", file_path) # DEBUG LOG
            return df
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    except Exception as e:
        print(f"DEBUG: load_data - ERROR loading data: {str(e)}") # DEBUG LOG
        raise ValueError(f"Error loading data from {file_path}: {str(e)}")

    print("DEBUG: load_data - END") # DEBUG LOG


def filter_by_date_range(
    data: pd.DataFrame,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime]
) -> pd.DataFrame:
    """
    Filter entries by date range for Annual Review.
    """
    print("DEBUG: filter_by_date_range - START", start_date, end_date) # DEBUG LOG
    if 'Date' not in data.columns:
        raise ValueError("DataFrame must contain a 'Date' column")

    # Make a copy to avoid modifying the original
    filtered_data = data.copy()

    # Try to convert dates to datetime, with error handling
    try:
        filtered_data['Date'] = pd.to_datetime(filtered_data['Date'], errors='raise')
    except Exception as e:
        raise ValueError(f"Invalid date format in data: {str(e)}")

    # Convert string dates to datetime if needed
    if isinstance(start_date, str):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid start date format: {start_date}. Use YYYY-MM-DD")

    if isinstance(end_date, str):
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid end date format: {end_date}. Use YYYY-MM-DD")

    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    # Filter by date range
    mask = filtered_data['Date'].between(start_ts, end_ts)
    print("DEBUG: filter_by_date_range - END") # DEBUG LOG
    return filtered_data[mask].reset_index(drop=True)


def validate_data(data: pd.DataFrame) -> None:
    """
    Validate the structure and content of the input data.
    """
    print("DEBUG: validate_data - START") # DEBUG LOG
    required_columns = [
        'Date',
        'Title',
        'Description',
        'Acceptance Criteria',
        'Success Notes',
        'Impact'
    ]

    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Check for empty descriptions
    empty_descriptions = data['Description'].isnull() | (data['Description'].astype(str).str.strip() == '')
    if empty_descriptions.any():
        raise ValueError("Found entries with empty descriptions")

    # Validate Impact values
    valid_impacts = ['High', 'Medium', 'Low']
    invalid_impacts = data[~data['Impact'].isin(valid_impacts)]['Impact'].unique()
    if len(invalid_impacts) > 0:
        raise ValueError(
            f"Invalid Impact values found: {', '.join(map(str, invalid_impacts))}. "
            f"Valid values are: {', '.join(valid_impacts)}"
        )
    print("DEBUG: validate_data - END") # DEBUG LOG


def prepare_data_for_analysis(
    data: pd.DataFrame,
    review_type: str,
    year: Optional[str] = None,
    output_dir: str = 'data'
) -> str:
    """
    Prepare data for Roo Code analysis.
    """
    print("DEBUG: prepare_data_for_analysis - START", review_type, year, output_dir) # DEBUG LOG
    # Validate review type
    if review_type.lower() not in ['annual', 'competency']:
        raise ValueError(
            "Invalid review type. Must be either 'annual' or 'competency'"
        )

    # Check if data is empty (after header)
    if len(data) == 0:
        raise ValueError("No data found in the input file")

    # Validate and prepare data
    validate_data(data)

    # Always try to convert 'Date' column to datetime for consistency
    try:
        data['Date'] = pd.to_datetime(data['Date'], errors='raise')
    except Exception as e:
        raise ValueError(f"Invalid date format in data: {str(e)}")

    if review_type.lower() == 'annual':
        if not year:
            raise ValueError("Year is required for annual reviews")

        # Annual review covers Sept to Aug
        start_date = f"{int(year)-1}-09-01"
        end_date = f"{year}-08-31"
        data = filter_by_date_range(data, start_date, end_date)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Convert to JSON format for Roo Code
    output_path = os.path.join(output_dir, f"processed_{review_type.lower()}.json")

    # Convert dates to ISO format strings for JSON serialization
    # First ensure we have datetime type in the Date column
    if hasattr(data['Date'], 'dt'):
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    else:
        # If somehow we don't have datetime objects, try a safe conversion
        data['Date'] = data['Date'].apply(lambda x: x.strftime('%Y-%m-%d') if hasattr(x, 'strftime') else str(x))

    # Save to file for Roo Code to access
    print(f"DEBUG: prepare_data_for_analysis - Saving processed data to: {output_path}") # DEBUG LOG
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json.loads(data.to_json(orient='records')), f, indent=2)
    except Exception as e:
        print(f"DEBUG: prepare_data_for_analysis - ERROR saving JSON: {str(e)}") # DEBUG LOG
        raise
    print(f"DEBUG: prepare_data_for_analysis - Saved processed data to: {output_path}") # DEBUG LOG
    print("DEBUG: prepare_data_for_analysis - END", output_path) # DEBUG LOG
    return output_path

# Report generator functions
def load_template(review_type):
    """
    Load the appropriate review template.
    """
    print("DEBUG: load_template - START", review_type) # DEBUG LOG
    if review_type == "competency":
        template_path = f"templates/competency_assessment_template.md"
    else:
        template_path = f"templates/annual_review_template.md"
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    print("DEBUG: load_template - END", template_path) # DEBUG LOG
    return template_content

def load_analysis(file_path):
    """
    Load the analysis generated by Roo Code.
    """
    print("DEBUG: load_analysis - START", file_path) # DEBUG LOG
    analysis_path = file_path.replace('processed_', 'analyzed_').replace('.json', '.md')

    if not os.path.exists(analysis_path):
        raise FileNotFoundError(
            f"Analysis file not found: {analysis_path}\n\n"
            "Please complete these steps first:\n"
            "1. Open VS Code\n"
            "2. Switch to Performance Analyst mode\n"
            f"3. Use the command: @{file_path} Please analyze this data and generate a structured report\n"
            "4. Save Roo Code's analysis to: " + analysis_path
        )

    with open(analysis_path, 'r', encoding='utf-8') as f:
        analyzed_content = f.read()
    print("DEBUG: load_analysis - Content read from analysis file:\n", analyzed_content) # DEBUG LOG
    print("DEBUG: load_analysis - END", analysis_path) # DEBUG LOG
    return analyzed_content

def markdown_to_docx(markdown_text, output_path):
    """
    Convert markdown formatted text to a DOCX document.
    """
    print("DEBUG: markdown_to_docx - START", output_path) # DEBUG LOG
    if not markdown_text.strip():
        raise ValueError("Markdown text cannot be empty")

    # Create new Document
    doc = Document()

    # Process markdown line by line
    in_list = False
    lines = markdown_text.split('\n')

    for line in lines:
        line = line.rstrip()
        if not line:
            # Empty line
            continue

        # Check for headers
        if line.startswith('# '):
            doc.add_heading(line[2:], level=1)
        elif line.startswith('## '):
            doc.add_heading(line[3:], level=2)
        elif line.startswith('### '):
            doc.add_heading(line[4:], level=3)
        # Check for list items
        elif line.startswith('- '):
            if not in_list:
                in_list = True
            doc.add_paragraph(line[2:], style='List Bullet')
        # Regular paragraph
        else:
            in_list = False
            doc.add_paragraph(line)

    # Save the document
    print(f"DEBUG: markdown_to_docx - Saving DOCX to: {output_path}") # DEBUG LOG
    doc.save(output_path)
    print("DEBUG: markdown_to_docx - END", output_path) # DEBUG LOG
    return output_path

def generate_final_report(data_file, review_type, output_format='markdown', output_path=None):
    """
    Generate final formatted report by combining Roo Code analysis with template.
    """
    print("DEBUG: generate_final_report - START", data_file, review_type, output_format, output_path) # DEBUG LOG
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    current_year = datetime.now().year

    # If no output path is specified, create a default one
    if not output_path:
        output_path = f"output/{review_type.lower()}_review_{timestamp}.{'md' if output_format.lower() == 'markdown' else 'docx'}"

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    try:
        # Load Roo Code's analysis
        analyzed_content = load_analysis(data_file)
        print("DEBUG: generate_final_report - Loaded analysis content:\n", analyzed_content) # DEBUG LOG

        # Load and apply the template
        template = load_template(review_type)
        
        # For annual review, modify the year and date range
        if review_type.lower() == 'annual':
            # Replace [Year] with the current year
            template = template.replace('[Year]', str(current_year))
            # Replace date range
            template = template.replace('[September 1, YYYY - August 31, YYYY]',
                                    f'[September 1, {current_year-1} - August 31, {current_year}]')
        
        # Handle empty analysis content
        if not analyzed_content.strip():
            analyzed_content = "No accomplishments found in the specified date range."
        
        # Format the template with the analyzed content
        report_content = template.format(analyzed_content=analyzed_content)
        print("DEBUG: generate_final_report - Report content after template formatting:\n", report_content) # DEBUG LOG

        if output_format.lower() == 'markdown':
            print(f"DEBUG: generate_final_report - Saving markdown report to: {output_path}") # DEBUG LOG
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"DEBUG: generate_final_report - Saved markdown report to: {output_path}") # DEBUG LOG
        elif output_format.lower() == 'docx':
            # If output path is for a docx, but we need a temporary md file
            if output_path.endswith('.docx'):
                md_path = output_path.replace('.docx', '.md')
            else:
                md_path = f"{output_path}.md"

            # Save markdown version
            print(f"DEBUG: generate_final_report - Saving temporary markdown for DOCX conversion to: {md_path}") # DEBUG LOG
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"DEBUG: generate_final_report - Saved temporary markdown for DOCX conversion to: {md_path}") # DEBUG LOG

            # Convert to DOCX
            docx_path = output_path if output_path.endswith('.docx') else f"{output_path}.docx"
            markdown_to_docx(report_content, docx_path)
            output_path = docx_path

            # Clean up temporary markdown file if it was just for conversion
            if md_path != output_path and os.path.exists(md_path):
                os.remove(md_path)

    except NotImplementedError as e:
        # Pass through the Roo Code usage instructions
        raise NotImplementedError(str(e))
    except Exception as e:
        print(f"DEBUG: generate_final_report - ERROR: {str(e)}") # DEBUG LOG
        raise ValueError(f"Error generating report: {str(e)}")

    print("DEBUG: generate_final_report - END", output_path) # DEBUG LOG
    return output_path


def run_roo_code_analysis(data_file: str, review_type: str) -> str:
    """
    Run Roo Code analysis on the processed data.
    """
    print("DEBUG: run_roo_code_analysis - START", data_file, review_type) # DEBUG LOG
    # Determine output path for the analysis
    analysis_path = data_file.replace('processed_', 'analyzed_').replace('.json', '.md')

    # Create a detailed prompt based on review type
    if review_type.lower() == 'annual':
        prompt = (f"@{data_file} Please analyze this data to generate an Annual Review report. "
                 "Follow the exact format from the system prompt, with separate sections for each criterion: "
                 "1. Communication, 2. Flexibility, 3. Initiative, 4. Member Service, "
                 "5. Personal Credibility, 6. Quality and Quantity of Work, 7. Teamwork, "
                 "and an Overall Summary. For each criterion, include 'How I Met This Criterion', "
                 "'Areas for Improvement', 'Improvement Plan', and 'Summary' sections.")
    else:
        prompt = (f"@{data_file} Please analyze this data to generate a Competency Assessment report. "
                 "Follow the exact format from the system prompt, with separate sections for each criterion.")

    # Prepare the Roo Code command
    roo_command = [
        'code', '--cli',  # Use VS Code CLI mode
        '--execute-command', 'roo.sendMessage',  # Execute Roo Code command
        '--args', prompt  # Detailed prompt
    ]

    try:
        # Run Roo Code analysis
        print("DEBUG: run_roo_code_analysis - Running Roo Code analysis subprocess...") # DEBUG LOG
        result = subprocess.run(roo_command, capture_output=True, text=True, check=True) # Capture output here
        print("DEBUG: run_roo_code_analysis - Roo Code analysis subprocess completed") # DEBUG LOG
        
        # Log stdout and stderr
        print("DEBUG: run_roo_code_analysis - Roo Code stdout:\n", result.stdout) # DEBUG LOG
        print("DEBUG: run_roo_code_analysis - Roo Code stderr:\n", result.stderr) # DEBUG LOG


        # Save Roo Code's output to the analysis file
        print(f"DEBUG: run_roo_code_analysis - Saving analysis to: {analysis_path}") # DEBUG LOG
        with open(analysis_path, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        print(f"DEBUG: run_roo_code_analysis - Saved analysis to: {analysis_path}") # DEBUG LOG

        print(f"DEBUG: run_roo_code_analysis - Analysis completed and saved to {analysis_path}") # DEBUG LOG
        print("DEBUG: run_roo_code_analysis - END", analysis_path) # DEBUG LOG
        return analysis_path

    except subprocess.CalledProcessError as e:
        print(f"DEBUG: run_roo_code_analysis - Roo Code analysis failed (subprocess.CalledProcessError): {e.stderr}") # DEBUG LOG
        raise RuntimeError(f"Roo Code analysis failed: {e.stderr}")
    except Exception as e:
        print(f"DEBUG: run_roo_code_analysis - Error running Roo Code analysis: {str(e)}") # DEBUG LOG
        raise RuntimeError(f"Error running Roo Code analysis: {str(e)}")


def generate_review(
    input_file: str,
    review_type: str,
    year: Optional[str] = None,
    output_format: str = 'markdown',
    output_path: Optional[str] = None
) -> str:
    """
    Generate a performance review report from start to finish.
    """
    print("DEBUG: generate_review - START", input_file, review_type, year, output_format, output_path) # DEBUG LOG
    try:
        # 1. Load and process data
        print(f"DEBUG: generate_review - Loading data from {input_file}...") # DEBUG LOG
        data = load_data(input_file)
        print(f"DEBUG: generate_review - Data loaded successfully from {input_file}") # DEBUG LOG

        print("DEBUG: generate_review - Processing data...") # DEBUG LOG
        processed_data_path = prepare_data_for_analysis(
            data,
            review_type,
            year,
            'data'  # Output directory
        )
        print(f"DEBUG: generate_review - Data processed and saved to {processed_data_path}") # DEBUG LOG

        # 2. Run Roo Code analysis
        analysis_path = run_roo_code_analysis(processed_data_path, review_type)

        # 3. Generate final report
        print("DEBUG: generate_review - Generating final report...") # DEBUG LOG
        report_path = generate_final_report(
            processed_data_path,
            review_type,
            output_format,
            output_path
        )
        print(f"DEBUG: generate_review - Report generated successfully at: {report_path}") # DEBUG LOG

        print("DEBUG: generate_review - END", report_path) # DEBUG LOG
        return report_path

    except ValueError as e:
        print(f"DEBUG: generate_review - ValueError: {str(e)}") # DEBUG LOG
        print(f"Error: Invalid input - {str(e)}", file=sys.stderr)
        raise
    except RuntimeError as e:
        print(f"DEBUG: generate_review - RuntimeError: {str(e)}") # DEBUG LOG
        print(f"Error: Process failed - {str(e)}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"DEBUG: generate_review - Unexpected Exception: {str(e)}") # DEBUG LOG
        print(f"Error: Unexpected error - {str(e)}", file=sys.stderr)
        raise


def main():
    """Main function to orchestrate the review generation process."""
    parser = argparse.ArgumentParser(
        description="Generate performance review reports",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  Generate an annual review report:
    %(prog)s --file data/accomplishments.csv --type annual --year 2025 --format docx

  Generate a competency assessment report:
    %(prog)s --file data/accomplishments.csv --type competency --format markdown
        """
    )

    # Add arguments
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the data file (CSV or Excel)"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["annual", "competency"],
        help="Type of review (annual or competency)"
    )
    parser.add_argument(
        "--year",
        help="Year for annual review (required for annual review type)"
    )
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "docx"],
        help="Output format (markdown or docx)"
    )
    parser.add_argument(
        "--output",
        help="Custom output path for the generated report"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.type == "annual" and not args.year:
        parser.error("--year is required for annual reviews")

    try:
        # Generate the review
        report_path = generate_review(
            args.file,
            args.type,
            args.year,
            args.format,
            args.output
        )
        print(f"\nReview generation complete! The report is available at: {report_path}")
        return 0

    except Exception as e:
        print("\nReview generation failed. Please check the error messages above.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
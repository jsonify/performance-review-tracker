"""
Integration tests for the performance review system.
"""

import os
import json
import pytest
import subprocess
from docx import Document
from src.data_processor import load_data, prepare_data_for_analysis
from src.report_generator import load_roo_code_output, generate_final_report

# Sample data for testing
SAMPLE_DATA = [
    {
        'Date': '2024-10-15',
        'Title': 'Task 1',
        'Description': 'Description 1',
        'Acceptance Criteria': 'Criteria 1',
        'Success Notes': 'Notes 1',
        'Impact': 'High'
    },
    {
        'Date': '2024-12-20',
        'Title': 'Task 2',
        'Description': 'Description 2',
        'Acceptance Criteria': 'Criteria 2',
        'Success Notes': 'Notes 2',
        'Impact': 'Medium'
    },
    {
        'Date': '2025-02-10',
        'Title': 'Task 3',
        'Description': 'Description 3',
        'Acceptance Criteria': 'Criteria 3',
        'Success Notes': 'Notes 3',
        'Impact': 'Low'
    }
]

@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for testing."""
    csv_path = tmp_path / "sample_data.csv"
    with open(csv_path, 'w') as f:
        f.write("Date,Title,Description,Acceptance Criteria,Success Notes,Impact\n")
        for row in SAMPLE_DATA:
            f.write(f"{row['Date']},{row['Title']},{row['Description']},{row['Acceptance Criteria']},{row['Success Notes']},{row['Impact']}\n")
    return csv_path

def test_end_to_end_annual_review(tmp_path, sample_csv):
    """Test the end-to-end workflow for annual review."""
    # 1. Process data
    data_processor_script = "src/data_processor.py"
    review_type = "annual"
    year = "2025"
    output_path = tmp_path / "processed_annual.json"

    command = [
        "python", data_processor_script,
        "--file", str(sample_csv),
        "--type", review_type,
        "--year", year
    ]
    subprocess.run(command, check=True, cwd=".")
    assert os.path.exists(output_path)

    # 2. Generate report using dummy Roo Code output (replace with actual Roo Code integration later)
    report_generator_script = "src/report_generator.py"
    roo_output_path = tmp_path / "roo_output.md"
    roo_output_path.write_text("# Roo Code Output\nThis is a sample output from Roo Code.")

    output_format = "markdown"
    final_report_path = tmp_path / "annual_review_report.md"

    command = [
        "python", report_generator_script,
        "--input", str(roo_output_path),
        "--type", review_type,
        "--format", output_format
    ]
    subprocess.run(command, check=True, cwd=tmp_path)
    assert os.path.exists(final_report_path)

    # 3. Validate output content (basic check)
    with open(final_report_path, "r") as f:
        report_content = f.read()
        assert "Roo Code Output" in report_content

def test_end_to_end_competency_assessment(tmp_path, sample_csv):
    """Test the end-to-end workflow for competency assessment."""
    # 1. Process data
    data_processor_script = "src/data_processor.py"
    review_type = "competency"
    output_path = tmp_path / "processed_competency.json"

    command = [
        "python", data_processor_script,
        "--file", str(sample_csv),
        "--type", review_type,
    ]
    subprocess.run(command, check=True, cwd=tmp_path)
    assert os.path.exists(output_path)

    # 2. Generate report using dummy Roo Code output (replace with actual Roo Code integration later)
    report_generator_script = "src/report_generator.py"
    roo_output_path = tmp_path / "roo_output.md"
    roo_output_path.write_text("# Roo Code Output\nThis is a sample output from Roo Code.")

    output_format = "docx"
    final_report_path = tmp_path / "competency_assessment_report.docx"

    command = [
        "python", report_generator_script,
        "--input", str(roo_output_path),
        "--type", review_type,
        "--format", output_format
    ]
    subprocess.run(command, check=True, cwd=".")
    assert os.path.exists(final_report_path)

    # 3. Validate output content (basic check)
    doc = Document(final_report_path)
    report_content = "\n".join([p.text for p in doc.paragraphs])
    assert "Roo Code Output" in report_content
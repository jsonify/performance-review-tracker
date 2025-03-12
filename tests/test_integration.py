import pytest
import subprocess
import re
from docx import Document
from typing import List, Dict, Union
from src.validation import validate_report, load_criteria

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

    # 3. Validate output content and format
    criteria_file = "criteria/annual_review_criteria.json"
    criteria = load_criteria(criteria_file)
    is_valid, issues = validate_report(str(final_report_path), criteria_file)
    assert is_valid, f"Report should be valid. Issues: {issues}"

    with open(final_report_path, "r") as f:
        report_content = f.read()

    # Check basic content
    assert "Roo Code Output" in report_content

    # Validate data inclusion
    for task in SAMPLE_DATA:
        assert task["Title"] in report_content, f"Missing task: {task['Title']}"
        assert task["Impact"] in report_content, f"Missing impact level: {task['Impact']}"

def test_edge_cases(tmp_path):
    """Test handling of edge cases and error conditions."""
    # Test with empty CSV
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("Date,Title,Description,Acceptance Criteria,Success Notes,Impact\n")

    # Should handle empty input gracefully
    data_processor_script = "src/data_processor.py"
    command = [
        "python", data_processor_script,
        "--file", str(empty_csv),
        "--type", "annual",
        "--year", "2025"
    ]
    process = subprocess.run(command, capture_output=True, text=True)
    assert process.returncode != 0, "Should fail with empty input"
    assert "No data found" in process.stderr or "No data found" in process.stdout

    # Test with invalid dates
    invalid_csv = tmp_path / "invalid.csv"
    invalid_csv.write_text(
        "Date,Title,Description,Acceptance Criteria,Success Notes,Impact\n"
        "invalid-date,Task 1,Desc,Criteria,Notes,High\n"
    )
    process = subprocess.run(
        ["python", data_processor_script, "--file", str(invalid_csv), "--type", "annual", "--year", "2025"],
        capture_output=True, text=True
    )
    assert process.returncode != 0, "Should fail with invalid date"
    assert "Invalid date format" in process.stderr or "Invalid date format" in process.stdout

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

    # 3. Validate output content and format
    criteria_file = "criteria/competency_assessment_criteria.json"
    criteria = load_criteria(criteria_file)
    is_valid, issues = validate_report(str(final_report_path), criteria_file)
    assert is_valid, f"Report should be valid. Issues: {issues}"

    doc = Document(final_report_path)
    report_content = "\n".join([p.text for p in doc.paragraphs])

    # Check basic content
    assert "Roo Code Output" in report_content

    # Validate document structure
    assert len(doc.sections) > 0, "Document should have at least one section"
    assert len(doc.paragraphs) > 0, "Document should have content"

    # Validate data inclusion
    for task in SAMPLE_DATA:
        task_found = any(task["Title"] in p.text for p in doc.paragraphs)
        assert task_found, f"Missing task: {task['Title']}"
        impact_found = any(task["Impact"] in p.text for p in doc.paragraphs)
        assert impact_found, f"Missing impact level: {task['Impact']}"

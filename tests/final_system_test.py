"""
Final system tests for the Performance Review Tracking System.
Tests the complete workflow with realistic data volumes and edge cases.
"""

import os
import shutil
import pytest
import pandas as pd
from datetime import datetime, timedelta
from src.main import (
    load_data,
    prepare_data_for_analysis,
    generate_final_report,
    generate_review
)

@pytest.fixture
def test_env(tmp_path):
    """Set up test environment with required directories and templates"""
    # Create test directories
    data_dir = tmp_path / "data"
    template_dir = tmp_path / "templates"
    output_dir = tmp_path / "output"
    
    os.makedirs(data_dir)
    os.makedirs(template_dir)
    os.makedirs(output_dir)
    
    # Copy templates from project's main templates directory
    project_root = os.path.dirname(os.path.dirname(__file__))
    shutil.copy(
        os.path.join(project_root, "templates", "annual_review_template.md"),
        template_dir / "annual_review_template.md"
    )
    shutil.copy(
        os.path.join(project_root, "templates", "competency_assessment_template.md"),
        template_dir / "competency_assessment_template.md"
    )
    
    return {
        "data_dir": data_dir,
        "template_dir": template_dir,
        "output_dir": output_dir
    }

def generate_test_data(num_entries=50):
    """Generate realistic test data with varied scenarios"""
    data = []
    start_date = datetime(2024, 9, 1)  # Start of review period
    impacts = ["High", "Medium", "Low"]
    
    for i in range(num_entries):
        entry_date = start_date + timedelta(days=i*7)  # Spread entries weekly
        data.append({
            "Date": entry_date.strftime("%Y-%m-%d"),
            "Title": f"Test Accomplishment {i+1}",
            "Description": f"Detailed description of accomplishment {i+1} with specific metrics and outcomes",
            "Acceptance Criteria": f"Measurable criteria for accomplishment {i+1}",
            "Success Notes": f"Documentation of success for accomplishment {i+1}",
            "Impact": impacts[i % 3]
        })
    return pd.DataFrame(data)

@pytest.fixture
def large_test_data(test_env):
    """Create a large test dataset"""
    data = generate_test_data(50)
    file_path = test_env["data_dir"] / "large_accomplishments.csv"
    data.to_csv(file_path, index=False)
    return file_path

def test_system_performance(test_env, large_test_data):
    """Test system performance with large dataset"""
    # Load and process large dataset
    data = pd.read_csv(large_test_data)
    assert len(data) >= 50, "Large dataset not loaded correctly"
    
    # Test processing time for annual review
    start_time = datetime.now()
    
    # Point to test template directory
    os.environ["TEMPLATE_DIR"] = str(test_env["template_dir"])
    
    output_path = generate_review(
        str(large_test_data),
        "annual",
        "2025",
        "markdown",
        os.path.join(test_env["output_dir"], "annual_review.md")
    )
    processing_time = (datetime.now() - start_time).total_seconds()
    
    # Assert processing completes within reasonable time
    assert processing_time < 30, f"Data processing took too long: {processing_time} seconds"
    assert os.path.exists(output_path), "Output file not created"

def test_report_formats(test_env, large_test_data):
    """Test generation of all supported report formats"""
    formats = ["markdown", "docx"]
    
    # Point to test template directory
    os.environ["TEMPLATE_DIR"] = str(test_env["template_dir"])
    
    for fmt in formats:
        output_path = generate_review(
            str(large_test_data),
            "annual",
            "2025",
            fmt,
            os.path.join(test_env["output_dir"], f"annual_review.{fmt}")
        )
        assert os.path.exists(output_path), f"Failed to generate {fmt} report"
        
        if fmt == "docx":
            # Additional checks for DOCX format
            from docx import Document
            doc = Document(output_path)
            assert len(doc.paragraphs) > 0, "DOCX report is empty"

def test_error_handling(test_env):
    """Test system's error handling capabilities"""
    os.environ["TEMPLATE_DIR"] = str(test_env["template_dir"])
    
    # Test nonexistent file
    with pytest.raises(FileNotFoundError):
        generate_review(
            "nonexistent_file.csv",
            "annual",
            "2025",
            "markdown",
            os.path.join(test_env["output_dir"], "error_test.md")
        )
    
    # Test invalid review type
    with pytest.raises(ValueError):
        data = generate_test_data(1)
        file_path = test_env["data_dir"] / "bad_type.csv"
        data.to_csv(file_path, index=False)
        generate_review(
            str(file_path),
            "invalid_type",
            "2025",
            "markdown",
            os.path.join(test_env["output_dir"], "error_test.md")
        )
    
    # Test missing year for annual review
    with pytest.raises(ValueError):
        data = generate_test_data(1)
        file_path = test_env["data_dir"] / "missing_year.csv"
        data.to_csv(file_path, index=False)
        generate_review(
            str(file_path),
            "annual",
            None,
            "markdown",
            os.path.join(test_env["output_dir"], "error_test.md")
        )

def test_edge_cases(test_env):
    """Test handling of edge cases"""
    os.environ["TEMPLATE_DIR"] = str(test_env["template_dir"])
    
    # Test empty description
    edge_data = pd.DataFrame([{
        "Date": "2024-10-15",
        "Title": "Empty Description",
        "Description": "",
        "Acceptance Criteria": "Test criteria",
        "Success Notes": "Test notes",
        "Impact": "High"
    }])
    
    file_path = test_env["data_dir"] / "edge_cases.csv"
    edge_data.to_csv(file_path, index=False)
    
    with pytest.raises(ValueError):
        generate_review(
            str(file_path),
            "annual",
            "2025",
            "markdown",
            os.path.join(test_env["output_dir"], "edge_test.md")
        )
    
    # Test future dates
    future_data = pd.DataFrame([{
        "Date": "2026-01-01",
        "Title": "Future Task",
        "Description": "Task in future",
        "Acceptance Criteria": "Test criteria",
        "Success Notes": "Test notes",
        "Impact": "High"
    }])
    
    file_path = test_env["data_dir"] / "future_data.csv"
    future_data.to_csv(file_path, index=False)
    
    output_path = generate_review(
        str(file_path),
        "annual",
        "2025",
        "markdown",
        os.path.join(test_env["output_dir"], "future_test.md")
    )
    
    # Check that future dates are handled appropriately
    with open(output_path, 'r') as f:
        content = f.read()
        assert "No accomplishments found" in content or not content.strip(), \
            "Future dates should be filtered out or result in empty report"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
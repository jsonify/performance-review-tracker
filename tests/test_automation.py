"""
Test script for the automated performance review generation.
"""

import os
import pytest
from src.main import generate_review, load_data, prepare_data_for_analysis

def test_annual_review_generation():
    """Test generating an annual review report."""
    input_file = "data/accomplishments.csv"
    review_type = "annual"
    year = "2025"
    output_format = "markdown"
    
    # Ensure input file exists
    assert os.path.exists(input_file), f"Test file not found: {input_file}"
    
    try:
        # Generate the review
        output_path = generate_review(
            input_file=input_file,
            review_type=review_type,
            year=year,
            output_format=output_format
        )
        
        # Check that output file was created
        assert os.path.exists(output_path), f"Output file not created: {output_path}"
        
        # Verify file content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content, "Generated file is empty"
            assert "# Annual Review" in content, "Missing review header"
        
    except Exception as e:
        pytest.fail(f"Review generation failed: {str(e)}")

def test_competency_assessment_generation():
    """Test generating a competency assessment report."""
    input_file = "data/accomplishments.csv"
    review_type = "competency"
    output_format = "markdown"
    
    # Ensure input file exists
    assert os.path.exists(input_file), f"Test file not found: {input_file}"
    
    try:
        # Generate the review
        output_path = generate_review(
            input_file=input_file,
            review_type=review_type,
            output_format=output_format
        )
        
        # Check that output file was created
        assert os.path.exists(output_path), f"Output file not created: {output_path}"
        
        # Verify file content
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert content, "Generated file is empty"
            assert "# Competency Assessment" in content, "Missing assessment header"
        
    except Exception as e:
        pytest.fail(f"Review generation failed: {str(e)}")

def test_docx_output_format():
    """Test generating a report in DOCX format."""
    input_file = "data/accomplishments.csv"
    review_type = "annual"
    year = "2025"
    output_format = "docx"
    
    try:
        # Generate the review
        output_path = generate_review(
            input_file=input_file,
            review_type=review_type,
            year=year,
            output_format=output_format
        )
        
        # Check that output file was created
        assert os.path.exists(output_path), f"Output file not created: {output_path}"
        assert output_path.endswith('.docx'), "Output file is not in DOCX format"
        
    except Exception as e:
        pytest.fail(f"DOCX generation failed: {str(e)}")

def test_invalid_inputs():
    """Test error handling for invalid inputs."""
    with pytest.raises(ValueError):
        # Test missing year for annual review
        generate_review(
            input_file="data/accomplishments.csv",
            review_type="annual",
            output_format="markdown"
        )
    
    with pytest.raises(FileNotFoundError):
        # Test non-existent input file
        generate_review(
            input_file="data/nonexistent.csv",
            review_type="competency",
            output_format="markdown"
        )
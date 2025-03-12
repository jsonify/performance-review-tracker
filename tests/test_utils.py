"""
Tests for utils.py module.
"""

import pytest
from src.utils import validate_criteria_coverage, check_report_completeness, validate_report_structure

def test_validate_criteria_coverage_valid():
    """Test criteria coverage validation with valid data."""
    data = [
        {"Date": "2024-01-01", "Title": "Implemented feature A", "Description": "This feature demonstrates excellent communication skills."},
        {"Date": "2024-01-02", "Title": "Resolved bug B", "Description": "This bug fix demonstrates problem-solving skills."}
    ]
    criteria = ["Communication", "Problem-Solving"]
    validate_criteria_coverage(data, criteria)  # Should not raise any exceptions

def test_validate_criteria_coverage_invalid():
    """Test criteria coverage validation with invalid data (missing criteria)."""
    data = [
        {"Date": "2024-01-01", "Title": "Implemented feature A", "Description": "This feature demonstrates excellent communication skills."},
        {"Date": "2024-01-02", "Title": "Resolved bug B", "Description": "This bug fix does not demonstrate problem-solving skills."}
    ]
    criteria = ["Communication", "Problem-Solving", "Teamwork"]
    with pytest.raises(ValueError, match="The following criteria are not covered in the data: Teamwork"):
        validate_criteria_coverage(data, criteria)

def test_check_report_completeness_valid():
    """Test report completeness check with a valid report."""
    report = """
    # Communication
    
    ## Expectations
    - Clear communication
    
    ## How I Met This Criterion
    - Implemented feature A
    
    ## Areas for Improvement
    - None
    
    ## Improvement Plan
    - Continue to communicate clearly
    
    ## Summary
    Excellent communication skills.
    """
    check_report_completeness(report)  # Should not raise any exceptions

def test_check_report_completeness_invalid():
    """Test report completeness check with an invalid report (missing section)."""
    report = """
    # Communication
    
    ## Expectations
    - Clear communication
    
    ## How I Met This Criterion
    - Implemented feature A
    
    ## Areas for Improvement
    - None
    
    ## Improvement Plan
    - Continue to communicate clearly
    """
    with pytest.raises(ValueError, match="The report is incomplete. Missing section: Summary"):
        check_report_completeness(report)

def test_validate_report_structure_valid():
    """Test report structure validation with a valid report."""
    report = """
    # Communication
    
    ## Expectations
    - Clear communication
    
    ## How I Met This Criterion
    - Implemented feature A
    
    ## Areas for Improvement
    - None
    
    ## Improvement Plan
    - Continue to communicate clearly
    
    ## Summary
    Excellent communication skills.
    """
    validate_report_structure(report)  # Should not raise any exceptions

def test_validate_report_structure_invalid():
    """Test report structure validation with an invalid report (not a string)."""
    report = 123
    with pytest.raises(TypeError, match="Report must be a string."):
        validate_report_structure(report)

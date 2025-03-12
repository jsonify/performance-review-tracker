"""
Utility functions for the performance review system.
"""

import json
import logging
from datetime import datetime

def validate_criteria_coverage(data, criteria):
    """
    Validate that all criteria are covered in the data.
    """
    covered_criteria = set()
    for entry in data:
        for criterion in criteria:
            if criterion.lower() in entry['Description'].lower() or criterion.lower() in entry['Title'].lower():
                covered_criteria.add(criterion)
    
    uncovered_criteria = set(criteria) - covered_criteria
    if uncovered_criteria:
        raise ValueError(f"The following criteria are not covered in the data: {', '.join(uncovered_criteria)}")

def check_report_completeness(report):
    """
    Check that the report is complete and contains all required sections.
    """
    required_sections = ["Expectations", "How I Met This Criterion", "Areas for Improvement", "Improvement Plan", "Summary"]
    for section in required_sections:
        if section not in report:
            raise ValueError(f"The report is incomplete. Missing section: {section}")

def validate_report_structure(report):
    """
    Validate the structure of the report.
    """
    # Add more detailed structure validation here
    if not isinstance(report, str):
        raise TypeError("Report must be a string.")

# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Example data
    data = [
        {"Date": "2024-01-01", "Title": "Implemented feature A", "Description": "This feature demonstrates excellent communication skills."},
        {"Date": "2024-01-02", "Title": "Resolved bug B", "Description": "This bug fix demonstrates problem-solving skills."}
    ]
    
    # Example criteria
    criteria = ["Communication", "Problem-Solving"]
    
    # Example report
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
    
    try:
        validate_criteria_coverage(data, criteria)
        logging.info("Criteria coverage validation passed.")
        
        check_report_completeness(report)
        logging.info("Report completeness check passed.")
        
        validate_report_structure(report)
        logging.info("Report structure validation passed.")
        
    except ValueError as e:
        logging.error(f"Validation error: {e}")
    except TypeError as e:
        logging.error(f"Type error: {e}")

"""
Validation tools for performance review reports.
"""

import json
import re
from typing import List, Dict, Union, Tuple
from docx import Document

def load_criteria(criteria_file: str) -> List[Dict[str, Union[str, List[str]]]]:
    """Load criteria definitions from JSON file."""
    try:
        with open(criteria_file, "r") as f:
            return json.load(f)["criteria"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading criteria file: {e}")

def validate_criteria_coverage(content: str, criteria: List[Dict[str, Union[str, List[str]]]]) -> List[str]:
    """
    Check if all required criteria are covered in the report.
    Returns a list of missing criteria, empty if all criteria are covered.
    """
    missing = []
    for criterion in criteria:
        name = criterion["name"]
        if name not in content:
            missing.append(name)
        else:
            # Check if at least one expectation is mentioned
            expectations = criterion["expectations"]
            expectations_found = any(exp in content for exp in expectations)
            if not expectations_found:
                missing_expectations = [exp for exp in expectations if exp not in content]
                missing.append(f"{name} (missing expectations: {', '.join(missing_expectations)})")
    return missing

def validate_report_structure(content: str) -> List[str]:
    """
    Validate the structural elements of a report.
    Returns a list of structural issues found.
    """
    issues = []
    
    # Check for required headers
    if not content.startswith("# "):
        issues.append("Missing main title (should start with #)")
    
    # Check for required sections
    required_sections = ["Summary", "Accomplishments", "Areas for Improvement"]
    for section in required_sections:
        if not re.search(rf"## {section}", content):
            issues.append(f"Missing required section: {section}")
    
    # Check for empty sections
    if re.search(r"##\s*\n##", content):
        issues.append("Found empty sections")
    
    # Check for proper markdown hierarchy
    if re.search(r"###[^#].*\n##[^#]", content):
        issues.append("Incorrect header hierarchy")
    
    return issues

def validate_content_completeness(content: str) -> List[str]:
    """
    Check for completeness of report content.
    Returns a list of content-related issues.
    """
    issues = []
    
    # Check for minimum content length (300 characters is about 50 words)
    if len(content.strip()) < 300:
        issues.append("Report seems too short (less than 300 characters)")
    
    # Check for impact statements
    if not re.search(r"impact", content, re.IGNORECASE):
        issues.append("No mention of impact in report")
    
    # Check for accomplishment details
    if not re.search(r"accomplish", content, re.IGNORECASE):
        issues.append("No mention of accomplishments")
    
    return issues

def validate_report(report_path: str, criteria_file: str) -> Tuple[bool, List[str]]:
    """
    Validate a performance review report for completeness and proper structure.
    Returns (is_valid, list_of_issues).
    """
    # Load criteria
    criteria = load_criteria(criteria_file)
    
    # Read report content
    if report_path.endswith(".md"):
        with open(report_path, "r") as f:
            content = f.read()
    elif report_path.endswith(".docx"):
        doc = Document(report_path)
        content = "\n".join([p.text for p in doc.paragraphs])
    else:
        return False, ["Unsupported file format"]
    
    # Collect all validation issues
    issues = []
    issues.extend(validate_report_structure(content))
    issues.extend(validate_content_completeness(content))
    issues.extend(validate_criteria_coverage(content, criteria))
    
    return len(issues) == 0, issues

def generate_validation_report(report_path: str, criteria_file: str) -> str:
    """
    Generate a detailed validation report in markdown format.
    """
    is_valid, issues = validate_report(report_path, criteria_file)
    
    report_lines = ["# Report Validation Results\n"]
    
    if is_valid:
        report_lines.append("✅ Report passed all validation checks!\n")
    else:
        report_lines.append("❌ Report has validation issues:\n")
        for issue in issues:
            report_lines.append(f"- {issue}")
    
    return "\n".join(report_lines)

"""
Validation tools for performance review reports.
"""

import json
import re
import os
from typing import List, Dict, Union, Tuple, Any
from docx import Document

def load_criteria(criteria_file: str) -> List[Dict[str, Union[str, List[str]]]]:
    """Load criteria definitions from JSON file."""
    try:
        with open(criteria_file, "r") as f:
            data = json.load(f)
            return data["criteria"]
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
        expectations = criterion["expectations"]
        
        # Check if criterion name is mentioned in the content
        name_found = re.search(r'(?i)' + re.escape(name), content)
        if not name_found:
            missing.append(name)
            continue
        
        # Get all significant words (length > 3) from expectations
        expectation_words = set()
        for expectation in expectations:
            words = re.findall(r'\b\w+\b', expectation.lower())
            expectation_words.update(word for word in words if len(word) > 3)
        
        # Check if a sufficient number of expectation words are present
        content_lower = content.lower()
        words_found = sum(1 for word in expectation_words if word in content_lower)
        
        # Require at least 25% of the significant words to be present
        if words_found < len(expectation_words) * 0.25:
            missing.append(name)
    
    return missing

def validate_report_structure(content: str) -> List[str]:
    """
    Validate the structural elements of a report.
    Returns a list of structural issues found.
    """
    issues = []
    
    # Check for required headers
    if not re.search(r'^#\s+', content, re.MULTILINE):
        issues.append("Missing main title (should start with #)")
    
    # Check for required sections - more flexibly match section headings
    required_sections = ["Summary", "Accomplishments", "Areas for Improvement"]
    for section in required_sections:
        if not re.search(rf'(?i)##\s+.*{section}|##\s+{section}', content):
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

def extract_text_from_docx(docx_path: str) -> str:
    """Extract all text from a DOCX file."""
    try:
        doc = Document(docx_path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {e}")

def validate_report(report_path: str, criteria_file: str) -> Tuple[bool, List[str]]:
    """
    Validate a performance review report for completeness and proper structure.
    Returns (is_valid, list_of_issues).
    """
    # Check if files exist
    if not os.path.exists(report_path):
        return False, [f"Report file not found: {report_path}"]
    
    if not os.path.exists(criteria_file):
        # We need to raise ValueError for the test_edge_cases test
        raise ValueError(f"Error loading criteria file: Criteria file not found: {criteria_file}")
    
    # Load criteria
    try:
        criteria = load_criteria(criteria_file)
    except ValueError as e:
        raise ValueError(f"Error loading criteria file: {e}")
    
    # Read report content
    try:
        if report_path.endswith(".md"):
            with open(report_path, "r") as f:
                content = f.read()
        elif report_path.endswith(".docx"):
            content = extract_text_from_docx(report_path)
        else:
            return False, ["Unsupported file format"]
    except Exception as e:
        return False, [f"Error reading report file: {e}"]
    
    # Collect all validation issues
    structure_issues = validate_report_structure(content)
    content_issues = validate_content_completeness(content)
    criteria_issues = validate_criteria_coverage(content, criteria)
    
    # Combine all issues
    all_issues = structure_issues + content_issues
    if criteria_issues:
        all_issues.append("Missing criteria: " + ", ".join(criteria_issues))
    
    return len(all_issues) == 0, all_issues

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

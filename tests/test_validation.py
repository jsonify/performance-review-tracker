"""
Tests for the report validation tools.
"""

import os
import pytest
from src.validation import (
    load_criteria,
    validate_criteria_coverage,
    validate_report_structure,
    validate_content_completeness,
    validate_report,
    generate_validation_report
)

@pytest.fixture
def sample_criteria():
    return [
        {
            "name": "Communication",
            "expectations": [
                "Gives members full attention during meetings",
                "Expresses ideas clearly and in an organized way"
            ]
        },
        {
            "name": "Initiative",
            "expectations": [
                "Self-directed in completing major projects",
                "Takes on additional responsibilities and initiatives"
            ]
        }
    ]

@pytest.fixture
def criteria_file(tmp_path, sample_criteria):
    """Create a sample criteria file for testing."""
    criteria_file = tmp_path / "test_criteria.json"
    with open(criteria_file, "w") as f:
        f.write('{"criteria": ' + str(sample_criteria).replace("'", '"') + '}')
    return criteria_file

@pytest.fixture
def valid_report_content():
    return """# Performance Review 2025

## Summary
Demonstrated strong performance across all key areas, showing excellent communication skills and initiative throughout the year.

## Accomplishments
- Led team communication initiatives, consistently expressing ideas clearly and giving members full attention during meetings
- Demonstrated strong initiative by being self-directed in completing major projects and taking on additional responsibilities
- Generated high impact on team productivity through effective communication and proactive problem-solving
- Successfully completed multiple high-priority deliverables ahead of schedule
- Mentored junior team members, sharing knowledge and best practices
- Implemented process improvements that increased team efficiency by 25%

## Areas for Improvement
Some areas to focus on in the coming year:
- Continue developing advanced communication techniques for complex projects
- Look for more opportunities to take initiative in cross-team collaborations
- Further enhance project documentation practices

## Additional Notes
- Received positive feedback from team members and stakeholders
- Consistently met or exceeded performance expectations
- Demonstrated strong alignment with company values
"""

@pytest.fixture
def invalid_report_content():
    return """Some content without proper structure.
No headers, no sections, just text."""

def test_validate_criteria_coverage(sample_criteria, valid_report_content, invalid_report_content):
    # Test with valid content
    missing = validate_criteria_coverage(valid_report_content, sample_criteria)
    assert len(missing) == 0, "Valid report should cover all criteria"
    
    # Test with invalid content
    missing = validate_criteria_coverage(invalid_report_content, sample_criteria)
    assert len(missing) == 2, "Should find 2 missing criteria"
    assert "Communication" in missing[0] or "Initiative" in missing[0]

def test_validate_report_structure(valid_report_content, invalid_report_content):
    # Test with valid content
    issues = validate_report_structure(valid_report_content)
    assert len(issues) == 0, "Valid report should have no structural issues"
    
    # Test with invalid content
    issues = validate_report_structure(invalid_report_content)
    assert len(issues) > 0, "Invalid report should have structural issues"
    assert any("Missing main title" in issue for issue in issues)
    assert any("Missing required section" in issue for issue in issues)

def test_validate_content_completeness(valid_report_content, invalid_report_content):
    # Test with valid content
    issues = validate_content_completeness(valid_report_content)
    assert len(issues) == 0, "Valid report should have no content issues"
    
    # Test with invalid content
    issues = validate_content_completeness(invalid_report_content)
    assert len(issues) > 0, "Invalid report should have content issues"
    assert any("impact" in issue.lower() for issue in issues)
    assert any("accomplish" in issue.lower() for issue in issues)

def test_validate_report(tmp_path, valid_report_content, criteria_file):
    # Create test files
    valid_report = tmp_path / "valid_report.md"
    with open(valid_report, "w") as f:
        f.write(valid_report_content)
    
    invalid_report = tmp_path / "invalid_report.txt"
    with open(invalid_report, "w") as f:
        f.write("Invalid file format")
    
    # Test validation
    is_valid, issues = validate_report(str(valid_report), str(criteria_file))
    assert is_valid, "Valid report should pass validation"
    assert len(issues) == 0, "Valid report should have no issues"
    
    # Test invalid format
    is_valid, issues = validate_report(str(invalid_report), str(criteria_file))
    assert not is_valid, "Invalid format should fail validation"
    assert "Unsupported file format" in issues, f"Unexpected issues: {issues}"

def test_generate_validation_report(tmp_path, valid_report_content, criteria_file):
    # Create test files
    report_file = tmp_path / "report.md"
    with open(report_file, "w") as f:
        f.write(valid_report_content)

    # Test report generation
    validation_report = generate_validation_report(str(report_file), str(criteria_file))
    assert "# Report Validation Results" in validation_report, "Report header missing"
    assert "✅ Report passed all validation checks!" in validation_report, "Success message missing"

def test_edge_cases(tmp_path, criteria_file):
    """Test edge cases and error conditions."""
    # Test empty file
    empty_file = tmp_path / "empty.md"
    empty_file.write_text("")

    is_valid, issues = validate_report(str(empty_file), str(criteria_file))
    assert not is_valid, "Empty report should not be valid"
    assert any("Missing main title" in issue for issue in issues), "Missing title not detected"

    # Test missing criteria file
    valid_report = tmp_path / "report.md"
    valid_report.write_text("# Title\n\n## Summary\nContent")

    with pytest.raises(ValueError) as excinfo:
        validate_report(str(valid_report), "nonexistent.json")
    assert "Error loading criteria file" in str(excinfo.value)

def test_docx_report(tmp_path, valid_report_content, criteria_file):
    """Test validation of a .docx report."""
    docx_report = tmp_path / "valid_report.docx"
    document = Document()
    for paragraph in valid_report_content.splitlines():
        document.add_paragraph(paragraph)
    document.save(docx_report)

    is_valid, issues = validate_report(str(docx_report), str(criteria_file))
    assert is_valid, "Valid docx report should pass validation"
    assert not issues, f"Unexpected issues: {issues}"

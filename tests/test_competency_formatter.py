"""
Tests for the competency assessment formatter.
"""

import os
import pytest
from src.competency_formatter import CompetencyFormatter

@pytest.fixture
def formatter():
    return CompetencyFormatter()

@pytest.fixture
def sample_competency():
    return {
        "name": "Programming/Software Development",
        "rating": 4,
        "evidence": [
            "Developed Jenkins pipeline reducing deployment time from 2 hours to 15 minutes",
            "Created Python ETL pipeline improving processing efficiency by 85%",
            "Implemented automated testing framework achieving 95% coverage"
        ],
        "rating_definition": "Takes technical responsibility across all stages and iterations of software development",
        "achievements": [
            "Automated critical deployment processes",
            "Significantly improved data processing efficiency",
            "Enhanced quality through test automation"
        ],
        "impact": ("These improvements have had substantial business impact, reducing operational costs "
                  "while improving reliability and scalability. The automated systems now handle "
                  "critical business processes with minimal manual intervention, allowing the team "
                  "to focus on strategic initiatives."),
        "growth": ("Demonstrated progression from individual contributor to technical leader, "
                  "regularly sharing knowledge and mentoring team members on best practices.")
    }

def test_format_evidence(formatter):
    evidence = [
        "First evidence item",
        "Second evidence item"
    ]
    result = formatter.format_evidence(evidence)
    assert result.startswith("- First")
    assert "- Second" in result
    assert result.count("- ") == 2

def test_format_evidence_empty(formatter):
    result = formatter.format_evidence([])
    assert result == "*No evidence provided*"

def test_format_justification(formatter):
    result = formatter.format_justification(
        rating=4,
        rating_definition="test definition",
        achievements=["achievement 1", "achievement 2"],
        impact="test impact",
        growth="test growth"
    )
    
    # Check paragraphs
    paragraphs = result.split("\n\n")
    assert len(paragraphs) == 4
    assert paragraphs[0].startswith("Based on")
    assert "4/5" in paragraphs[0]
    assert "achievement 1" in paragraphs[1]
    assert paragraphs[2] == "test impact"
    assert paragraphs[3] == "test growth"

def test_format_justification_no_growth(formatter):
    result = formatter.format_justification(
        rating=3,
        rating_definition="test definition",
        achievements=["achievement"],
        impact="test impact"
    )
    
    # Check paragraphs
    paragraphs = result.split("\n\n")
    assert len(paragraphs) == 3
    assert "growth" not in result

def test_format_competency(formatter, sample_competency):
    result = formatter.format_competency(**sample_competency)
    
    # Check main sections
    assert "## Programming/Software Development" in result
    assert "### Rating: 4/5" in result
    assert "### Evidence" in result
    assert "### Justification" in result
    
    # Check content
    assert "Jenkins pipeline" in result
    assert "These improvements" in result
    assert "Demonstrated progression" in result

def test_generate_report(formatter, sample_competency):
    summary = "Test summary"
    result = formatter.generate_report(summary=summary, competencies=[sample_competency])
    
    # Check structure
    assert result.startswith("# Competency Assessment Report")
    assert "## Summary" in result
    assert summary in result
    assert "## Programming/Software Development" in result

def test_markdown_formatting(formatter, sample_competency):
    """Test that Markdown formatting is preserved and proper."""
    result = formatter.generate_report(
        summary="Test",
        competencies=[sample_competency]
    )
    
    # Check header levels
    assert result.count("# ") == 1  # Main title
    assert result.count("## ") >= 2  # Summary and at least one competency
    assert result.count("### ") >= 3  # Rating, Evidence, and Justification sections
    
    # Check list formatting
    assert result.count("- ") >= 3  # Evidence items
    
    # Check spacing
    assert "\n\n" in result  # Proper paragraph spacing
    assert "---" in result  # Section separators

def test_save_report(formatter, sample_competency, tmp_path):
    """Test saving report to file."""
    output_file = tmp_path / "test_report.md"
    report = formatter.generate_report(
        summary="Test summary",
        competencies=[sample_competency]
    )
    
    with open(output_file, "w") as f:
        f.write(report)
        
    assert os.path.exists(output_file)
    with open(output_file) as f:
        content = f.read()
        assert content == report
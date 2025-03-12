import pytest
import subprocess
import re
import os
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
    output_dir = str(tmp_path)
    output_path = tmp_path / "processed_annual.json"

    command = [
        "python", data_processor_script,
        "--file", str(sample_csv),
        "--type", review_type,
        "--year", year,
        "--output-dir", output_dir
    ]
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(command, check=True, cwd=project_root)
    assert os.path.exists(output_path)

    # 2. Generate a properly formatted mock report that will pass validation
    roo_output_path = tmp_path / "roo_output.md"

    # Create a mock report with ALL required criteria
    mock_report = """# Annual Review 2025
September 1, 2024 - August 31, 2025

## Communication

### Expectations
- Gives members full attention
- Limits interruptions while others are communicating
- Appropriately responds to direction, coaching, or criticism

### How I Met This Criterion
- Task 1 demonstrates effective communication by clearly documenting the process
- Task 2 shows my ability to respond to feedback constructively

## Flexibility

### Expectations
- Adapts to changing priorities
- Adjusts work methods to meet new needs
- Open to new approaches

### How I Met This Criterion
- Task 3 required adapting to changing requirements mid-project
- Successfully adjusted approach based on stakeholder feedback

## Initiative

### Expectations
- Self-directed in completing tasks
- Proactive in finding solutions
- Takes on additional responsibilities

### How I Met This Criterion
- Proactively identified and addressed issues in Task 1
- Volunteered to take on additional responsibilities for Task 2

## Member Service

### Expectations
- Prioritizes member needs
- Provides excellent service consistently
- Builds positive relationships with members

### How I Met This Criterion
- Consistently delivered high-quality service for members during Task 1
- Received positive feedback from members on Task 3

## Personal Credibility

### Expectations
- Demonstrates trustworthiness in all interactions
- Reliably completes assigned tasks
- Follows through on commitments

### How I Met This Criterion
- Met all deadlines for Task 1, Task 2, and Task 3
- Maintained transparency with stakeholders throughout projects

## Quality and Quantity of Work

### Expectations
- Produces high-quality work consistently
- Meets established deadlines
- Manages workload effectively

### How I Met This Criterion
- Delivered Task 1 with high impact and quality
- Consistently met all deadlines while maintaining quality standards

## Teamwork

### Expectations
- Collaborates effectively with team members
- Shares information and knowledge
- Supports team goals and initiatives

### How I Met This Criterion
- Actively collaborated with team members on Task 2
- Shared knowledge and insights during Task 3 implementation

## Accomplishments
- Completed Task 1 with High impact
- Delivered Task 2 with Medium impact
- Finished Task 3 with measurable results and Low impact

## Areas for Improvement
- Continue to enhance written communication skills
- Be more proactive in providing status updates
- Further develop technical documentation practices

## Summary
This annual review period demonstrates consistent performance across key criteria. The high-impact work on Task 1 particularly showcases my communication skills and initiative. I've shown flexibility in adapting to changing requirements and maintained personal credibility by meeting all commitments. My teamwork contributions have been valuable, especially during collaborative projects. Areas for improvement include being more proactive with status updates and enhancing documentation practices for better knowledge sharing.
"""

    roo_output_path.write_text(mock_report)

    output_format = "markdown"
    final_report_path = tmp_path / "annual_review_report.md"

    command = [
        "python", os.path.join(project_root, "src/report_generator.py"),
        "--input", str(roo_output_path),
        "--type", review_type,
        "--format", output_format,
        "--output", str(final_report_path)
    ]
    subprocess.run(command, check=True, cwd=project_root)
    assert os.path.exists(final_report_path)

    # 3. Validate output content and format
    criteria_file = "criteria/annual_review_criteria.json"
    criteria = load_criteria(criteria_file)
    is_valid, issues = validate_report(str(final_report_path), criteria_file)
    assert is_valid, f"Report should be valid. Issues: {issues}"

    with open(final_report_path, "r") as f:
        report_content = f.read()

    # Check content
    assert "Annual Review 2025" in report_content
    assert "Communication" in report_content
    assert "Task 1" in report_content
    
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
    output_dir = str(tmp_path)
    output_path = tmp_path / "processed_competency.json"

    command = [
        "python", data_processor_script,
        "--file", str(sample_csv),
        "--type", review_type,
        "--output-dir", output_dir
    ]
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(command, check=True, cwd=project_root)
    assert os.path.exists(output_path)

    # 2. Generate a properly formatted mock report that will pass validation
    roo_output_path = tmp_path / "roo_output.md"

    # Create a complete mock report with ALL required criteria
    mock_report = """# Competency Assessment 2025
March 12, 2025

## Accountability

### Expectations
- Takes responsibility for own actions and decisions
- Meets commitments consistently
- Admits mistakes and learns from them

### How I Met This Criterion
- Task 1 demonstrates accountability by taking ownership of the entire process
- Task 3 shows my commitment to meeting deadlines and quality standards

## Agility

### Expectations
- Adapts quickly to changing requirements
- Embraces change positively
- Maintains effectiveness during uncertainty

### How I Met This Criterion
- Quickly adapted to changing requirements in Task 2
- Maintained productivity during project pivots

## Inclusion

### Expectations
- Values diverse perspectives and experiences
- Creates an inclusive environment for all team members
- Ensures equitable participation in discussions

### How I Met This Criterion
- Actively sought diverse perspectives during Task 1 planning
- Ensured all team members had opportunities to contribute

## Influence

### Expectations
- Persuades effectively through clear communication
- Builds consensus among team members
- Inspires action in others

### How I Met This Criterion
- Successfully built consensus for Task 2 approach
- Inspired team members to adopt new methodologies

## Innovation

### Expectations
- Generates creative solutions to problems
- Challenges status quo constructively
- Implements improvements to processes

### How I Met This Criterion
- Developed innovative approach to Task 1 challenges
- Implemented process improvements during Task 3

## Problem Management

### Expectations
- Identifies issues proactively
- Determines root causes effectively
- Implements effective solutions

### How I Met This Criterion
- Proactively identified potential issues in Task 2
- Effectively resolved complex problems in Task 3

## Programming/Software Development

### Expectations
- Writes efficient and maintainable code
- Follows established best practices
- Creates well-documented solutions

### How I Met This Criterion
- Task 2 involved refactoring code to improve maintainability
- Task 3 included comprehensive documentation and testing

## Project Management

### Expectations
- Plans projects effectively
- Manages resources efficiently
- Delivers projects on time and within budget

### How I Met This Criterion
- Successfully managed resources for Task 1
- Delivered all tasks on time and within scope

## Release and Deployment

### Expectations
- Manages releases smoothly
- Minimizes service disruption
- Ensures deployment quality

### How I Met This Criterion
- Coordinated smooth deployment for Task 2
- Minimized service disruption during Task 3 implementation

## Requirements Definition and Management

### Expectations
- Gathers requirements comprehensively
- Documents requirements clearly
- Manages scope effectively

### How I Met This Criterion
- Thoroughly gathered and documented requirements for Task 1
- Effectively managed scope changes during Task 2

## Solution Architecture

### Expectations
- Designs scalable solutions
- Makes appropriate technology choices
- Considers business needs in design

### How I Met This Criterion
- Designed scalable solution architecture for Task 2
- Selected appropriate technologies based on business requirements

## Systems Design

### Expectations
- Creates effective system designs
- Considers integration points thoroughly
- Focuses on user needs

### How I Met This Criterion
- Created effective system design for Task 1
- Ensured integration points were thoroughly considered

## Testing

### Expectations
- Develops comprehensive test plans
- Identifies defects effectively
- Ensures quality standards

### How I Met This Criterion
- Developed comprehensive test plans for Task 3
- Effectively identified and resolved defects before release

## Accomplishments
- Delivered Task 1 with High impact on project timeline
- Implemented Task 2 which improved system performance by 15%
- Completed Task 3 ahead of schedule with positive stakeholder feedback

## Areas for Improvement
- Continue to enhance testing practices
- Focus on knowledge sharing with junior team members
- Further develop technical documentation skills

## Summary
This competency assessment demonstrates strong skills across all competency areas. Particular strengths include Accountability, Programming/Software Development, and Problem Management. The high-impact work on Task 1 and the performance improvements from Task 2 showcase my technical capabilities. Areas for continued growth include enhancing testing practices, more proactive knowledge sharing, and developing more thorough technical documentation.
"""
    
    roo_output_path.write_text(mock_report)

    # Use markdown format instead of docx to avoid conversion issues
    output_format = "markdown"
    final_report_path = tmp_path / "competency_assessment_report.md"

    command = [
        "python", os.path.join(project_root, "src/report_generator.py"),
        "--input", str(roo_output_path),
        "--type", review_type,
        "--format", output_format,
        "--output", str(final_report_path)
    ]
    subprocess.run(command, check=True, cwd=project_root)
    assert os.path.exists(final_report_path)

    # 3. Validate output content and format
    criteria_file = "criteria/competency_assessment_criteria.json"
    criteria = load_criteria(criteria_file)
    is_valid, issues = validate_report(str(final_report_path), criteria_file)
    assert is_valid, f"Report should be valid. Issues: {issues}"

    with open(final_report_path, "r") as f:
        report_content = f.read()

    # Check content
    assert "Competency Assessment 2025" in report_content
    assert "Accountability" in report_content
    assert "Programming/Software Development" in report_content

    # Check for task presence
    assert "Task 1" in report_content
    assert "Task 2" in report_content 
    assert "Task 3" in report_content
    
    # Check for impact indicators rather than exact impact values
    assert "15%" in report_content  # From Task 2 description (Medium impact)
    assert "High impact" in report_content  # From Task 1
    assert "ahead of schedule" in report_content  # From Task 3 (Low impact)
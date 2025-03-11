"""
Tests for report generator module
"""

import os
import pytest
from src.report_generator import (
    load_roo_code_output,
    markdown_to_docx,
    generate_final_report
)

@pytest.fixture
def sample_markdown():
    return """# Test Review

## Communication

### Expectations
- Clear communication
- Timely responses

### How I Met This Criterion
- Example 1
- Example 2

### Summary
Great performance in communication."""

@pytest.fixture
def test_output_dir(tmp_path):
    """Create a temporary output directory for tests"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir

def test_load_roo_code_output(tmp_path):
    """Test loading Roo Code output from file"""
    # Create test file
    test_file = tmp_path / "test_output.md"
    test_content = "# Test Review\nSample content"
    test_file.write_text(test_content)
    
    # Test loading valid file
    content = load_roo_code_output(str(test_file))
    assert content == test_content
    
    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        load_roo_code_output("nonexistent.md")
    
    # Test empty file
    empty_file = tmp_path / "empty.md"
    empty_file.write_text("")
    with pytest.raises(ValueError):
        load_roo_code_output(str(empty_file))

def test_markdown_to_docx(tmp_path, sample_markdown):
    """Test conversion from markdown to DOCX"""
    output_path = str(tmp_path / "test_output.docx")
    
    # Test valid conversion
    result_path = markdown_to_docx(sample_markdown, output_path)
    assert os.path.exists(result_path)
    assert result_path.endswith('.docx')
    
    # Test empty markdown
    with pytest.raises(ValueError):
        markdown_to_docx("", output_path)

def test_generate_final_report(test_output_dir, sample_markdown):
    """Test report generation in different formats"""
    # Test markdown output
    md_path = generate_final_report(
        sample_markdown,
        'annual',
        'markdown'
    )
    assert os.path.exists(md_path)
    assert md_path.endswith('.md')
    
    # Test DOCX output
    docx_path = generate_final_report(
        sample_markdown,
        'competency',
        'docx'
    )
    assert os.path.exists(docx_path)
    assert docx_path.endswith('.docx')
    
    # Test invalid review type
    with pytest.raises(ValueError):
        generate_final_report(sample_markdown, 'invalid', 'markdown')
    
    # Test invalid output format
    with pytest.raises(ValueError):
        generate_final_report(sample_markdown, 'annual', 'pdf')

def test_generate_final_report_creates_output_dir(tmp_path, sample_markdown):
    """Test that output directory is created if it doesn't exist"""
    # Change to temporary directory
    original_cwd = os.getcwd()
    os.chdir(str(tmp_path))
    
    try:
        # Generate report (should create output directory)
        output_path = generate_final_report(sample_markdown, 'annual', 'markdown')
        
        # Verify output directory was created
        assert os.path.exists('output')
        assert os.path.isdir('output')
        assert os.path.exists(output_path)
    finally:
        # Restore original working directory
        os.chdir(original_cwd)
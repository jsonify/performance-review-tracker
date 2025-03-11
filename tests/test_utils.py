"""
Tests for utils.py module.

This module contains unit tests for utility functions,
including file operations, date handling, and logging.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
import pytest
from src.utils import (
    ensure_directory_exists,
    safe_file_write,
    validate_date_format,
    get_review_period_dates,
    get_unique_filename,
    log_error,
    init_logger
)

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path / "test_dir"

@pytest.fixture
def test_logger(tmp_path):
    """Create a test logger with a temporary log file."""
    log_file = tmp_path / "test.log"
    return init_logger("test_logger", str(log_file))

def test_ensure_directory_exists(temp_dir):
    """Test directory creation."""
    # Test creating new directory
    ensure_directory_exists(temp_dir)
    assert temp_dir.exists()
    assert temp_dir.is_dir()

    # Test with existing directory (should not raise error)
    ensure_directory_exists(temp_dir)
    assert temp_dir.exists()

def test_safe_file_write(temp_dir):
    """Test safe file writing."""
    test_file = temp_dir / "test.txt"
    test_content = "Test content\nwith multiple lines"

    safe_file_write(test_file, test_content)
    assert test_file.exists()
    assert test_file.read_text(encoding='utf-8') == test_content

def test_safe_file_write_with_unicode(temp_dir):
    """Test safe file writing with Unicode content."""
    test_file = temp_dir / "unicode_test.txt"
    test_content = "Unicode test: 测试 テスト 테스트"

    safe_file_write(test_file, test_content)
    assert test_file.exists()
    assert test_file.read_text(encoding='utf-8') == test_content

def test_validate_date_format():
    """Test date format validation."""
    # Test valid dates
    assert validate_date_format("2024-03-11")
    assert validate_date_format("2025-12-31")

    # Test invalid dates
    assert not validate_date_format("2024/03/11")
    assert not validate_date_format("2024-13-11")
    assert not validate_date_format("invalid")

def test_get_review_period_dates():
    """Test review period date calculation."""
    # Test with valid year
    start_date, end_date = get_review_period_dates(2025)
    assert start_date == "2024-09-01"
    assert end_date == "2025-08-31"

    # Test with string year
    start_date, end_date = get_review_period_dates("2025")
    assert start_date == "2024-09-01"
    assert end_date == "2025-08-31"

    # Test invalid years
    with pytest.raises(ValueError):
        get_review_period_dates("invalid")
    with pytest.raises(ValueError):
        get_review_period_dates(1800)  # Too old
    with pytest.raises(ValueError):
        get_review_period_dates(10000)  # Too far in future

def test_get_unique_filename(temp_dir):
    """Test unique filename generation."""
    # Test with default parameters
    filename = get_unique_filename(temp_dir)
    assert isinstance(filename, Path)
    assert filename.suffix == ".md"
    assert str(filename.parent) == str(temp_dir)

    # Test with custom parameters
    filename = get_unique_filename(temp_dir, "test_", "_final", ".docx")
    assert filename.name.startswith("test_")
    assert filename.name.endswith("_final.docx")
    assert len(filename.stem) > len("test__final")  # Ensures timestamp is included

def test_get_unique_filename_uniqueness(temp_dir):
    """Test that generated filenames are unique."""
    filenames = set()
    for _ in range(5):  # Generate multiple filenames
        filename = get_unique_filename(temp_dir)
        filenames.add(filename.name)
    assert len(filenames) == 5  # All filenames should be unique

def test_log_error(test_logger, caplog):
    """Test error logging functionality."""
    test_error = ValueError("Test error")
    test_context = "Test context"

    with caplog.at_level(logging.ERROR):
        log_error(test_error, test_context)

    assert len(caplog.records) == 1
    assert "Test context: ValueError: Test error" in caplog.text
    assert "ValueError" in caplog.text

def test_init_logger(tmp_path):
    """Test logger initialization."""
    log_file = tmp_path / "test.log"
    logger = init_logger("test", str(log_file))

    # Test logger configuration
    assert logger.name == "test"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 2  # Console and file handlers

    # Test logging
    test_message = "Test log message"
    logger.info(test_message)

    # Verify log file contents
    assert log_file.exists()
    log_content = log_file.read_text()
    assert test_message in log_content

def test_init_logger_invalid_path():
    """Test logger initialization with invalid log file path."""
    logger = init_logger("test", "//nonexistent-server/share/test.log")

    # Should still have console handler
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)

def test_logger_handles_unicode(test_logger, caplog):
    """Test logger handles Unicode content correctly."""
    unicode_message = "Unicode test: 测试 テスト 테스트"
    with caplog.at_level(logging.INFO):
        test_logger.info(unicode_message)

    assert unicode_message in caplog.text

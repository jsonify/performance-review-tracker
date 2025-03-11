"""
Tests for data_processor.py module.

This module contains unit tests for the data processing functionality,
including data loading, filtering, validation, and preparation.
"""

import os
import json
from datetime import datetime
import pytest
import pandas as pd
from src.data_processor import (
    load_data,
    filter_by_date_range,
    validate_data,
    prepare_data_for_analysis
)

# Test data
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
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(SAMPLE_DATA)

@pytest.fixture
def temp_csv(tmp_path, sample_df):
    """Create a temporary CSV file with sample data."""
    csv_path = tmp_path / "test_data.csv"
    sample_df.to_csv(csv_path, index=False)
    return csv_path

@pytest.fixture
def temp_excel(tmp_path, sample_df):
    """Create a temporary Excel file with sample data."""
    excel_path = tmp_path / "test_data.xlsx"
    sample_df.to_excel(excel_path, index=False)
    return excel_path

def test_load_data_csv(temp_csv):
    """Test loading data from CSV file."""
    df = load_data(str(temp_csv))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == [
        'Date', 'Title', 'Description', 'Acceptance Criteria',
        'Success Notes', 'Impact'
    ]

def test_load_data_excel(temp_excel):
    """Test loading data from Excel file."""
    df = load_data(str(temp_excel))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == [
        'Date', 'Title', 'Description', 'Acceptance Criteria',
        'Success Notes', 'Impact'
    ]

def test_load_data_nonexistent_file():
    """Test loading data from nonexistent file."""
    with pytest.raises(FileNotFoundError):
        load_data("nonexistent_file.csv")

def test_load_data_unsupported_format(tmp_path):
    """Test loading data from unsupported file format."""
    unsupported_file = tmp_path / "test.txt"
    unsupported_file.write_text("test data")
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_data(str(unsupported_file))

def test_filter_by_date_range(sample_df):
    """Test filtering data by date range."""
    # Test inclusive date range
    start_date = "2024-12-01"
    end_date = "2025-01-01"
    filtered_df = filter_by_date_range(sample_df, start_date, end_date)
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]['Title'] == 'Task 2'

def test_filter_by_date_range_invalid_dates(sample_df):
    """Test filtering with invalid date formats."""
    with pytest.raises(ValueError, match="Invalid .* date format"):
        filter_by_date_range(sample_df, "invalid_date", "2025-01-01")

def test_filter_by_date_range_missing_date_column():
    """Test filtering with missing Date column."""
    df = pd.DataFrame({'Column': [1, 2, 3]})
    with pytest.raises(ValueError, match="must contain a 'Date' column"):
        filter_by_date_range(df, "2024-01-01", "2025-01-01")

def test_validate_data_valid(sample_df):
    """Test data validation with valid data."""
    validate_data(sample_df)  # Should not raise any exceptions

def test_validate_data_missing_columns():
    """Test data validation with missing columns."""
    df = pd.DataFrame({'Date': ['2024-01-01']})
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(df)

def test_validate_data_invalid_impact():
    """Test data validation with invalid Impact values."""
    data = SAMPLE_DATA.copy()
    data.append({'Date': '2024-01-01', 'Title': 'Invalid Task', 'Description': 'Test', 'Acceptance Criteria': 'Test', 'Success Notes': 'Test', 'Impact': 'Invalid'
})
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Invalid Impact values found"):
        validate_data(df)

def test_prepare_data_for_analysis(sample_df, tmp_path):
    """Test complete data preparation workflow."""
    # Set up test environment
    os.chdir(tmp_path)
    os.makedirs('data', exist_ok=True)

    # Test annual review
    output_path = prepare_data_for_analysis(sample_df, 'annual', '2025')
    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

    # Test competency assessment
    output_path = prepare_data_for_analysis(sample_df, 'competency')
    assert os.path.exists(output_path)
    with open(output_path, 'r') as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert all(isinstance(item, dict) for item in data)

def test_prepare_data_invalid_review_type(sample_df):
    """Test data preparation with invalid review type."""
    with pytest.raises(ValueError, match="Invalid review type"):
        prepare_data_for_analysis(sample_df, 'invalid')

def test_prepare_data_missing_year(sample_df):
    """Test annual review preparation without year."""
    with pytest.raises(ValueError, match="Year is required"):
        prepare_data_for_analysis(sample_df, 'annual')

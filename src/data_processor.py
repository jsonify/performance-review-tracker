#!/usr/bin/env python3
"""
Data Processor for Performance Review Tracking System.

This module handles loading and preparing data for analysis, including:
- Loading data from CSV/Excel files
- Filtering data by date ranges for Annual Reviews
- Preparing data for Roo Code analysis
"""

import argparse
import json
import os
from datetime import datetime
from typing import Optional, Union

import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from CSV or Excel file.

    Args:
        file_path (str): Path to the data file (CSV or Excel)

    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is not supported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_ext = os.path.splitext(file_path)[1].lower()
    try:
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    except Exception as e:
        raise ValueError(f"Error loading data from {file_path}: {str(e)}")


def filter_by_date_range(
    data: pd.DataFrame,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime]
) -> pd.DataFrame:
    """
    Filter entries by date range for Annual Review.

    Args:
        data (pd.DataFrame): Input DataFrame containing work entries
        start_date (Union[str, datetime]): Start date for filtering
        end_date (Union[str, datetime]): End date for filtering

    Returns:
        pd.DataFrame: Filtered DataFrame containing only entries within the date range

    Raises:
        ValueError: If dates are invalid or if DataFrame lacks required columns
    """
    if 'Date' not in data.columns:
        raise ValueError("DataFrame must contain a 'Date' column")

    # Convert string dates to datetime if needed
    if isinstance(start_date, str):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid start date format: {start_date}. Use YYYY-MM-DD")

    if isinstance(end_date, str):
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid end date format: {end_date}. Use YYYY-MM-DD")

    # Convert data dates to datetime for comparison
    data['Date'] = pd.to_datetime(data['Date'])

    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    # Filter by date range
    mask = data['Date'].between(start_ts, end_ts)
    return pd.DataFrame(data[mask]).reset_index(drop=True)


def validate_data(data: pd.DataFrame) -> None:
    """
    Validate the structure and content of the input data.

    Args:
        data (pd.DataFrame): Input DataFrame to validate

    Raises:
        ValueError: If data doesn't meet required format
    """
    required_columns = [
        'Date',
        'Title',
        'Description',
        'Acceptance Criteria',
        'Success Notes',
        'Impact'
    ]

    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Validate Impact values
    valid_impacts = ['High', 'Medium', 'Low']
    invalid_impacts = data[~data['Impact'].isin(valid_impacts)]['Impact'].unique()
    if len(invalid_impacts) > 0:
        raise ValueError(
            f"Invalid Impact values found: {', '.join(map(str, invalid_impacts))}. "
            f"Valid values are: {', '.join(valid_impacts)}"
        )


def prepare_data_for_analysis(
    data: pd.DataFrame,
    review_type: str,
    year: Optional[str] = None
) -> str:
    """
    Prepare data for Roo Code analysis.

    Args:
        data (pd.DataFrame): Input DataFrame to prepare
        review_type (str): Type of review ('annual' or 'competency')
        year (Optional[str]): Year for annual review filtering

    Returns:
        str: Path to the saved JSON file containing prepared data

    Raises:
        ValueError: If review_type is invalid or if year is missing for annual review
    """
    # Validate review type
    if review_type.lower() not in ['annual', 'competency']:
        raise ValueError(
            "Invalid review type. Must be either 'annual' or 'competency'"
        )

    # Validate and prepare data
    validate_data(data)

    if review_type.lower() == 'annual':
        if not year:
            raise ValueError("Year is required for annual reviews")

        # Annual review covers Sept to Aug
        start_date = f"{int(year)-1}-09-01"
        end_date = f"{year}-08-31"
        data = filter_by_date_range(data, start_date, end_date)

    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)

    # Convert to JSON format for Roo Code
    output_path = f"data/processed_{review_type.lower()}.json"

    # Convert dates to ISO format strings for JSON serialization
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

    # Save to file for Roo Code to access
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json.loads(data.to_json(orient='records')), f, indent=2)

    return output_path


def main():
    """Command-line interface for the data processor."""
    parser = argparse.ArgumentParser(
        description='Process performance review data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Process data for annual review:
    %(prog)s --file data/accomplishments.csv --type annual --year 2025

  Process data for competency assessment:
    %(prog)s --file data/accomplishments.csv --type competency
        """
    )

    parser.add_argument(
        '--file',
        required=True,
        help='Path to data file (CSV or Excel)'
    )
    parser.add_argument(
        '--type',
        required=True,
        choices=['annual', 'competency'],
        help='Review type'
    )
    parser.add_argument(
        '--year',
        help='Year for annual review (required for annual review type)'
    )

    args = parser.parse_args()

    try:
        # Load data
        print(f"Loading data from {args.file}...")
        data = load_data(args.file)

        # Process data
        print("Processing data...")
        output_path = prepare_data_for_analysis(data, args.type, args.year)

        print(f"Data processed successfully and saved to {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()

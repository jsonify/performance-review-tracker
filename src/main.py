#!/usr/bin/env python3
"""
Main script for the Performance Review Tracking System.

This script orchestrates the end-to-end process of generating performance
review reports, including data processing and report generation.
"""

import argparse
import subprocess
import sys
import os


def main():
    """
    Main function to orchestrate data processing and report generation.
    """
    parser = argparse.ArgumentParser(
        description="Generate performance review reports",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  Generate an annual review report:
    %(prog)s --file data/accomplishments.csv --type annual --year 2025 --format docx

  Generate a competency assessment report:
    %(prog)s --file data/accomplishments.csv --type competency --format markdown
        """
    )

    # Add common arguments
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the data file (CSV or Excel)"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["annual", "competency"],
        help="Type of review (annual or competency)"
    )
    parser.add_argument(
        "--year",
        help="Year for annual review (required for annual review type)"
    )
    parser.add_argument(
        "--format",
        default="markdown",
        choices=["markdown", "docx"],
        help="Output format (markdown or docx)"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.type == "annual" and not args.year:
        parser.error("--year is required for annual reviews")

    try:
        # 1. Data Processing
        print("Processing data...")
        data_processor_cmd = [
            "python", "src/data_processor.py",
            "--file", args.file,
            "--type", args.type
        ]
        if args.year:
            data_processor_cmd.extend(["--year", args.year])

        result = subprocess.run(data_processor_cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        processed_data_path = result.stdout.split("saved to ")[-1].strip()

        # 2. Report Generation
        print("Generating report...")
        report_generator_cmd = [
            "python", "src/report_generator.py",
            "--input", processed_data_path,
            "--type", args.type,
            "--format", args.format
        ]

        result = subprocess.run(report_generator_cmd, capture_output=True, text=True, check=True)
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
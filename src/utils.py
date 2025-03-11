"""
Utility functions for the Performance Review Tracking System.

This module provides helper functions for:
- File operations
- Date handling
- Logging
"""

import os
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Union, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('performance_review.log')  # File output
    ]
)

logger = logging.getLogger(__name__)

def ensure_directory_exists(directory: Union[str, Path]) -> None:
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory (Union[str, Path]): Path to the directory

    Raises:
        OSError: If directory creation fails
    """
    try:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")
    except OSError as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        raise

def safe_file_write(filepath: Union[str, Path], content: str) -> None:
    """
    Safely write content to a file, creating directories if needed.

    Args:
        filepath (Union[str, Path]): Path to the file
        content (str): Content to write

    Raises:
        OSError: If file writing fails
    """
    try:
        # Ensure the directory exists
        directory = os.path.dirname(filepath)
        ensure_directory_exists(directory)

        # Write the file with proper encoding
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.debug(f"Successfully wrote to file: {filepath}")
    except OSError as e:
        logger.error(f"Failed to write to file {filepath}: {e}")
        raise

def validate_date_format(date_str: str, fmt: str = '%Y-%m-%d') -> bool:
    """
    Validate if a date string matches the expected format.

    Args:
        date_str (str): Date string to validate
        fmt (str, optional): Expected date format. Defaults to '%Y-%m-%d'.

    Returns:
        bool: True if date string is valid, False otherwise
    """
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False

def get_review_period_dates(year: Union[str, int]) -> tuple[str, str]:
    """
    Get start and end dates for an annual review period (September to August).

    Args:
        year (Union[str, int]): The year of the review end date

    Returns:
        tuple[str, str]: Tuple of (start_date, end_date) in YYYY-MM-DD format

    Raises:
        ValueError: If year is invalid
    """
    try:
        year = int(year)
        if year < 1900 or year > 9999:
            raise ValueError("Year must be between 1900 and 9999")

        start_date = f"{year-1}-09-01"
        end_date = f"{year}-08-31"
        return start_date, end_date
    except ValueError as e:
        logger.error(f"Invalid year provided: {year}")
        raise ValueError(f"Invalid year format: {e}")

def get_unique_filename(base_path: Union[str, Path],
                       prefix: str = "",
                       suffix: str = "",
                       extension: str = ".md") -> Path:
    """
    Generate a unique filename using a timestamp.

    Args:
        base_path (Union[str, Path]): Base directory for the file
        prefix (str, optional): Prefix for the filename. Defaults to "".
        suffix (str, optional): Suffix for the filename. Defaults to "".
        extension (str, optional): File extension. Defaults to ".md".

    Returns:
        Path: Path object with the unique filename

    Example:
        >>> get_unique_filename("output", "review_", "_final", ".docx")
        Path('output/review_20250311_132145_final.docx')
    """
    time.sleep(0.01)  # Ensure unique timestamps in rapid succession
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = f"{prefix}{timestamp}{suffix}{extension}"
    return Path(base_path) / filename

def log_error(error: Exception, context: str = "") -> None:
    """
    Log an error with optional context.

    Args:
        error (Exception): The error to log
        context (str, optional): Additional context about where/why the error occurred
    """
    message = f"{context + ': ' if context else ''}{type(error).__name__}: {str(error)}"
    logger.error(message, exc_info=True)

def init_logger(name: str,
                log_file: Optional[str] = None,
                level: int = logging.INFO) -> logging.Logger:
    """
    Initialize a logger with console and optional file output.

    Args:
        name (str): Name for the logger
        log_file (Optional[str], optional): Path to log file. Defaults to None.
        level (int, optional): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance
    """
    # Get logger and clear any existing handlers
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log_file is specified
    if log_file is not None:
        try:
            # Create directory if needed
            log_dir = os.path.dirname(log_file)
            if log_dir:
                ensure_directory_exists(log_dir)

            # Create file handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)

            # Test if file is writable
            file_handler.stream.write('')
            file_handler.stream.flush()

            # Add handler if all tests pass
            logger.addHandler(file_handler)
        except (OSError, IOError) as e:
            logger.error(f"Failed to set up file logging to {log_file}: {e}")
            # Keep only console handler
            logger.handlers = [console_handler]

    return logger

#!/bin/bash

# Activate virtual environment
source venv/bin/activate || {
    echo "Error: Failed to activate virtual environment. Please ensure it exists by running:"
    echo "python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
}

# Function to display script usage
usage() {
    echo "Usage: $0 --input <file> --type <annual|competency> [--year YYYY]"
    echo
    echo "Options:"
    echo "  --input    Input CSV file path"
    echo "  --type     Review type (annual or competency)"
    echo "  --year     Year for annual review (required for annual reviews)"
    echo
    echo "Example:"
    echo "  $0 --input data/accomplishments.csv --type annual --year 2025"
    exit 1
}

# Function to validate input file
validate_input_file() {
    local file=$1
    if [ ! -f "$file" ]; then
        echo "Error: Input file '$file' does not exist"
        exit 1
    fi
    
    if [[ ! "$file" =~ \.(csv|xlsx)$ ]]; then
        echo "Error: Input file must be a CSV or XLSX file"
        exit 1
    fi
}

# Function to validate review type
validate_review_type() {
    local type=$1
    if [ "$type" != "annual" ] && [ "$type" != "competency" ]; then
        echo "Error: Review type must be 'annual' or 'competency'"
        exit 1
    fi
}

# Function to validate year
validate_year() {
    local year=$1
    if ! [[ "$year" =~ ^[0-9]{4}$ ]]; then
        echo "Error: Year must be a 4-digit number"
        exit 1
    fi
}

# Function to display progress
show_progress() {
    local msg=$1
    echo ">>> $msg..."
}

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --input)
            input_file="$2"
            shift 2
            ;;
        --type)
            review_type="$2"
            shift 2
            ;;
        --year)
            review_year="$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        *)
            echo "Error: Unknown parameter '$1'"
            usage
            ;;
    esac
done

# Validate required parameters
if [ -z "$input_file" ] || [ -z "$review_type" ]; then
    echo "Error: Missing required parameters"
    usage
fi

# Validate inputs
validate_input_file "$input_file"
validate_review_type "$review_type"

# Validate year for annual reviews
if [ "$review_type" == "annual" ]; then
    if [ -z "$review_year" ]; then
        echo "Error: Year is required for annual reviews"
        exit 1
    fi
    validate_year "$review_year"
fi

# Process the data
show_progress "Processing data file"

# Build python command
cmd="python src/data_processor.py --file \"$input_file\" --type $review_type"
if [ "$review_type" == "annual" ]; then
    cmd="$cmd --year $review_year"
fi

# Execute data processing
echo "Executing: $cmd"
eval "$cmd" > process_data.log 2>&1
if [ $? -ne 0 ]; then
    echo "Error: Data processing failed. See process_data.log for details."
    exit 1
fi

show_progress "Data processing completed"
echo "Output saved to data/processed_${review_type}.json"

# Deactivate virtual environment
deactivate
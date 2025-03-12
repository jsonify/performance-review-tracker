#!/bin/bash

# Activate virtual environment
source venv/bin/activate || {
    echo "Error: Failed to activate virtual environment. Please ensure it exists by running:"
    echo "python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
}

# Function to display script usage
usage() {
    echo "Usage: $0 --input <file> --format <markdown|docx> --output <path>"
    echo
    echo "Options:"
    echo "  --input    Input file path (processed data JSON)"
    echo "  --format   Output format (markdown or docx)"
    echo "  --output   Output file path"
    echo
    echo "Example:"
    echo "  $0 --input data/processed_annual.json --format docx --output output/annual_review.docx"
    exit 1
}

# Function to validate input file
validate_input_file() {
    local file=$1
    if [ ! -f "$file" ]; then
        echo "Error: Input file '$file' does not exist"
        exit 1
    fi
    
    if [[ ! "$file" =~ \.json$ ]]; then
        echo "Error: Input file must be a JSON file"
        exit 1
    fi
}

# Function to validate format
validate_format() {
    local format=$1
    if [ "$format" != "markdown" ] && [ "$format" != "docx" ]; then
        echo "Error: Format must be 'markdown' or 'docx'"
        exit 1
    fi
}

# Function to validate output path
validate_output_path() {
    local output=$1
    local format=$2
    local dir=$(dirname "$output")
    
    # Create output directory if it doesn't exist
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir" || {
            echo "Error: Failed to create output directory '$dir'"
            exit 1
        }
    fi
    
    # Check file extension matches format
    if [ "$format" == "markdown" ] && [[ ! "$output" =~ \.md$ ]]; then
        echo "Error: Output file must have .md extension for markdown format"
        exit 1
    elif [ "$format" == "docx" ] && [[ ! "$output" =~ \.docx$ ]]; then
        echo "Error: Output file must have .docx extension for docx format"
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
        --format)
            output_format="$2"
            shift 2
            ;;
        --output)
            output_path="$2"
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
if [ -z "$input_file" ] || [ -z "$output_format" ] || [ -z "$output_path" ]; then
    echo "Error: Missing required parameters"
    usage
fi

# Validate inputs
validate_input_file "$input_file"
validate_format "$output_format"
validate_output_path "$output_path" "$output_format"

# Determine review type from input filename
review_type=""
if [[ "$input_file" =~ processed_annual\.json$ ]]; then
    review_type="annual"
elif [[ "$input_file" =~ processed_competency\.json$ ]]; then
    review_type="competency"
else
    echo "Error: Unable to determine review type from input file name"
    exit 1
fi

# Generate the report
show_progress "Generating $review_type review report in $output_format format"

# Build python command
cmd="python src/report_generator.py --input \"$input_file\" --type $review_type --format $output_format --output \"$output_path\""

# Execute report generation
echo "Executing: $cmd"
eval "$cmd" > generate_report.log 2>&1
if [ $? -ne 0 ]; then
    echo "Error: Report generation failed. See generate_report.log for details."
    exit 1
fi

show_progress "Report generation completed"
echo "Output saved to $output_path"

# Deactivate virtual environment
deactivate
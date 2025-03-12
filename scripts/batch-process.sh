#!/bin/bash

# Activate virtual environment
source venv/bin/activate || {
    echo "Error: Failed to activate virtual environment. Please ensure it exists by running:"
    echo "python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
}

# Function to display script usage
usage() {
    echo "Usage: $0 --input-dir <directory> --output-dir <directory> [--type <annual|competency>] [--year YYYY]"
    echo
    echo "Options:"
    echo "  --input-dir   Directory containing input CSV/XLSX files"
    echo "  --output-dir  Directory for output reports"
    echo "  --type        Review type (annual or competency)"
    echo "  --year        Year for annual reviews"
    echo
    echo "Example:"
    echo "  $0 --input-dir data/batch --output-dir output/batch --type annual --year 2025"
    exit 1
}

# Function to validate directory
validate_directory() {
    local dir=$1
    local create=${2:-false}
    
    if [ ! -d "$dir" ]; then
        if [ "$create" = true ]; then
            mkdir -p "$dir" || {
                echo "Error: Failed to create directory '$dir'"
                exit 1
            }
        else
            echo "Error: Directory '$dir' does not exist"
            exit 1
        fi
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
    local current=$1
    local total=$2
    local percentage=$((current * 100 / total))
    printf "\rProcessing files: [%-50s] %d%%" $(printf "#%.0s" $(seq 1 $((percentage/2)))) $percentage
}

# Parse command line arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --input-dir)
            input_dir="$2"
            shift 2
            ;;
        --output-dir)
            output_dir="$2"
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
if [ -z "$input_dir" ] || [ -z "$output_dir" ]; then
    echo "Error: Missing required parameters"
    usage
fi

# Validate inputs
validate_directory "$input_dir"
validate_directory "$output_dir" true

# Validate review type if provided
if [ ! -z "$review_type" ]; then
    validate_review_type "$review_type"
    # Validate year for annual reviews
    if [ "$review_type" == "annual" ]; then
        if [ -z "$review_year" ]; then
            echo "Error: Year is required for annual reviews"
            exit 1
        fi
        validate_year "$review_year"
    fi
fi

# Find all CSV and XLSX files in input directory
files=($(find "$input_dir" -type f \( -name "*.csv" -o -name "*.xlsx" \)))
total_files=${#files[@]}

if [ $total_files -eq 0 ]; then
    echo "Error: No CSV or XLSX files found in input directory"
    exit 1
fi

echo "Found $total_files files to process"
echo

# Process each file
for ((i=0; i<${#files[@]}; i++)); do
    file="${files[$i]}"
    filename=$(basename "$file")
    base_filename="${filename%.*}"
    
    # Show progress
    show_progress $((i+1)) $total_files
    
    # Process the data
    if [ ! -z "$review_type" ]; then
        process_cmd="./scripts/process-data.sh --input \"$file\" --type $review_type"
        if [ "$review_type" == "annual" ] && [ ! -z "$review_year" ]; then
            process_cmd="$process_cmd --year $review_year"
        fi
        
        if ! eval "$process_cmd"; then
            echo
            echo "Error: Failed to process $filename"
            continue
        fi
        
        # Generate the report
        output_file="$output_dir/${base_filename}_${review_type}.docx"
        generate_cmd="./scripts/generate-report.sh --input \"data/processed_${review_type}.json\" --format docx --output \"$output_file\""
        
        if ! eval "$generate_cmd"; then
            echo
            echo "Error: Failed to generate report for $filename"
            continue
        fi
    else
        # Try both annual and competency reports if type not specified
        for type in "annual" "competency"; do
            process_cmd="./scripts/process-data.sh --input \"$file\" --type $type"
            if [ "$type" == "annual" ]; then
                current_year=$(date +"%Y")
                process_cmd="$process_cmd --year $current_year"
            fi
            
            if eval "$process_cmd" 2>/dev/null; then
                output_file="$output_dir/${base_filename}_${type}.docx"
                generate_cmd="./scripts/generate-report.sh --input \"data/processed_${type}.json\" --format docx --output \"$output_file\""
                
                if ! eval "$generate_cmd"; then
                    echo
                    echo "Error: Failed to generate $type report for $filename"
                fi
            fi
        done
    fi
done

echo
echo "Batch processing completed"
echo "Output files saved in $output_dir"

# Deactivate virtual environment
deactivate
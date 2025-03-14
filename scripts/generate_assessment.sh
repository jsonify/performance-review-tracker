#!/bin/bash

# Script to generate competency assessment report

# Ensure we're in the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Ensure output directory exists
mkdir -p output

# Run assessment
echo "Generating competency assessment..."
python src/example_assessment.py --accomplishments data/accomplishments.csv --prompt .roo/system-prompt-competency-analyst --output output/competency_assessment.md

# Check if report was generated
if [ -f "output/competency_assessment.md" ]; then
    echo "Assessment complete! Report generated at: output/competency_assessment.md"
else
    echo "Error: Report generation failed!"
    exit 1
fi

echo ""
echo "Done!"
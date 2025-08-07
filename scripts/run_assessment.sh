#!/bin/bash

# Helper script to generate test data and run assessment

# Ensure we're in the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Ensure scripts are executable
chmod +x scripts/generate_assessment.sh
chmod +x scripts/generate_test_data.py

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Generate test data if needed
if [ ! -f "data/accomplishments.csv" ] || [ "$1" == "--fresh" ]; then
    echo "Generating test data..."
    python scripts/generate_test_data.py --num 15
fi

# Run assessment
./scripts/generate_assessment.sh

# Show summary of results
echo ""
echo "Quick Summary:"
echo "=============="
if [ -f "output/competency_assessment.md" ]; then
    echo "Top rated competencies:"
    grep -A 1 "^### Rating:" output/competency_assessment.md | grep -B 1 "5/5\|4/5" | grep "^##[^#]"
    
    echo ""
    echo "Total competencies assessed:"
    grep -c "^## [^#]" output/competency_assessment.md
    
    echo ""
    echo "View full report at: output/competency_assessment.md"
fi

echo ""
echo "Done!"
# Developer Documentation

## Project Structure

```
performance-review-tracker/
├── src/
│   ├── data_processor.py  # Data loading and processing functionality
│   ├── report_generator.py  # Report generation and formatting
│   ├── utils.py  # Utility functions and helpers
│   ├── validation.py  # Validation tools and functions
│   └── main.py  # Main entry point and CLI
├── templates/
│   ├── annual_review_template.md  # Template for annual reviews
│   └── competency_assessment_template.md  # Template for competency assessments
├── criteria/
│   ├── annual_review_criteria.json  # Annual review criteria definitions
│   └── competency_assessment_criteria.json  # Competency assessment criteria
├── data/
│   └── (exported spreadsheet data)  # CSV files from Google Sheets
├── output/
│   └── (generated reports)  # Generated review documents
└── tests/
    └── (test files)  # Unit and integration tests
```

## Module Descriptions

### data_processor.py
Core module for loading and processing accomplishment data from various sources. Handles data validation, filtering, and preparation for analysis.

Key Functions:
- `load_data(file_path: str) -> pd.DataFrame`: Loads data from CSV or Excel files
- `filter_by_date_range(data: pd.DataFrame, start_date: str, end_date: str)`: Filters entries by date range
- `validate_data(data: pd.DataFrame) -> None`: Validates the structure and content of input data
- `prepare_data_for_analysis(data: pd.DataFrame, review_type: str, year: Optional[str])`: Prepares data for Roo Code analysis
- `main()`: CLI entry point for data processing operations

### report_generator.py
Handles the generation and formatting of final review reports in various formats.

Key Functions:
- `load_roo_code_output(file_path)`: Loads analysis output from Roo Code
- `markdown_to_docx(markdown_text, output_path)`: Converts markdown reports to DOCX format
- `generate_final_report(roo_output, review_type, output_format='markdown', output_path=None)`: Generates the final formatted report
- `main()`: CLI entry point for report generation

### utils.py
Utility functions used across the project for common operations.

Key Functions:
- `validate_criteria_coverage(data, criteria)`: Ensures all required criteria are covered
- `check_report_completeness(report)`: Verifies report contains all required sections
- `validate_report_structure(report)`: Validates the structure of generated reports

### validation.py
Comprehensive validation tools for ensuring report quality and completeness.

Key Functions:
- `load_criteria(criteria_file: str)`: Loads criteria definitions from JSON files
- `validate_criteria_coverage(content: str, criteria: List[Dict])`: Checks criteria coverage in reports
- `validate_report_structure(content: str)`: Validates report structure against templates
- `validate_content_completeness(content: str)`: Ensures all required content is present
- `extract_text_from_docx(docx_path: str)`: Extracts text content from DOCX files
- `validate_report(report_path: str, criteria_file: str)`: Performs comprehensive report validation
- `generate_validation_report(report_path: str, criteria_file: str)`: Creates validation summary report

### main.py
Main entry point for the application, providing CLI interface for all operations.

Key Functions:
- `main()`: Primary CLI interface with subcommands for different operations

## Testing

The project uses Python's built-in `unittest` framework for testing. Tests are organized in the `tests/` directory:

- Unit tests for individual modules
- Integration tests for end-to-end workflows
- Validation tests for report generation
- Debug utilities for development

To run tests:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests/test_data_processor.py

# Run with verbose output
python -m unittest -v
```

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints for function parameters and return values
   - Include docstrings for all functions and classes
   - Keep functions focused and single-purpose

2. **Error Handling**
   - Use appropriate exception types
   - Include meaningful error messages
   - Log errors for debugging
   - Validate inputs early

3. **Testing**
   - Write tests for new functionality
   - Maintain test coverage
   - Use meaningful test names
   - Include edge cases

4. **Documentation**
   - Update documentation for new features
   - Include examples in docstrings
   - Keep README current
   - Document any configuration changes

## Contributing

1. **Setting Up Development Environment**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd performance-review-tracker

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Making Changes**
   - Create a feature branch
   - Make changes with appropriate tests
   - Update documentation
   - Submit pull request

## Common Tasks

### Adding New Criteria
1. Update appropriate JSON file in `criteria/`
2. Add validation rules if needed
3. Update templates if required
4. Add tests for new criteria

### Modifying Report Format
1. Update templates in `templates/`
2. Modify report generation code
3. Update validation rules
4. Test with sample data

### Adding New Features
1. Plan changes and impact
2. Update relevant modules
3. Add tests
4. Update documentation
5. Test end-to-end workflow

## Troubleshooting Development Issues

### Common Issues

1. **Data Loading Errors**
   - Check file permissions
   - Verify file format
   - Validate data structure
   - Check encoding

2. **Report Generation Issues**
   - Verify template exists
   - Check output directory permissions
   - Validate input data
   - Check for missing dependencies

3. **Test Failures**
   - Check test data exists
   - Verify environment setup
   - Check for recent changes
   - Review test logs

## API Documentation

Detailed API documentation for each module is maintained in the source code docstrings. 
To generate HTML documentation:

```bash
# Using pdoc3
pdoc --html --output-dir docs/api src/

# Using Sphinx
cd docs
make html
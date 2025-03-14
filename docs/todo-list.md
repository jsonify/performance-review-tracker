# Performance Review Tracking System Implementation Todo List


- [x] Create project directory structure
  - [x] Create main project folder (`performance-review-tracker`)
  - [x] Create subdirectories (`src`, `templates`, `criteria`, `data`, `output`, `tests`)
- [x] Set up virtual environment
  - [x] Install Python 3.9+ if not already installed
  - [x] Create virtual environment: `python -m venv venv`
  - [x] Activate virtual environment
- [x] Initialize Git repository
  - [x] Run `git init`
  - [x] Create `.gitignore` file with appropriate entries
- [x] Create initial `requirements.txt` with dependencies:
  - [x] `pandas` for data processing
  - [x] `gspread` (optional, for Google Sheets API)
  - [x] `google-auth` (optional, for authentication)
  - [x] `python-docx` for document creation
  - [x] `markdown` for markdown processing
  - [x] `argparse` for command-line interface
- [x] Install dependencies: `pip install -r requirements.txt`
- [x] Create basic README.md with project overview
- [x] Install VS Code if not already installed
- [x] Install Roo Code extension for VS Code

## Phase 2: VS Code and Roo Code Setup

- [x] Configure VS Code for Python development
  - [x] Install Python extension
  - [x] Configure Python interpreter
  - [x] Set up linting and formatting
- [x] Configure Roo Code extension
  - [x] Create `.roo` directory
  - [x] Create custom system prompt for Analyst mode
  - [x] Test basic Roo Code functionality
- [x] Create custom mode for Performance Review analysis
  - [x] Define role definition for Analyst mode
  - [x] Configure tool permissions
  - [x] Test custom mode functionality

## Phase 3: Criteria Definition

- [x] Create criteria definition files
  - [x] Create `criteria/annual_review_criteria.json` with detailed definitions
  - [x] Create `criteria/competency_assessment_criteria.json` with detailed definitions
- [x] Create report templates
  - [x] Develop `templates/annual_review_template.md`
  - [x] Develop `templates/competency_assessment_template.md`

## Phase 4: Google Sheets Integration

- [x] Create Google Sheet template
  - [x] Set up simplified column structure (without manual tagging columns)
  - [x] Add data validation for dropdown fields
  - [x] Create sample data for testing
- [x] Set up data export process
  - [x] Document manual CSV export process
  - [x] (Optional) Set up Google Sheets API access
    - [ ] Create Google Cloud project (if needed)
    - [ ] Enable Google Sheets API
    - [ ] Create service account for API access
    - [ ] Download and secure credentials file

## Phase 5: Data Processing Scripts

- [x] Create data processing module
  - [x] Implement `src/data_processor.py`
  - [x] Add functions to load data from CSV/Excel
  - [x] (Optional) Add functions to load data directly from Google Sheets
  - [x] Implement date filtering for Annual Reviews
  - [x] Add data validation and cleaning functions
  - [x] Create functions to save processed data as JSON
- [x] Create report generation module
  - [x] Implement `src/report_generator.py`
  - [x] Add functions to load Roo Code analysis output
  - [x] Create markdown to DOCX conversion function
  - [x] Implement file naming and organization functions
- [x] Create utilities module
  - [x] Implement `src/utils.py`
  - [x] Add helper functions for file operations
  - [x] Create date handling utilities
  - [x] Implement logging functions

## Phase 6: Roo Code Integration

- [x] Finalize Roo Code custom system prompt
  - [x] Refine criteria definitions for better analysis
  - [x] Improve output formatting instructions
  - [x] Add detailed error handling guidance
- [x] Create prompting guide
  - [x] Document sample prompts for different report types
  - [x] Create examples with different parameters
  - [x] Develop troubleshooting guidance
- [x] Develop context mention patterns
  - [x] Create standardized file references
  - [x] Document effective mention strategies
  - [x] Test with various data scenarios

## Phase 7: Command-Line Interface

- [x] Implement command-line interface for data processor
  - [x] Add arguments for input file path
  - [x] Add arguments for review type (annual/competency)
  - [x] Add arguments for date ranges and year
  - [x] Implement help documentation
- [x] Implement command-line interface for report generator
  - [x] Add arguments for input file path
  - [x] Add arguments for output format
  - [x] Add arguments for output file path
  - [x] Implement help documentation
- [x] Create combined CLI script
  - [x] Implement `src/main.py` for end-to-end processing
  - [x] Add subcommands for different functionality
  - [x] Create sample usage commands

## Phase 8: Testing and Validation

- [x] Set up testing framework
  - [x] Configure pytest in the project
  - [x] Create test fixtures with sample data
  - [x] Implement helper functions for testing
- [x] Create unit tests
  - [x] Test data loading and processing functions
  - [x] Test date filtering functions
  - [x] Test report generation functions
- [x] Create integration tests
  - [x] Test end-to-end workflow with sample data
  - [x] Validate output format and content
  - [x] Test edge cases and error conditions
- [x] Create validation tools
  - [x] Implement validation for criteria coverage
  - [x] Create checks for report completeness
  - [x] Add tools to validate report structure
- [x] Fixed tests failing due to missing dependencies
- [x] Fixed tests failing due to incorrect import statements
- [x] Updated cwd argument in integration tests
  - [x] Validate output format and content
  - [x] Test edge cases and error conditions
- [x] Create validation tools
  - [x] Implement validation for criteria coverage
  - [x] Create checks for report completeness
  - [x] Add tools to validate report structure

## Phase 9: Documentation

- [x] Create user documentation
  - [x] Write Google Sheet setup guide
  - [x] Create data entry instructions
  - [x] Document report generation process
  - [x] Add troubleshooting section
- [x] Create developer documentation
  - [x] Document project structure
  - [x] Create module descriptions
  - [x] Add function documentation
  - [x] Document testing procedures
- [x] Create Roo Code usage guide
  - [x] Document Analyst mode functionality
  - [x] Provide sample prompts
  - [x] Create troubleshooting guide
  - [x] Add examples of effective context references

## Phase 10: Workflow Integration and Optimization

- [x] Create streamlined workflows
  - [x] Develop shell scripts for common tasks
  - [x] Add VS Code tasks for frequent operations
  - [x] Create batch processing capabilities
  - [x] Document performance review workflow steps:
    - [x] Step 1: Process raw data (process-data.sh)

      ```bash
      python src/data_processor.py --file data/accomplishments.csv --type annual --year 2025
      ```

    - [x] Step 2: Generate Roo Code analysis
      - Open VS Code
      - Switch to Performance Analyst mode
      - Run: @/data/processed_annual.json analyze for review
      - Save output as: data/analyzed_annual.md
    - [x] Step 3: Generate final report (generate-report.sh)

      ```bash
      ./scripts/generate-report.sh --input data/processed_annual.json --format markdown --output output/review.md
      ```

- [x] Optimize performance
  - [x] Review and optimize data processing
  - [x] Improve file handling efficiency
  - [x] Enhance Roo Code interaction patterns
- [x] Add batch processing capability
  - [x] Enable processing multiple entries at once
  - [x] Create summarization tools for large datasets
  - [x] Implement progress reporting for long operations

## Phase 10.5: Workflow Enhancement

- [x] Create separate system prompt files for Annual Review and Competency Assessment
- [x] Update workflow documentation to reference both system prompt files
- [x] Test new system prompts with simple user instructions

## Phase 11: Finalizing and Packaging

- [x] Enhanced System Prompt Organization
  - [x] Created dedicated system prompt files:
    - [x] `.roo/system-prompt-annual-analyst` for Annual Reviews
    - [x] `.roo/system-prompt-competency-analyst` for Competency Assessments
  - [x] Improved user experience:
    - [x] Simplified prompts from 40+ lines to single line
    - [x] Maintained consistent output formatting
    - [x] Added explicit error handling instructions
  - [x] Enhanced maintainability:
    - [x] Separated concerns between review types
    - [x] Clear section boundaries for future updates
    - [x] Added quality check requirements
- [x] Conduct final testing
  - [x] Test with realistic data volume
  - [x] Validate all report formats
  - [x] Check error handling and edge cases

## Phase 12: Future Enhancements (Placeholder)

- [x] Add "self rating" system to annual review that reflects how well achievements align with the criteria on a scale of 1, 2, 3 (Poor, Good, Excellent)
- [x] Refine the `system-prompt-competency-analyst` to add a "self rating" system to better define achievements aligned with criteria on a scale of 1-5, resulting in a final rating
- [x] Simplify the `system-prompt-competency-analyst` file output by removing unnecessary sections like "improvement plan with 3-5 actionable steps" and "areas for improvement for this competency"
- [ ] Prepare for user handover
  - [ ] Create quick start guide
  - [ ] Develop sample walkthroughs
  - [ ] Create troubleshooting reference
- [ ] Finalize project structure
  - [ ] Clean up any temporary files
  - [ ] Organize code for maintainability
  - [ ] Update all documentation to final state
- [ ] Direct Google Sheets API integration without CSV export
- [ ] Web-based interface for report generation
- [ ] Automated scheduling of monthly milestone reports
- [ ] Analytics on accomplishment distribution across criteria
- [ ] Integration with other task tracking systems (e.g., Azure DevOps)

## Notes

- Remember to test frequently throughout development
- Commit code regularly with descriptive commit messages
- Keep credentials secure and never commit them to the repository
- Use environment variables for sensitive information (if using API integration)
- Document as you go to avoid documentation debt
- Keep the Roo Code extension updated to the latest version

# Performance Review Tracking System
## Design Document

**Author:** Claude  
**Version:** 2.0  
**Date:** March 11, 2025

## 1. Introduction

### 1.1 Purpose
This document outlines the design for a Performance Review Tracking System that helps employees track their work accomplishments throughout the year and generate targeted reports for both Annual Reviews and Competency Assessments.

### 1.2 Problem Statement
Employees need to track their work accomplishments and map them to specific criteria required for:
1. Annual Reviews (covering September to August timeframe)
2. Competency Assessments (covering all relevant work since the previous assessment)

Currently, this process is manual, time-consuming, and prone to omissions, as employees must recall and organize their work achievements when review time arrives.

### 1.3 Solution Overview
A streamlined system consisting of:
1. A Google Sheet for continuous documentation of work accomplishments
2. A VS Code-based solution using Roo Code, an AI-powered coding agent
3. Python scripts to process data and generate structured reports
4. Report templates formatted specifically for Annual Reviews and Competency Assessments

## 2. System Architecture

### 2.1 Component Overview

```
[User] → [Google Sheet] → [VS Code + Roo Code] → [Python Scripts] → [Generated Reports]
```

### 2.2 Components

#### 2.2.1 Google Sheet (Data Collection)
A structured spreadsheet where the user records work accomplishments as they occur.

**Key Features:**
- Simple data entry interface
- Consistent structure for all entries
- No manual tagging required (AI will determine relevant criteria)
- Data validation to ensure consistency
- Filterable columns for easy review

#### 2.2.2 VS Code + Roo Code (Processing Environment)
The integrated development environment where data processing and AI analysis occurs.

**Key Features:**
- VS Code as the central development/execution environment
- Roo Code extension providing AI analysis capabilities
- File system access for reading data and writing reports
- Context awareness to reference project files
- Specialized modes for performance review analysis

#### 2.2.3 Python Scripts (Data Processing)
Scripts that extract data from the Google Sheet and prepare it for analysis.

**Key Features:**
- Google Sheets API integration or CSV import
- Date filtering for Annual Reviews
- Data preparation and cleaning
- File handling for intermediate and final outputs

#### 2.2.4 Roo Code AI Analysis (Analysis Engine)
Uses Roo Code to analyze work entries and generate insights based on review criteria.

**Key Features:**
- Pattern recognition across work entries
- Automatic tagging of accomplishments to criteria
- Generating strengths, improvement areas, and action plans
- Crafting cohesive narrative summaries
- Formatting output according to templates

#### 2.2.5 Generated Reports
The final output documents formatted according to the requirements.

**Key Features:**
- Separate reports for Annual Review and Competency Assessment
- Consistent formatting following organizational templates
- Specific examples tied to each criterion
- Action plans for improvement
- Comprehensive summaries

## 3. Detailed Design

### 3.1 Google Sheet Structure

#### 3.1.1 Columns
1. **Date** - When the work was completed (Date format)
2. **Title** - Brief title of the accomplishment (Text)
3. **Description** - Detailed description of the work (Text)
4. **Acceptance Criteria** - What defined success for this work (Text)
5. **Success Notes** - How the work met or exceeded expectations (Text)
6. **Impact** - Significance of the accomplishment (High/Medium/Low dropdown)

Note: Manual tagging columns have been removed as Roo Code will determine relevant criteria.

#### 3.1.2 Data Validation

**Impact Dropdown Values:**
- High
- Medium
- Low

### 3.2 VS Code Project Structure

```
performance-review-tracker/
├── src/
│   ├── data_processor.py
│   ├── report_generator.py
│   └── utils.py
├── templates/
│   ├── annual_review_template.md
│   └── competency_assessment_template.md
├── criteria/
│   ├── annual_review_criteria.json
│   └── competency_assessment_criteria.json
├── data/
│   └── (exported spreadsheet data)
├── output/
│   └── (generated reports)
├── tests/
│   └── (test files)
├── .roo/
│   └── system-prompt-analyst
└── README.md
```

### 3.3 Python Script Functionality

#### 3.3.1 Data Processor Script
The `data_processor.py` script handles loading and preparing data:

```python
import pandas as pd
import json
from datetime import datetime

def load_data(file_path):
    """Load data from CSV or directly from Google Sheets"""
    # Determine file type and load accordingly
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        # Use Google Sheets API
        # ...

def filter_by_date_range(data, start_date, end_date):
    """Filter entries by date range for Annual Review"""
    # Convert string dates to datetime if needed
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Convert data dates to datetime for comparison
    data['Date'] = pd.to_datetime(data['Date'])
    
    # Filter by date range
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    return filtered_data

def prepare_data_for_analysis(data, review_type, year=None):
    """Prepare data for Roo Code analysis"""
    if review_type.lower() == 'annual' and year:
        # Annual review covers Sept to Aug
        start_date = f"{int(year)-1}-09-01"
        end_date = f"{year}-08-31"
        data = filter_by_date_range(data, start_date, end_date)
    
    # Convert to JSON format for Roo Code
    json_data = data.to_json(orient='records', date_format='iso')
    
    # Save to file for Roo Code to access
    output_path = f"data/processed_{review_type.lower()}.json"
    with open(output_path, 'w') as f:
        f.write(json_data)
    
    return output_path

# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Process performance data')
    parser.add_argument('--file', required=True, help='Path to data file')
    parser.add_argument('--type', required=True, choices=['annual', 'competency'], help='Review type')
    parser.add_argument('--year', help='Year for annual review')
    
    args = parser.parse_args()
    
    data = load_data(args.file)
    output_path = prepare_data_for_analysis(data, args.type, args.year)
    print(f"Data processed and saved to {output_path}")
```

#### 3.3.2 Report Generator Script
The `report_generator.py` script handles final report formatting:

```python
import os
import json
import markdown
from docx import Document

def load_roo_code_output(file_path):
    """Load output generated by Roo Code"""
    with open(file_path, 'r') as f:
        return f.read()

def markdown_to_docx(markdown_text, output_path):
    """Convert markdown to DOCX format"""
    doc = Document()
    # Process markdown and add to document
    # ...
    doc.save(output_path)
    return output_path

def generate_final_report(roo_output, review_type, output_format='markdown'):
    """Generate final formatted report"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if output_format.lower() == 'markdown':
        output_path = f"output/{review_type.lower()}_review_{timestamp}.md"
        with open(output_path, 'w') as f:
            f.write(roo_output)
    elif output_format.lower() == 'docx':
        md_path = f"output/{review_type.lower()}_review_{timestamp}.md"
        with open(md_path, 'w') as f:
            f.write(roo_output)
        output_path = md_path.replace('.md', '.docx')
        markdown_to_docx(roo_output, output_path)
    
    return output_path

# Example usage
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate final report')
    parser.add_argument('--input', required=True, help='Path to Roo Code output file')
    parser.add_argument('--type', required=True, choices=['annual', 'competency'], help='Review type')
    parser.add_argument('--format', default='markdown', choices=['markdown', 'docx'], help='Output format')
    
    args = parser.parse_args()
    
    output_path = generate_final_report(load_roo_code_output(args.input), args.type, args.format)
    print(f"Report generated at {output_path}")
```

### 3.4 Roo Code Integration

#### 3.4.1 Custom System Prompt
A custom system prompt will be created for the Analyst mode in `.roo/system-prompt-analyst`:

```
You are Roo in Performance Analyst mode, an AI assistant specialized in analyzing work accomplishments and generating performance reviews.

==== CAPABILITIES
You have expertise in:
- Understanding work accomplishments and their significance
- Mapping accomplishments to specific performance criteria
- Identifying strengths and areas for improvement
- Generating actionable improvement plans
- Creating comprehensive, well-structured reports

==== REVIEW CRITERIA

For ANNUAL REVIEWS, apply these criteria:
- Communication: Gives full attention, limits interruptions, responds to direction/coaching/criticism appropriately, expresses ideas clearly, communicates positively/timely/effectively
- Flexibility: Adapts to changing priorities, adjusts work methods to meet new needs, open to new approaches
- Initiative: Self-directed, proactive in finding solutions, takes on additional responsibilities
- Member Service: Prioritizes member needs, provides excellent service, builds positive relationships
- Personal Credibility: Trustworthy, reliable, follows through on commitments, demonstrates integrity
- Quality and Quantity of Work: Produces high-quality work, meets deadlines, manages workload effectively
- Teamwork: Collaborates effectively, shares information, supports team goals, fosters positive relationships

For COMPETENCY ASSESSMENTS, apply these criteria:
- Accountability: Takes responsibility, meets commitments, admits/learns from mistakes
- Agility: Adapts quickly, embraces change, maintains effectiveness during uncertainty
- Inclusion: Values diverse perspectives, creates inclusive environment, ensures equitable participation
- Influence: Persuades effectively, builds consensus, inspires action
- Innovation: Generates creative solutions, challenges status quo, implements improvements
- Problem Management: Identifies issues, determines root causes, implements effective solutions
- Programming/Software Development: Writes efficient code, follows best practices, creates maintainable solutions
- Project Management: Plans effectively, manages resources, delivers on time/budget
- Release and Deployment: Manages releases smoothly, minimizes disruption, ensures quality
- Requirements Definition and Management: Gathers/documents requirements, manages scope, ensures traceability
- Solution Architecture: Designs scalable solutions, makes appropriate technology choices, considers business needs
- Systems Design: Creates effective system designs, considers integration points, focuses on user needs
- Testing: Develops comprehensive test plans, identifies defects, ensures quality

==== TASK FRAMEWORK
When analyzing performance data:
1. Carefully read each work accomplishment
2. For each entry, determine which Annual Review and/or Competency Assessment criteria it demonstrates
3. Group accomplishments by criteria
4. For each criterion with matching accomplishments:
   a. Identify 2-4 specific examples that best demonstrate this criterion
   b. Determine 1-2 areas for improvement based on the criterion definition
   c. Create a concrete, actionable improvement plan
   d. Write a concise summary paragraph highlighting strengths and improvement areas
5. Format the output according to the specified template

==== OUTPUT FORMAT
Always format your analysis into a structured report following this pattern for each criterion:

# [Criterion Name]

## Expectations
- [List the specific expectations for this criterion]

## How I Met This Criterion
- [Specific example from work entries with details]
- [Another specific example from work entries]
- [Additional example if applicable]

## Areas for Improvement
- [Specific area identified based on the criterion]
- [Another area if applicable]

## Improvement Plan
[Concrete, actionable steps for improvement]

## Summary
[Concise paragraph summarizing performance, examples, areas for improvement, and growth plan]
```

#### 3.4.2 Workflow with Roo Code
The typical workflow would involve:

1. Process data using Python script:
   ```bash
   python src/data_processor.py --file data/accomplishments.csv --type annual --year 2025
   ```

2. Use Roo Code to analyze the data:
   ```
   @/data/processed_annual.json I need to generate an Annual Review report using this data. 
   Please analyze each work entry, determine which criteria they satisfy, and create a structured 
   report following the annual review template. Include specific examples for each criterion, areas
   for improvement, an improvement plan, and a summary paragraph.
   ```

3. Roo Code generates the analysis in Markdown format

4. (Optional) Convert to DOCX if needed:
   ```bash
   python src/report_generator.py --input output/roo_analysis.md --type annual --format docx
   ```

### 3.5 Output Report Format

The output report formats remain the same as in the original design:

#### 3.5.1 Annual Review Report

```
# Annual Review [Year]
[September 1, YYYY - August 31, YYYY]

## 1. Communication

### Expectations
- Gives members full attention
- Limits interruptions while others are communicating
- Appropriately responds to direction, coaching, or criticism
- Expresses ideas clearly and in an organized way
- Communicates in a positive, timely, and effective manner

### How I Met This Criterion
- [Specific example from work entries with details]
- [Another specific example from work entries]
- [Additional example if applicable]

### Areas for Improvement
- [Specific area identified based on the criterion]
- [Another area if applicable]

### Improvement Plan
[Concrete, actionable steps for improvement]

### Summary
[Concise paragraph summarizing performance, examples, areas for improvement, and growth plan]

## 2. Flexibility
[Same structure as above]

[Continues for all Annual Review criteria]
```

#### 3.5.2 Competency Assessment Report

```
# Competency Assessment [Date]

## 1. Accountability

### Expectations
- [List of specific expectations for this competency]

### How I Met This Criterion
- [Specific example from work entries with details]
- [Another specific example from work entries]
- [Additional example if applicable]

### Areas for Improvement
- [Specific area identified based on the criterion]
- [Another area if applicable]

### Improvement Plan
[Concrete, actionable steps for improvement]

### Summary
[Concise paragraph summarizing performance, examples, areas for improvement, and growth plan]

## 2. Agility
[Same structure as above]

[Continues for all Competency Assessment criteria]
```

## 4. Implementation Plan

### 4.1 Development Phases

#### 4.1.1 Phase 1: VS Code Project Setup
- Set up VS Code project structure
- Install Roo Code extension
- Create custom system prompt for Analyst mode
- Test basic Roo Code functionality

#### 4.1.2 Phase 2: Google Sheet Setup
- Create Google Sheet with simplified structure
- Set up data validation for dropdown menus
- Create simple input instructions
- Test with sample data entries

#### 4.1.3 Phase 3: Python Script Development
- Develop data processor script
- Implement data extraction and preparation
- Create report generator script
- Test with sample data

#### 4.1.4 Phase 4: Roo Code Integration
- Finalize custom system prompt
- Create criteria definition files
- Test analysis quality with sample data
- Refine prompt based on test results

#### 4.1.5 Phase 5: Output Formatting
- Create report templates
- Implement formatting options
- Test report generation
- Add export options (markdown, docx)

### 4.2 Technology Stack

#### 4.2.1 Frontend
- Google Sheets (data entry interface)
- VS Code with Roo Code extension (development environment)

#### 4.2.2 Backend
- Python 3.9+
- Libraries:
  - pandas (data processing)
  - gspread (optional, for Google Sheets API)
  - python-docx (document creation)
  - markdown (markdown processing)
  - argparse (command line interface)

#### 4.2.3 Tools
- VS Code
- Roo Code extension
- Google Sheets

### 4.3 Security Considerations
- Data remains local within VS Code environment
- No API keys needed for basic functionality (CSV export/import)
- Google Sheets credentials only needed if using direct API integration
- No sensitive data transmitted to external services

## 5. Usage Instructions

### 5.1 Google Sheet Setup
1. Create a new Google Sheet or use the provided template
2. Set up columns with appropriate data validation
3. Record accomplishments throughout the year

### 5.2 Generating Reports with Roo Code
1. Export Google Sheet data to CSV (or use API integration)
2. Process data using Python script:
   ```bash
   python src/data_processor.py --file data/accomplishments.csv --type annual --year 2025
   ```
3. Open VS Code and switch to Analyst mode in Roo Code
4. Ask Roo Code to analyze the data:
   ```
   @/data/processed_annual.json I need to generate an Annual Review report using this data. 
   Please analyze each work entry, determine which criteria they satisfy, and create a structured 
   report following the annual review template.
   ```
5. Review the generated report
6. (Optional) Convert to DOCX if needed:
   ```bash
   python src/report_generator.py --input output/roo_analysis.md --type annual --format docx
   ```

### 5.3 Recording Work Accomplishments
1. Enter new accomplishments as they occur
2. Ensure all fields are completed
3. Add any additional notes or context
4. No need to manually tag entries with criteria

## 6. Maintenance and Support

### 6.1 Regular Maintenance
- Update criteria definitions as organizational requirements change
- Keep Roo Code extension updated to latest version
- Refresh the custom system prompt as needed

### 6.2 Troubleshooting
- Check file paths if data loading fails
- Verify VS Code and Roo Code are properly installed
- Ensure Google Sheet format hasn't been modified

## 7. Future Enhancements

### 7.1 Potential Additions
- Direct Google Sheets API integration without CSV export
- Web-based interface for running reports (vs. command line)
- Automated scheduling of monthly milestone reports
- Analytics on accomplishment distribution across categories
- Integration with other task tracking systems (e.g., Azure DevOps)

### 7.2 Roadmap
1. Core functionality (current design)
2. Improved user interface
3. Direct API integration
4. Advanced analytics and insights
5. Integration with additional systems

## 8. Appendices

### 8.1 Sample Data Format
```json
[
  {
    "Date": "2024-10-15",
    "Title": "Automation Bridge User's Guide",
    "Description": "Created comprehensive documentation for the Automation Bridge system",
    "Acceptance Criteria": "Complete guide with all features documented, approved by stakeholders",
    "Success Notes": "Guide received positive feedback and is now the main reference for team members",
    "Impact": "High"
  },
  {
    "Date": "2024-11-22",
    "Title": "Load Runner Enterprise Usage Report",
    "Description": "Developed automated reporting system for Load Runner usage",
    "Acceptance Criteria": "Accurate daily usage statistics with user breakdown",
    "Success Notes": "Report helped identify usage patterns and optimize licensing costs",
    "Impact": "Medium"
  }
]
```

### 8.2 Roo Code Prompt Example
```
@/data/processed_annual.json I need to generate an Annual Review report using this data. 
Please analyze each work entry, determine which criteria they satisfy, and create a structured 
report following the annual review template. Include specific examples for each criterion, areas
for improvement, an improvement plan, and a summary paragraph.
```

### 8.3 Sample Report Output
See sections 3.5.1 and 3.5.2 for the detailed report structure.

## 9. Conclusion

This updated Performance Review Tracking System design leverages VS Code with Roo Code to provide a more integrated and efficient solution. By using Roo Code's AI capabilities directly within the VS Code environment, we've eliminated the need for external API calls while maintaining the system's core functionality.

Key improvements in this design include:
- Removal of manual tagging requirements (AI determines relevant criteria)
- Local development environment without external API dependencies
- Direct file system access for reading data and writing reports
- Simplified workflow with fewer components
- Enhanced flexibility through custom VS Code integration

This approach significantly reduces the time and effort required for review preparation while increasing the quality and comprehensiveness of the resulting documents, meeting the original objectives with a more streamlined implementation.

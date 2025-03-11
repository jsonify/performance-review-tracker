# Performance Review Tracking System
## Design Document

**Author:** Claude
**Version:** 1.0
**Date:** March 10, 2025

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
2. A Python script that processes this data and uses Claude to analyze and generate structured reports
3. Report templates formatted specifically for Annual Reviews and Competency Assessments

## 2. System Architecture

### 2.1 Component Overview

```
[User] → [Google Sheet] → [Python Script] → [Claude API] → [Generated Reports]
```

### 2.2 Components

#### 2.2.1 Google Sheet (Data Collection)
A structured spreadsheet where the user records work accomplishments as they occur.

**Key Features:**
- Simple data entry interface
- Consistent structure for all entries
- Tagging system for both Annual Review and Competency Assessment criteria
- Data validation to ensure consistency
- Filterable columns for easy review

#### 2.2.2 Python Script (Data Processing)
A script that extracts data from the Google Sheet, formats it appropriately, and sends it to Claude.

**Key Features:**
- Google Sheets API integration
- Date filtering for Annual Reviews
- Structured data formatting for Claude
- Claude API integration
- Report file generation and management

#### 2.2.3 Claude API (Analysis Engine)
Uses Claude to analyze the work entries and generate insights based on review criteria.

**Key Features:**
- Pattern recognition across work entries
- Mapping accomplishments to specific criteria
- Generating strengths, improvement areas, and action plans
- Crafting cohesive narrative summaries
- Formatting output according to templates

#### 2.2.4 Generated Reports
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
6. **Annual Review Tags** - Categories relevant to annual review (Multi-select dropdown)
7. **Competency Tags** - Categories relevant to competency assessment (Multi-select dropdown)
8. **Impact** - Significance of the accomplishment (High/Medium/Low dropdown)

#### 3.1.2 Data Validation

**Annual Review Tags Dropdown Values:**
- Communication
- Flexibility
- Initiative
- Member Service
- Personal Credibility
- Quality and Quantity of Work
- Teamwork

**Competency Tags Dropdown Values:**
- Accountability
- Agility
- Inclusion
- Influence
- Innovation
- Problem Management
- Programming/Software Development
- Project Management
- Release and Deployment
- Requirements Definition and Management
- Solution Architecture
- Systems Design
- Testing

**Impact Dropdown Values:**
- High
- Medium
- Low

### 3.2 Python Script Functionality

#### 3.2.1 Script Workflow
1. Read configuration (API keys, file paths, etc.)
2. Connect to Google Sheets API
3. Load data from the specified sheet
4. Process data (filtering, formatting)
5. Prepare Claude prompt with appropriate template
6. Send to Claude API
7. Receive and format Claude's response
8. Save output as formatted document
9. Provide confirmation to user

#### 3.2.2 Configuration Parameters
- Google Sheets API credentials
- Claude API key
- Google Sheet ID
- Output file path/format preferences
- Review type (Annual or Competency)
- Date range for Annual Review (if applicable)

#### 3.2.3 Error Handling
- Sheet access errors
- API rate limiting
- Invalid data formats
- Claude API errors
- File writing errors

### 3.3 Claude Integration

#### 3.3.1 Prompt Template

```
# Performance Review Analysis Request

## Data Context
<data>
[Your Google Sheet data would be inserted here by the script in JSON or CSV format]
</data>

## Review Type
[ANNUAL_REVIEW or COMPETENCY_ASSESSMENT]

## Time Period
Start Date: [For Annual Review: September 1, 2024]
End Date: [For Annual Review: August 31, 2025]

## Criteria Definitions

### Annual Review Criteria
- COMMUNICATION: Gives members full attention, limits interruptions while others are communicating, appropriately responds to direction/coaching/criticism, expresses ideas clearly and in an organized way, communicates in a positive/timely/effective manner
- FLEXIBILITY: [Definition...]
[Remaining criteria with their definitions...]

### Competency Assessment Criteria
- ACCOUNTABILITY: [Definition...]
- AGILITY: [Definition...]
[Remaining criteria with their definitions...]

## Output Format Instructions
Please analyze the provided work entries and generate a comprehensive review following this structure for each applicable criterion:

<topic>
[CRITERION_NAME]
</topic>

<topic_examples>
[List of expectations for this criterion]
</topic_examples>

<comments>
<how_i_did>
[2-4 bullet points with specific examples from my work entries that demonstrate how I met this criterion]
</how_i_did>

<areas_to_improve>
[1-2 bullet points identifying realistic areas for improvement based on the criterion definition and my work entries]
</areas_to_improve>

<improvement_plan>
[A concrete, actionable plan for how I will improve in these areas over the next review period]
</improvement_plan>

<final_review>
[A concise paragraph summarizing my performance in this criterion, highlighting strengths with specific examples, acknowledging areas for improvement, and outlining my plan for growth]
</final_review>
</comments>
```

#### 3.3.2 Claude API Parameters
- Model: claude-3-7-sonnet-20250219 (or latest available version)
- Temperature: 0.3 (lower for factual consistency)
- Max tokens: 8000 (to allow for comprehensive responses)
- System prompt: Custom instructions for review generation

### 3.4 Output Report Format

#### 3.4.1 Annual Review Report

The Annual Review Report will follow this structure:

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

#### 3.4.2 Competency Assessment Report

The Competency Assessment Report will follow this structure:

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

#### 4.1.1 Phase 1: Google Sheet Setup
- Create Google Sheet with defined structure
- Set up data validation for dropdown menus
- Create simple input instructions
- Test with sample data entries

#### 4.1.2 Phase 2: Python Script Development
- Set up Google Sheets API access
- Develop data extraction functionality
- Create data filtering capabilities
- Implement configuration options
- Test with sample data

#### 4.1.3 Phase 3: Claude Integration
- Finalize prompt templates
- Set up Claude API integration
- Test analysis quality with sample data
- Refine prompt based on test results
- Implement error handling

#### 4.1.4 Phase 4: Output Formatting
- Create report formatting functionality
- Implement template structure
- Test report generation
- Add export options (docx, PDF, etc.)
- Finalize user interface

### 4.2 Technology Stack

#### 4.2.1 Frontend
- Google Sheets (data entry interface)

#### 4.2.2 Backend
- Python 3.9+
- Libraries:
  - gspread (Google Sheets API)
  - google-auth (Authentication)
  - anthropic (Claude API)
  - python-docx (Document creation)
  - argparse (Command line interface)

#### 4.2.3 APIs
- Google Sheets API
- Claude API

### 4.3 Security Considerations
- API keys stored securely (environment variables or secure config)
- Limited Google Sheets permissions (read-only for script)
- Data remains within user's Google account
- No persistent storage of work data by the script
- Rate limiting implementation for API calls

## 5. Usage Instructions

### 5.1 Google Sheet Setup
1. Create a new Google Sheet or use the provided template
2. Set up columns with appropriate data validation
3. Share with any relevant collaborators (optional)

### 5.2 Recording Work Accomplishments
1. Enter new accomplishments as they occur
2. Ensure all fields are completed
3. Tag with relevant Annual Review and Competency Assessment categories
4. Add any additional notes or context

### 5.3 Generating Reports
1. Run the Python script with appropriate parameters:
   ```
   python review_generator.py --type [annual|competency] --sheet-id [SHEET_ID] --output [OUTPUT_PATH]
   ```
2. For Annual Reviews, specify the year:
   ```
   python review_generator.py --type annual --year 2025 --sheet-id [SHEET_ID] --output [OUTPUT_PATH]
   ```
3. Review the generated document
4. Make any manual adjustments as needed
5. Finalize for submission

## 6. Maintenance and Support

### 6.1 Regular Maintenance
- Update criteria definitions as organizational requirements change
- Refresh API keys when needed
- Update Claude model version when improved versions are available

### 6.2 Troubleshooting
- Check Google Sheets permissions if data access fails
- Verify API keys if Claude integration fails
- Ensure Google Sheet format hasn't been modified
- Check for rate limiting issues if multiple reports are generated in succession

## 7. Future Enhancements

### 7.1 Potential Additions
- Web-based interface for running reports (vs. command line)
- Email notification when reports are ready
- Integration with other task tracking systems (e.g., Azure DevOps)
- Automated scheduling of monthly milestone reports
- Analytics on accomplishment distribution across categories
- Collaborative review features for team feedback

### 7.2 Roadmap
1. Core functionality (current design)
2. Improved user interface
3. Integration with additional systems
4. Advanced analytics and insights
5. Team collaboration features

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
    "Annual Review Tags": ["Communication", "Quality and Quantity of Work"],
    "Competency Tags": ["Documentation", "Technical Writing"],
    "Impact": "High"
  },
  {
    "Date": "2024-11-22",
    "Title": "Load Runner Enterprise Usage Report",
    "Description": "Developed automated reporting system for Load Runner usage",
    "Acceptance Criteria": "Accurate daily usage statistics with user breakdown",
    "Success Notes": "Report helped identify usage patterns and optimize licensing costs",
    "Annual Review Tags": ["Initiative", "Quality and Quantity of Work"],
    "Competency Tags": ["Programming/Software Development", "Innovation"],
    "Impact": "Medium"
  }
]
```

### 8.2 Claude Prompt Examples
See section 3.3.1 for the detailed prompt template.

### 8.3 Sample Report Output
See sections 3.4.1 and 3.4.2 for the detailed report structure.

## 9. Conclusion

This Performance Review Tracking System provides a streamlined, efficient approach to documenting and reporting work accomplishments for both Annual Reviews and Competency Assessments. By maintaining a single source of truth in the Google Sheet and leveraging Claude's analysis capabilities, users can generate comprehensive, well-structured reviews with minimal manual effort.

The system follows KISS and DRY principles by:
- Using a single data entry point for all accomplishments
- Automating the analysis and categorization process
- Generating standardized reports from the same data source
- Providing flexibility for both automated and manual workflows

This approach significantly reduces the time and effort required for review preparation while increasing the quality and comprehensiveness of the resulting documents.

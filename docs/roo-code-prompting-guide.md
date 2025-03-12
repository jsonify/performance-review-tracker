# Roo Code Prompting Guide for Performance Reviews

## Overview

This guide provides examples and best practices for using Roo Code to analyze work accomplishments and generate performance review reports.

## Basic Command Structure

```bash
@/path/to/data.json [review type] [additional parameters]
```

## Sample Prompts

### 1. Annual Review Generation

```bash
@/data/processed_annual.json Please generate an Annual Review report for the period Sept 2024 - Aug 2025. Focus on technical achievements and their impact on team goals.
```

#### Parameters to Include:
- Time period
- Focus areas (optional)
- Special considerations (optional)

### 2. Competency Assessment

```bash
@/data/processed_competency.json Please analyze my technical competencies with emphasis on Software Development and Solution Architecture. Include specific project examples from Q1-Q2 2025.
```

#### Parameters to Include:
- Key competencies to emphasize
- Time period (if relevant)
- Project context (optional)

### 3. Focused Criteria Analysis

```bash
@/data/processed_annual.json Please analyze my performance specifically for the Quality of Work and Initiative criteria. Include quantifiable metrics where possible.
```

#### Parameters to Include:
- Specific criteria to analyze
- Metrics focus (optional)
- Context requirements (optional)

## Context Mention Patterns

### 1. File References
- Always use the full path: `@/data/processed_annual.json`
- Include relevant date ranges in the prompt
- Specify output format preferences
- Use consistent file naming patterns:
  * `processed_annual.json` for annual reviews
  * `processed_competency.json` for competency assessments
  * `processed_custom_YYYYMM.json` for custom periods

### 2. Criteria References
- Use exact names from criteria definitions
- Group related criteria when relevant
- Specify primary vs secondary focus areas
- Examples:
  * Technical: "Programming/Software Development, Solution Architecture, Systems Design"
  * Leadership: "Communication, Initiative, Personal Credibility"
  * Project: "Project Management, Requirements Definition, Release and Deployment"

### 3. Project References
- Include project names and timeframes
- Mention specific roles or responsibilities
- Reference team context when relevant
- Format: `[Project Name] ([Time Period]) - [Role/Context]`
- Examples:
  * "API Modernization (Q1-Q2 2025) - Technical Lead"
  * "Cloud Migration (2024-09 to 2025-03) - Senior Developer"

### 4. Testing Scenarios

#### Basic Testing
```bash
@/data/processed_annual.json Please verify the data structure and generate a sample paragraph for the Communication criterion to test output formatting.
```

#### Data Validation
```bash
@/data/processed_annual.json Please analyze the data completeness for all criteria and identify any missing or incomplete areas that need attention.
```

#### Format Testing
```bash
@/data/processed_competency.json Please generate a sample report section with all standard components (expectations, examples, improvements, plan, summary) to verify formatting.
```

#### Edge Cases
```bash
@/data/processed_annual.json Please analyze the data handling special characters, very long descriptions, and entries spanning multiple criteria.
```

## Advanced Usage

### 1. Multi-Criteria Analysis

```bash
@/data/processed_annual.json Please analyze my performance across all technical criteria (Programming, Architecture, System Design) with emphasis on how they interconnect. Consider projects from both Q1 and Q2 2025.
```

### 2. Impact Analysis

```bash
@/data/processed_annual.json Please analyze high-impact achievements across all criteria, focusing on quantifiable business value and team influence.
```

### 3. Growth Analysis

```bash
@/data/processed_competency.json Please analyze my technical growth trajectory, highlighting progression in Solution Architecture and System Design competencies over the past 6 months.
```

## Common Scenarios

### 1. New Role Transition

```bash
@/data/processed_annual.json Please analyze my performance considering my role transition in March 2025 from Senior Developer to Technical Lead, with emphasis on leadership growth.
```

### 2. Cross-Team Impact

```bash
@/data/processed_competency.json Please analyze my contributions focusing on cross-team collaboration and influence, particularly in the API modernization project.
```

### 3. Technical Leadership

```bash
@/data/processed_annual.json Please analyze my technical leadership impact, focusing on mentoring, architecture decisions, and team enablement.
```

## Troubleshooting Guide

### 1. Incomplete Data

If data is missing or incomplete:
```bash
@/data/processed_annual.json Please analyze available data, noting any gaps. For the Testing competency, focus on Q2 data as Q1 records are incomplete.
```

### 2. Complex Projects

For long-running or complex projects:
```bash
@/data/processed_competency.json Please analyze the Cloud Migration project phases separately, then provide an overall impact assessment.
```

### 3. Role Changes

When responsibilities have shifted:
```bash
@/data/processed_annual.json Please analyze my performance with special consideration for the role change in March. Weight recent leadership activities appropriately.
```

### 4. Common Issues and Solutions

#### Issue: Missing Context
**Problem:** Analysis lacks specific project details
**Solution:** Include project names, dates, and roles explicitly:
```bash
@/data/processed_annual.json Please analyze my contributions to [Project Name] ([Dates]) as [Role], focusing on [specific criteria].
```

#### Issue: Criteria Mismatch
**Problem:** Analysis doesn't map well to intended criteria
**Solution:** Explicitly list relevant criteria and their relationships:
```bash
@/data/processed_competency.json Please analyze how my work on [Project] demonstrates [Criterion 1], particularly in relation to [Criterion 2].
```

#### Issue: Timeline Gaps
**Problem:** Analysis shows gaps in activity
**Solution:** Acknowledge and explain gaps:
```bash
@/data/processed_annual.json Please note the planned project transition period in Q2 when analyzing the timeline of achievements.
```

## Best Practices

1. **Be Specific**
   - Include relevant dates
   - Name specific projects
   - Reference particular criteria
   - Mention desired focus areas

2. **Provide Context**
   - Mention role changes
   - Include team context
   - Reference organizational changes
   - Note special circumstances

3. **Request Metrics**
   - Ask for quantifiable impacts
   - Request specific examples
   - Include business value metrics
   - Reference project outcomes

4. **Consider Timeframes**
   - Specify review periods
   - Note any partial periods
   - Mention phase transitions
   - Include project timelines

5. **Focus Direction**
   - Prioritize key areas
   - Request balanced analysis
   - Specify depth vs breadth
   - Include growth focus

6. **Data Organization**
   - Use clear file naming
   - Maintain data structure
   - Include all required fields
   - Validate data completeness

7. **Context Clarity**
   - Use consistent terminology
   - Reference official criteria names
   - Include role context
   - Specify reporting preferences

## Example Data Scenarios

### 1. Annual Review with Role Change

```json
{
  "reviewType": "annual",
  "period": "2024-09-01 to 2025-08-31",
  "roleChange": {
    "date": "2025-03-15",
    "from": "Senior Developer",
    "to": "Technical Lead"
  }
}
```

### 2. Competency Focus Areas

```json
{
  "reviewType": "competency",
  "primaryFocus": [
    "Solution Architecture",
    "Technical Leadership"
  ],
  "projects": [
    "API Modernization",
    "Cloud Migration"
  ]
}
```

### 3. Project-Based Analysis

```json
{
  "reviewType": "annual",
  "projects": [
    {
      "name": "API Modernization",
      "role": "Technical Lead",
      "period": "2025-01 to 2025-06",
      "primaryCriteria": [
        "Solution Architecture",
        "Technical Leadership",
        "Project Management"
      ]
    }
  ]
}
```

Remember to keep prompts clear, specific, and focused on the desired analysis outcomes. Include relevant context and any special considerations that might impact the analysis.

## Testing Strategy

### 1. Data Validation Testing
Test data completeness and structure:
```bash
@/data/processed_annual.json Please verify data completeness and required fields for all entries.
```

### 2. Criteria Coverage Testing
Ensure all relevant criteria are considered:
```bash
@/data/processed_competency.json Please analyze criteria coverage and identify any areas lacking sufficient examples.
```

### 3. Timeline Analysis Testing
Verify proper handling of time periods:
```bash
@/data/processed_annual.json Please validate date ranges and entry distribution across the review period.
```

### 4. Format Verification Testing
Check output formatting:
```bash
@/data/processed_annual.json Please generate a sample report section to verify markdown formatting and structure.
```

Remember to test with various scenarios and data combinations to ensure robust analysis and reporting.
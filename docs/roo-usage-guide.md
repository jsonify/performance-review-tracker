# Roo Usage Guide

## Competency Assessment vs Annual Review

The system supports two distinct types of reviews, each with its own prompt and usage pattern:

### 1. Competency Assessment

Use this format to generate a competency-based assessment with ratings:

```
@/data/accomplishments.csv
'.roo/system-prompt-competency-analyst'
Please generate my competency assessment.
```

This will:
- Analyze accomplishments against 13 competency criteria
- Provide 1-5 ratings for each competency
- Include evidence and detailed justifications
- Focus on demonstrating competency levels

### 2. Annual Review

Use a different format for annual performance reviews:

```
'data/accomplishments.csv' (see below for file content)
'.roo/system-prompt-annual-review' (see below for file content)
Please generate my annual review.
```

This will:
- Provide a calendar year-based review
- Focus on overall impact and achievements
- Include forward-looking goals
- Align with annual review formats

## Using Roo's Performance Review Analyst Mode

1. Open VS Code
2. Switch to Performance Review Analyst mode
3. Choose the appropriate prompt and format based on your needs:
   - Use system-prompt-competency-analyst for competency assessments
   - Use system-prompt-annual-review for annual reviews
4. Reference both the data file and prompt file as shown above
5. Use the exact phrasing to specify which type of review you want

## Best Practices

1. Be explicit about which type of review you want
2. Always reference both the data file and appropriate prompt
3. Use the exact phrases:
   - "Please generate my competency assessment"
   - "Please generate my annual review"
4. Keep accomplishments data up to date
5. Review the appropriate prompt file before generating to ensure it meets your needs

## Automated Alternative

For batch processing or quick competency assessments, you can also use the automated system:

```bash
./scripts/run_assessment.sh --fresh
```

This uses the same rating system and format but processes accomplishments automatically rather than through Roo's analysis.

Choose the method that best fits your needs:
- Roo Analysis: For nuanced, detailed reviews requiring AI insight
- Automated System: For batch processing or quick assessments

See the main README for more details on the automated system.
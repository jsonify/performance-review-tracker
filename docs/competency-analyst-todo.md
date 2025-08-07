# Competency Analyst Implementation Todo List

## Goals
- Simplify the competency assessment output
- Add 1-5 rating system based on competencies-formatted.csv
- Focus purely on assessment of current achievements, not future improvements

## Implementation Tasks

1. [ ] Modify system-prompt-competency-analyst:
   - Remove sections for improvement plans and areas for improvement
   - Add rating scale definitions from competencies-formatted.csv
   - Update output format to show only:
     * Rating (1-5)
     * Supporting evidence from accomplishments
     * Brief justification of rating

2. [ ] Create new output format template:
```markdown
## [Competency Name]

**Rating:** [1-5]

**Evidence:**
- [Specific accomplishment that demonstrates this competency]
- [Additional accomplishment if applicable]

**Justification:**
[Brief explanation of why this rating was chosen, referencing the rating definition from competencies-formatted.csv]
```

3. [ ] Test with sample accomplishments:
   - Verify rating accuracy
   - Check evidence selection
   - Validate justification clarity

4. [ ] Documentation updates:
   - Update prompting guide
   - Add rating scale reference
   - Include example outputs

## Rating Scale Reference (1-5)
1. Learning - Just starting to apply the competency
2. Developing - Building basic competency
3. Practicing - Demonstrating solid competency
4. Mastering - Leading and teaching others
5. Leading - Setting direction and driving innovation

## Notes
- Focus on evidence-based assessment
- Use specific accomplishments to justify ratings
- Ensure justifications reference the rating scale definitions
- Remove any forward-looking or improvement-focused content
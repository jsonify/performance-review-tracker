# Competency Analyst System Simplification Implementation Plan

## 1. Goals

- Simplify the output of the `system-prompt-competency-analyst` to focus on concise assessment.
- Implement a 1-5 rating system for each competency, based on definitions in `data/competencies-formatted.csv`.
- Ensure the assessment is based purely on provided accomplishments (`data/accomplishments.csv`), removing any forward-looking improvement plans or areas for improvement.
- Create a more elegant and robust system prompt that aligns with KISS and DRY principles.

## 2. Current System Analysis

The current `system-prompt-competency-analyst` is designed to provide a detailed analysis of work accomplishments against 13 competency criteria. It includes:

- **Detailed sections for each competency:** "How I Met This Criterion," "Areas for Improvement," "Improvement Plan," and "Summary."
- **Focus on identifying improvement areas and creating actionable plans.**
- **Prescriptive output format.**

Limitations of the current system for the user's current need:

- **Over-engineered for a simple assessment:** The detailed improvement plans and areas for improvement are not needed for the current task, which is focused on evaluating current performance.
- **Lacks a clear rating system:**  The current system provides qualitative analysis but no explicit rating scale for each competency.

## 3. Proposed System Design

The simplified `system-prompt-competency-analyst` will focus on providing a concise, rating-based assessment of each competency. The key elements of the proposed design are:

- **Rating Scale:** Utilize the 1-5 rating scale defined in `data/competencies-formatted.csv` (1 - Learning, 2 - Developing, 3 - Practicing, 4 - Mastering, 5 - Leading).
- **Output Structure per Competency:**
    ```markdown
    ## [Competency Name]

    **Rating:** [1-5]

    **Evidence:**
    - [Specific accomplishment from data/accomplishments.csv that demonstrates this competency]
    - [Optional: Additional accomplishment]

    **Justification:**
    [Brief explanation of the rating, referencing the rating definition from data/competencies-formatted.csv and the provided evidence.]
    ```
- **Focus on Evidence-Based Assessment:** The rating and justification must be directly supported by specific examples from the `data/accomplishments.csv` file.
- **Removal of Improvement-Focused Sections:**  Eliminate "Areas for Improvement" and "Improvement Plan" sections to align with the user's requirement for a purely assessment-focused output.

## 4. Implementation Steps

The implementation will follow these steps, as outlined in `docs/competency-analyst-todo.md`:

1. **Modify `system-prompt-competency-analyst`:**
   - [ ] Remove sections for improvement plans and areas for improvement.
   - [ ] Add rating scale definitions from `data/competencies-formatted.csv` as context.
   - [ ] Update output format instructions to reflect the simplified structure (Rating, Evidence, Justification).

2. **Create New Output Format Template:** (Already defined in `docs/competency-analyst-todo.md`)

3. **Test with Sample Accomplishments:**
   - [ ] Use sample data from `data/accomplishments.csv` to test the modified system prompt.
   - [ ] Verify rating accuracy against the definitions in `data/competencies-formatted.csv`.
   - [ ] Check that evidence selection is relevant and supports the rating.
   - [ ] Validate that justifications are clear and concise.

4. **Documentation Updates:**
   - [ ] Update the prompting guide (`docs/roo-code-prompting-guide.md`) to reflect the changes in the `system-prompt-competency-analyst`.
   - [ ] Add a rating scale reference to the documentation.
   - [ ] Include example outputs in the documentation to demonstrate the new format.

## 5. Testing Strategy

- **Unit Testing (Prompt Level):**  Test the modified `system-prompt-competency-analyst` with various sample accomplishments from `data/accomplishments.csv`. Manually review the output to ensure:
    - Ratings are aligned with the competency definitions and provided evidence.
    - Evidence is relevant and accurately reflects the accomplishments.
    - Justifications are clear, concise, and logically sound.
    - Output format adheres to the new simplified template.
- **Qualitative Review:**  Evaluate the overall quality and usefulness of the simplified competency assessments. Ensure that the output provides valuable insights into performance based on the provided accomplishments.

## 6. Rollback Plan

If the simplified system prompt does not perform as expected or if the user is not satisfied with the results, we can easily rollback to the previous version by:

1. **Reverting the changes to `system-prompt-competency-analyst`:**  Replace the modified content with the original content of the file.
2. **Deleting the new todo list and implementation plan documents** (optional, for cleanliness).

This rollback process is straightforward as we are primarily modifying a single system prompt file.

## 7. Timeline

- **Implementation of System Prompt Changes (Step 1 & 2):** 1-2 hours
- **Testing and Validation (Step 3 & 5):** 2-3 hours
- **Documentation Updates (Step 4):** 1-2 hours
- **Total Estimated Time:** 4-7 hours

This timeline is an estimate and may vary based on the complexity of testing and any unforeseen issues during implementation.

---

This implementation plan provides a detailed roadmap for simplifying the `system-prompt-competency-analyst`. Please review it and let me know if you have any feedback or adjustments.
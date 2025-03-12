# Plan for Modifying Performance Review Analyst Mode

## Objective

Modify the Performance Review Analyst mode to use the `data/accomplishments.csv` file instead of `processed_annual.json`, and generate output similar to `output/sample_analysis.md`.

## 1. Gather Information:

*   Read the contents of `docs/roo-code-prompting-guide.md` to understand how the prompts are structured and how they reference the data file.
*   Read the contents of `data/accomplishments.csv` to understand its structure and how it can be used to generate the performance review.
*   Read the contents of `output/sample_analysis.md` to understand the desired output format.
*   Examine the `src/main.py` file, as this is likely where the main logic for the performance review analysis resides.
*   Search for the string "processed\_annual.json" in the codebase to identify where the file is being referenced.
*   Read the contents of `docs/performance-review-tracking-system-design-document.md` and `docs/workflow-automation-plan.md` to understand the data requirements and workflow.
*   Read the contents of `templates/annual_review_template.md` to understand the structure of the annual review template.

## 2. Modify the Code:

*   Modify the `src/main.py` file to use the `data/accomplishments.csv` file as input.
*   Modify the `src/main.py` file to call the `src/data_processor.py` script to process the CSV data and generate the JSON file.
*   Modify the `src/main.py` file to pass the generated JSON file to Roo Code for analysis.
*   Update the code to generate output in the format of `output/sample_analysis.md`.
*   Update any prompts in `docs/roo-code-prompting-guide.md` to reflect the new data source and output format.

## 3. Testing:

*   Run the `src/main.py` script with the `data/accomplishments.csv` file and verify that the output is generated correctly.
*   Compare the generated output with `output/sample_analysis.md` to ensure that the format is consistent.
*   Test the prompts in `docs/roo-code-prompting-guide.md` to ensure that they work as expected.

## 4. Finalize:

*   Write the updated plan to a markdown file.
*   Request the user to switch to another mode to implement the solution.

## Mermaid Diagram

```mermaid
graph TD
    A[Gather Information] --> B{Modify the Code};
    B --> C{Testing};
    C --> D[Finalize];
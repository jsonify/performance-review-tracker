# Detailed Plan for Phase 2: VS Code and Roo Code Setup

## 1. Configure VS Code for Python Development
- **Configure Python Interpreter**
  - Open VS Code settings.
  - Set the Python interpreter to the virtual environment created in Phase 1 (`venv`).
- **Set up Linting and Formatting**
  - Install `pylint` and `black` for linting and formatting.
  - Configure VS Code to use these tools:
    ```json
    {
      "python.linting.pylintEnabled": true,
      "python.formatting.provider": "black",
      "editor.formatOnSave": true
    }
    ```

## 2. Configure Roo Code Extension
- **Create Custom System Prompt for Analyst Mode**
  - Create a file `.roo/system-prompt-analyst` with the custom system prompt content provided in the design document.
- **Test Basic Roo Code Functionality**
  - Verify that Roo Code is installed and enabled in VS Code.
  - Test basic commands to ensure Roo Code is functioning correctly.

## 3. Create Custom Mode for Performance Review Analysis
- **Define Role Definition for Analyst Mode**
  - Add the role definition for Analyst mode to the custom mode configuration.
- **Configure Tool Permissions**
  - Ensure the necessary tool permissions are set for the Analyst mode.
- **Test Custom Mode Functionality**
  - Test the custom mode by running sample analysis tasks to ensure it works as expected.

## Mermaid Diagram for Phase 2

```mermaid
graph TD
    A[Configure VS Code for Python Development] --> B[Configure Python Interpreter]
    A --> C[Set up Linting and Formatting]
    D[Configure Roo Code Extension] --> E[Create Custom System Prompt for Analyst Mode]
    D --> F[Test Basic Roo Code Functionality]
    G[Create Custom Mode for Performance Review Analysis] --> H[Define Role Definition for Analyst Mode]
    G --> I[Configure Tool Permissions]
    G --> J[Test Custom Mode Functionality]

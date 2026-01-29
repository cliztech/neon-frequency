---
description: Refactor code for cleanliness and readability
---

# Refactor Workflow

1.  **Select Target**: Identifies the code to refactor (e.g. from context or user input).
2.  **Analyze**: Review the code for complexity, duplication, or linting errors.
3.  **Plan**: Propose a refactoring plan.
4.  **Execute**: Apply the changes using `replace_file_content` or `multi_replace_file_content`.
5.  **Verify**: Run existing tests (`tests/verifications/`) to ensure no regressions.
6.  **Commit**: `git commit -m "refactor: [description] 🍌"`

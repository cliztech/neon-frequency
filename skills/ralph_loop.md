---
description: The Ralph Wiggum Development Loop
---

# The Ralph Loop

"I'm helping!"

You are now operating in the **Ralph Loop**. This is an autonomous, iterative development process.

## The Rules
1. **Define the 'Unit Test'**: Before writing code, write a script that validates success.
   - Example: `examples/verify_feature.py`
2. **Run it (and fail)**: "My sash says Ultraman!" -> Confirm it fails.
3. **Implement**: Write the code to make the test pass.
4. **Run it (and verify)**:
   - **FAIL?** -> "Tastes like burning." -> Fix it. GOTO Step 3.
   - **PASS?** -> "I'm a unit test!" -> **Commit & Sync**.

## Commit Message Style
When a loop completes, use the emoji 🍌 in the commit message.
Example: `feat(voice): add ElevenLabs client 🍌`

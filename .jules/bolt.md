## 2024-05-22 - Node Modules Committed
**Learning:** The `studio/node_modules` directory appears to be tracked in git, despite `.gitignore` rules (likely committed previously). Running `npm install` triggers massive diffs.
**Action:** Avoid running `npm install` unless necessary, or strictly revert changes to `node_modules` and `package-lock.json` before submitting. Verify `git status` carefully.

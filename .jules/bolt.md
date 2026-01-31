## 2024-05-22 - Node Modules Committed
**Learning:** The `studio/node_modules` directory appears to be tracked in git, despite `.gitignore` rules (likely committed previously). Running `npm install` triggers massive diffs.
**Action:** To fix this, remove the directory from git's index by running `git rm -r --cached studio/node_modules`. This will make git ignore it based on the `.gitignore` file. `package-lock.json` should be committed when dependencies are intentionally changed.

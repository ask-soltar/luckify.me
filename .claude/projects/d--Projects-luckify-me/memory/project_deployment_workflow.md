---
name: Deployment workflow (clasp + GitHub)
description: How to push engine changes to Google Apps Script and GitHub
type: project
---

## Deployment Setup

**Google Apps Script (clasp):**
- `.clasp.json` location: `d:/Projects/luckify-me/engine/.clasp.json`
- Working directory: `d:/Projects/luckify-me/engine/`
- Command: `cd d:/Projects/luckify-me/engine && clasp push`
- Result: Pushes all 31 .gs files + appsscript.json to the Apps Script project

**GitHub:**
- Repository: https://github.com/ask-soltar/luckify-engine.git
- Main branch: `main`
- Working directory: `d:/Projects/luckify-me/`

## Typical Workflow

1. Make changes to engine files (e.g., `01_menu.gs`, `00_config.gs`) or docs (e.g., `CLAUDE.md`)
2. Push to Google Apps Script:
   ```bash
   cd d:/Projects/luckify-me/engine && clasp push
   ```
3. Commit to GitHub:
   ```bash
   cd d:/Projects/luckify-me && git add [files] && git commit -m "[message]" && git push
   ```
4. Or combined (from root):
   ```bash
   cd d:/Projects/luckify-me/engine && clasp push && cd .. && git add . && git commit -m "[msg]" && git push
   ```

## Always Do Both

- **clasp push** syncs to Apps Script (live in the Sheet)
- **git push** syncs to GitHub (version control)
- Both are part of the audit trail; don't skip either

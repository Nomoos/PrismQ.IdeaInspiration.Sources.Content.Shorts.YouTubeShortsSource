# Reorganize repository structure following best practices

## Description

Reorganize the repository to follow Python best practices with clear separation of concerns:
- Move documentation to `docs/` folder
- Move scripts to `scripts/` folder  
- Create file-based issue tracking in `issues/` with state folders
- Add copilot instructions for developers

## Implementation Notes

### Changes Made

1. Created folder structure:
   - `docs/` - All documentation (CONTRIBUTING, METRICS, WINDOWS_QUICKSTART)
   - `scripts/` - Setup and utility scripts
   - `issues/` - File-based issue tracking with state folders (new/, in-progress/, review/, blocked/, done/)
   - `.github/copilot-instructions.md` - Developer guide

2. Updated all documentation:
   - Fixed file paths in README.md
   - Updated cross-references in all docs
   - Created navigation READMEs in each folder

3. Implemented file-based issue tracking:
   - Created state-based folder structure
   - Added README in each state folder
   - Updated main issues/README.md with workflow guide

### Benefits

- ✅ Better organization following Python community standards
- ✅ Clear separation of documentation, scripts, and code
- ✅ File-based issue tracking for lightweight workflow
- ✅ Comprehensive developer guide for Copilot and contributors

## Links

- PR: #[PR number will be added]
- Commits: b4e08ad, d0bcc5c, [new commits]

## State History

- Started: issues/new/
- In Progress: issues/in-progress/
- Review: issues/review/
- Done: issues/done/ (current)

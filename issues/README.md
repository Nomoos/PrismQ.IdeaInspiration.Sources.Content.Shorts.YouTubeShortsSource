# Issues - File-Based Issue Tracking

This folder contains a lightweight, file-based issue tracking system organized by state.

## Structure

Issues are tracked as Markdown files organized into state folders:

```
issues/
├── new/          # Newly reported issues
├── in-progress/  # Issues currently being worked on
├── review/       # Issues awaiting review
├── blocked/      # Issues that cannot proceed
├── done/         # Completed issues
├── KNOWN_ISSUES.md
└── ROADMAP.md
```

## How to Create an Issue

1. Create a new `.md` file in `issues/new/`
2. Use a short, descriptive filename (e.g., `fix-login-timeout.md`, `add-tiktok-plugin.md`)
3. Follow this template:

```markdown
# Title of the Issue

## Description
Detailed description of the issue or feature request.

## Steps to Reproduce (for bugs)
1. Step one
2. Step two
3. Expected vs actual behavior

## Notes
- Any additional context
- Related issues or discussions

## Links
- PR: #123
- Commit: abc1234
```

## Moving Issues Between States

As work progresses, move issue files between folders:

```bash
# Start working on an issue
git mv issues/new/feature-name.md issues/in-progress/feature-name.md

# Move to review
git mv issues/in-progress/feature-name.md issues/review/feature-name.md

# Mark as blocked
git mv issues/in-progress/feature-name.md issues/blocked/feature-name.md

# Complete the issue
git mv issues/review/feature-name.md issues/done/feature-name.md
```

## Issue States

### new/
Newly reported issues that haven't been triaged or started yet.

### in-progress/
Issues currently being worked on by a contributor.

### review/
Issues with completed work awaiting review or testing.

### blocked/
Issues that cannot proceed due to dependencies, decisions needed, or external factors.

### done/
Completed and closed issues. Keep for reference.

## GitHub Issues Integration

This file-based system complements GitHub Issues:

- Use **GitHub Issues** for community discussions and tracking
- Use **file-based issues** for internal development workflow
- Cross-reference: Link GitHub issue numbers in file-based issues and vice versa

## Finding Issues

### By State
Browse folders directly:
- `issues/new/` - Issues ready to be picked up
- `issues/in-progress/` - Active work
- `issues/blocked/` - Issues needing help

### By Topic
Use `grep` to search across all issues:

```bash
# Find all issues mentioning "API"
grep -r "API" issues/

# Find all bug-related issues
grep -r "bug" issues/new/ issues/in-progress/
```

## Contributing

If you want to work on an issue:

1. Check `issues/new/` for available issues
2. Move the issue to `issues/in-progress/` when you start
3. Update the issue file with your progress and notes
4. When ready for review, move to `issues/review/`
5. After approval, move to `issues/done/`

See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for full guidelines.

## Templates

Use our [GitHub issue templates](../.github/ISSUE_TEMPLATE/) for:
- Bug reports
- Feature requests
- General discussions

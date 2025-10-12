# Issues - File-Based Issue Tracking

This folder contains a lightweight, file-based issue tracking system organized by state.

## Structure

Issues are tracked as Markdown files organized into state folders:

```
issues/
├── new/          # Newly reported issues
├── wip/          # Issues being worked on (Work In Progress)
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

## Type
Bug | Feature | Enhancement

## Priority
High | Medium | Low

## Target Platform
Windows | NVIDIA RTX 5090 | AMD Ryzen | 64GB RAM

## Steps to Reproduce (for bugs)
1. Step one
2. Step two
3. Expected vs actual behavior

## Notes
- Any additional context
- Related issues or discussions
- Hardware/platform considerations

## Links
- PR: #123
- Commit: abc1234
```

## Moving Issues Between States

As work progresses, move issue files between folders:

```bash
# Start working on an issue
git mv issues/new/feature-name.md issues/wip/feature-name.md

# Complete the issue
git mv issues/wip/feature-name.md issues/done/feature-name.md

# Return to new if pausing work
git mv issues/wip/feature-name.md issues/new/feature-name.md
```

## Issue States

### new/
Newly reported issues that haven't been started yet.

### wip/
Issues currently being worked on (Work In Progress).

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
- `issues/wip/` - Active work
- `issues/done/` - Completed

### By Topic
Use `grep` to search across all issues:

```bash
# Find all issues mentioning "API"
grep -r "API" issues/

# Find all bug-related issues
grep -r "bug" issues/new/ issues/wip/
```

## Contributing

If you want to work on an issue:

1. Check `issues/new/` for available issues
2. Move the issue to `issues/wip/` when you start
3. Update the issue file with your progress and notes
4. When complete, move to `issues/done/`

See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for full guidelines.

## Templates

Use our [GitHub issue templates](../.github/ISSUE_TEMPLATE/) for:
- Bug reports
- Feature requests
- General discussions

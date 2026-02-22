# GitHub Automation

This document describes the GitHub automation workflows for this project.

## Daily Sync

Run the daily sync script to keep repositories synchronized:

```bash
./scripts/daily-github-sync.sh
```

## Automation Tools

- GitHub CLI (gh)
- Git hooks for pre-commit checks
- Dependabot for dependency updates

## Repository Management

- Use GitHub Issues for tracking
- Use Pull Requests for code review
- Enable branch protection rules

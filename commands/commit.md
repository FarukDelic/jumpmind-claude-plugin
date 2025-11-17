---
description: Generate conventional commit message from staged changes
argument-hint: [type] [scope] [--breaking]
allowed-tools: Bash(git:*)
model: haiku
---

## Context

**Current git status:**
!`git status`

**Staged changes:**
!`git diff --cached --stat`

**Diff details:**
!`git diff --cached`

**Recent commits for style reference:**
!`git log -5 --oneline`

## Instructions

Analyze the staged changes and create a commit message following this structure:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

Use these standard types based on the changes:

- **feat**: New feature for the user (correlates to MINOR in semantic versioning)
- **fix**: Bug fix for the user (correlates to PATCH)
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (white-space, formatting, missing semi-colons)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes to build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Requirements

1. **Type**: MUST be one of the types above
2. **Scope**: OPTIONAL, indicates what part of codebase is affected (e.g., `parser`, `api`, `ui`)
3. **Description**: REQUIRED, short summary in present tense, lowercase, no period at end
4. **Body**: OPTIONAL, provides additional context. Use when:
   - Changes are non-trivial
   - Multiple files or concerns are affected
   - Implementation details would help reviewers
5. **Footer**: OPTIONAL, used for:
   - Breaking changes: `BREAKING CHANGE: <description>`
   - Issue references: `Fixes #123`, `Closes #456`
   - Co-authors: `Co-authored-by: Name <email>`

### Breaking Changes

If changes include breaking changes, indicate via:

- Add `!` after type/scope: `feat(api)!: remove deprecated endpoints`
- OR add footer: `BREAKING CHANGE: API v1 endpoints removed`

### Best Practices

- Keep description under 50 characters when possible
- Use imperative mood: "add feature" not "added feature" or "adds feature"
- Don't capitalize first letter of description
- No period at end of description
- Separate body from description with blank line
- Wrap body at 72 characters
- Explain what and why, not how
- Reference issues and PRs in footer

### Output Format

Provide the commit message in a code block that can be copied directly. Include explanation of your choices below the commit message.

**Arguments**:

- If $ARGUMENTS provided, use them as guidance (e.g., "/commit feat auth" suggests feat type with auth scope)
- If "--breaking" flag present, ensure breaking change is indicated
- Otherwise, analyze changes automatically

Generate the commit message now.

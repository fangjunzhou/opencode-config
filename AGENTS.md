# Agent Guidelines for opencode-config

This repository contains OpenCode prompts and configurations for agentic coding workflows.

## Repository Structure

```
opencode-config/
├── opencode.json          # OpenCode configuration (schema reference)
├── README.md              # Project documentation
├── AGENTS.md              # This file - agent instructions
└── .opencode/
    ├── package.json       # Dependencies (@opencode-ai/plugin)
    └── agents/
        ├── autobuild.md   # Primary end-to-end implementation agent
        └── autoplan.md    # Research-heavy planning agent
```

## Build/Lint/Test Commands

This is a **configuration repository** with no traditional build, lint, or test pipelines.

### JSON Validation

```bash
# Validate JSON syntax (parse-only check)
cat opencode.json | jq empty

# Pretty-print to verify structure
cat opencode.json | jq .

# Validate all JSON files in the repo
find . -name "*.json" -not -path "./.opencode/node_modules/*" -exec jq empty {} \;
```

### YAML/Frontmatter Validation

Agent files use YAML frontmatter - verify manually by reading the file and checking for:
- Valid YAML syntax (no malformed key-value pairs)
- All required fields present
- Correct indentation (2 spaces)

### Package Dependencies

```bash
# Install/update dependencies
cd .opencode && bun install
```

### Pre-commit Validation Checklist

Before committing changes to agent definitions:
1. Verify JSON files parse correctly (`jq empty <file>`)
2. Confirm YAML frontmatter has all required fields
3. Check file naming conventions match conventions below
4. Review permission model follows least-privilege principle

## Code Style Guidelines

### Configuration Files (JSON)

- Use 2-space indentation
- Always include `$schema` field when available
- Use trailing commas (consistent with modern JSON)
- Keep configuration values organized by category
- No inline comments in JSON

**Example:**
```json
{
  "$schema": "https://opencode.ai/config.json",
  "setting1": "value",
  "setting2": {
    "nested": true
  }
}
```

### Agent Definition Files (Markdown)

Agent files use **YAML frontmatter** followed by markdown content.

**Required Frontmatter Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Brief description of the agent's role (1-2 sentences) |
| `mode` | string | Agent mode: `primary`, `analysis`, `review`, etc. |
| `temperature` | number | Sampling temperature (0.0-1.0) |
| `permission` | object | Explicit permission grants/denials for each tool |

**Permission Structure:**
```yaml
permission:
  read: allow|deny
  list: allow|deny
  glob: allow|deny
  grep: allow|deny
  edit:
    "*": deny
    ".opencode/plans/*": allow  # Granular path-based rules
  bash: allow|deny
  webfetch: allow|deny
  websearch: allow|deny
  todoread: allow|deny
  todowrite: allow|deny
  task: allow|deny
  question: allow|deny
```

**Markdown Content:**
- Use ATX-style headings (`#`, `##`, `###`)
- Keep lines under 120 characters
- Use bullet lists for requirements
- Include code blocks with language identifiers
- No emoji in documentation (unless explicitly requested)

### File Naming Conventions

| File Type | Convention | Example |
|-----------|------------|---------|
| Agent files | `snake_case.md` | `autobuild.md`, `code_review.md` |
| Configuration files | `camelCase.json` or `kebab-case.json` | `opencode.json` |
| Documentation | `Title Case.md` or `UPPERCASE.md` | `README.md` |
| Plan documents | `kebab-case.md` in `.opencode/plans/` | `feature-x-implementation.md` |

**Agent Names:** Use descriptive, action-oriented names matching the agent's primary responsibility.
**Configuration Keys:** Use camelCase, be concise (2-3 words max), group related settings together.

### Error Handling

**Agent Definitions:**
- Missing required frontmatter fields will cause agent loading failures
- Invalid YAML syntax breaks the entire file
- Ensure all permission values are either `allow` or `deny`

**JSON Files:**
- Invalid JSON syntax prevents parsing entirely
- Missing `$schema` reduces IDE validation capability
- Use `jq` to validate before committing

**Best Practices:** Validate after every edit, keep changes minimal, document non-obvious choices.

### Documentation Standards

**Agent Instructions:** Be specific about what the agent should/should not do, provide concrete examples, include explicit validation steps, state when to ask for clarification, avoid ambiguous instructions.

## Permission Model

| Value | Meaning |
|-------|---------|
| `allow` | Agent can use this tool |
| `deny` | Agent cannot use this tool |

**Guidelines:** Default deny is recommended for sensitive tools (`bash`, `websearch`). Grant least privilege necessary. Use granular path-based rules for file editing when possible.

## General Operating Rules

1. **Minimal Changes**: Prefer the smallest correct change that satisfies the request
2. **Validate First**: Verify JSON syntax after editing configuration files
3. **Schema Compliance**: Ensure configurations match their declared schemas
4. **No Unnecessary Comments**: Configuration files should be clean
5. **Consistent Formatting**: Match existing file formatting patterns
6. **Test Changes in Isolation**: Verify agent behavior before committing
7. **Document Risks**: Explicitly state what could not be validated

### Before Finishing

Verify and report: files changed, commands run, local documentation consulted, network sources consulted, whether validation passed, any remaining risk or follow-up.

## Notes

- This is a personal configuration repository
- Changes to agent definitions directly affect how OpenCode operates
- Always review the impact of permission changes
- The `.opencode/` directory contains the actual agent definitions used at runtime
- No Cursor or Copilot rules exist in this repository

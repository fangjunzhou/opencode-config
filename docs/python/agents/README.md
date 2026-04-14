# Python-Specific Agents

This directory contains Python-specific agent definitions that override or extend the shared agents.

## When to Add Python Agents

Create a Python-specific agent if:

- The agent behavior differs from the shared version
- Python projects need special handling
- Python-specific tools/libraries require customization

## Format

Same as shared agents:

```markdown
---
description: Python-specific agent description
mode: subagent | primary
temperature: 0.0-1.0
permission:
  # ... permissions
---

Agent instructions...
```

## Examples

If `autobuild.md` needs Python-specific behavior, create:

- `python/agents/autobuild.md` (will override `shared-config/agents/autobuild.md`)

Or add new Python-only agents:

- `python/agents/python-linter.md`
- `python/agents/pytest-runner.md`

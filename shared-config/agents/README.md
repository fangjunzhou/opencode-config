# Agent Definitions

This directory contains shared OpenCode agent definitions that are common to all language variants.

## Structure

Each agent is defined as a Markdown file with YAML frontmatter:

- `autobuild.md` - End-to-end implementation agent
- `autoplan.md` - Research-heavy planning agent

## Format

Each agent file follows the structure:

```markdown
---
description: Brief description of the agent
mode: subagent | primary | analysis | review
temperature: 0.0-1.0
permission:
  read: allow|deny
  edit: allow|deny
  bash: allow|deny
  # ... other tools
---

Agent instructions and guidelines...
```

## Language-Specific Agents

Language variants can add or override agents:

- `../python/agents/` - Python-specific agents
- `../cpp/agents/` - C++-specific agents
- etc.

These are merged on top of shared agents when generating `.opencode/`.

## For Developers

When adding a new agent definition:

1. Create file: `{agent-name}.md`
2. Start with YAML frontmatter (required fields: description, mode, temperature, permission)
3. Add agent instructions after the `---` separator
4. Test locally: `./scripts/setup-opencode.sh base`
5. Verify in `.opencode/agents/`

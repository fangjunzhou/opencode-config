# Python-Specific Commands

This directory contains command definitions specific to Python projects.

## Available Commands

- `add-lib.md` - Add library dependencies to Python projects

## Format

Commands are Markdown files with:

- Command name and purpose
- Usage examples
- Required arguments
- Optional flags
- Success/error criteria

## Adding New Commands

When adding a new Python command:

1. Create file: `{command-name}.md`
2. Document thoroughly with examples
3. Test: `./scripts/setup-opencode.sh python`
4. Verify in `.opencode/commands/`
5. Commit

## For Agents

Agents can directly fetch Python commands:

```
https://fangjun.github.io/opencode-config/python/commands/
```

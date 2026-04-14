# Common Commands

This directory contains command definitions that are shared across all language variants.

## Structure

Commands are organized by type:

- `.md` files - Command definitions
- Each command is self-contained and documented

## Format

Each command file should include:

- Command name and purpose
- Usage examples
- Required arguments
- Optional flags
- Success/error criteria

## Language-Specific Commands

Language variants can add additional commands:

- `../python/commands/` - Python-specific commands
- `../cpp/commands/` - C++-specific commands
- etc.

These are merged on top of shared commands when generating `.opencode/`.

## For Developers

When adding a new command:

1. Create file: `{command-name}.md`
2. Document the command thoroughly
3. Include usage examples
4. Test locally: `./scripts/setup-opencode.sh base`
5. Verify in `.opencode/commands/`

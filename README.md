# OpenCode Config

Multi-variant configuration system for OpenCode agents.

## Quick Start

Download and extract your configuration:

Base (no language specifics):
```bash
curl -fsSL https://fangjun.github.io/opencode-config/distributions/opencode-base.tar.gz | tar xz
```

Python-specific:
```bash
curl -fsSL https://fangjun.github.io/opencode-config/distributions/opencode-python.tar.gz | tar xz
```

## Browse

- All files and configurations: https://fangjun.github.io/opencode-config/
- Download page with all variants: https://fangjun.github.io/opencode-config/distributions/

## Repository Layout

- `shared-config/` - Base configurations (all variants)
- `python/` - Python-specific overrides
- `scripts/` - Build and setup automation
- `.opencode/` - Generated merged configurations (do not edit)
- `DEVELOPER_GUIDE.md` - Developer guide and contribution instructions

## For Developers

See DEVELOPER_GUIDE.md for:
- Project architecture
- How to add/edit configurations
- Build and testing commands
- Adding new variants
- Code style guidelines

## For Agents

Configurations are publicly accessible via HTTP:

```bash
# Browse root
curl https://fangjun.github.io/opencode-config/

# Access agent definition
curl https://fangjun.github.io/opencode-config/shared-config/agents/autobuild.md

# Access variant-specific command
curl https://fangjun.github.io/opencode-config/python/commands/add-lib.md
```

Agents can download and consume configurations directly without authentication.

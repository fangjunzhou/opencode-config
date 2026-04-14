# OpenCode Config

Multi-variant configuration system for OpenCode agents.

## Quick Start

Download and extract your configuration:

Base (no language specifics):
```bash
curl -fsSL https://fangjunzhou.github.io/opencode-config/distributions/opencode-base.tar.gz | tar xz
```

Python-specific:
```bash
curl -fsSL https://fangjunzhou.github.io/opencode-config/distributions/opencode-python.tar.gz | tar xz
```

## Browse Online

- **File Browser**: https://fangjunzhou.github.io/opencode-config/ - Browse all configurations and source files
- **Downloads**: https://fangjunzhou.github.io/opencode-config/distributions/ - Download pre-built packages
- **GitHub Repository**: https://github.com/fangjunzhou/opencode-config

## Repository Layout

- `shared-config/` - Base configurations (all variants)
- `python/` - Python-specific overrides and commands
- `scripts/` - Build and deployment automation
- `.opencode/` - Generated merged configurations (do not edit)
- `distributions/` - Pre-built packages for download
- `DEVELOPER_GUIDE.md` - Comprehensive development guide

## For Developers

See [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) for:
- Complete architecture overview
- How to add/edit configurations
- Build and testing commands
- Adding new variants
- Code style and contribution guidelines

## For Agents

Configurations are publicly accessible via HTTP:

```bash
# Browse root file listing
curl https://fangjunzhou.github.io/opencode-config/

# Access base agent definition
curl https://fangjunzhou.github.io/opencode-config/shared-config/agents/autobuild.md

# Access variant-specific command
curl https://fangjunzhou.github.io/opencode-config/python/commands/add-lib.md

# Download and extract base variant
curl -fsSL https://fangjunzhou.github.io/opencode-config/distributions/opencode-base.tar.gz | tar xz
```

Agents can download and consume configurations directly without authentication required.

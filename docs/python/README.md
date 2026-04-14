# Python OpenCode Variant

This directory contains Python-specific configurations and overrides for the OpenCode system.

## Structure

```
python/
├── commands/           # Python-specific commands
├── agents/             # Python-specific agent overrides (optional)
├── opencode.json       # Python-specific config overrides (optional)
└── README.md           # This file
```

## How It Works

When you run:

```bash
./scripts/setup-opencode.sh python
```

The system:

1. Copies all files from `shared-config/` to `.opencode/`
2. Overlays all files from `python/` on top (overwrites shared)
3. Result: `.opencode/` contains shared configs + Python-specific customizations

## Python-Specific Commands

Commands in `python/commands/` are specific to Python projects:

- `add-lib.md` - Add Python library/dependencies

These are merged with common commands from `shared-config/commands/`.

## Python-Specific Agents

If needed, you can override or create Python-specific agents in `python/agents/`:

- Same format as `shared-config/agents/`
- Will override shared agents with the same filename
- New agents are added to the final configuration

## Python-Specific Config

Optionally create `python/opencode.json` to override `shared-config/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "python": {
    "version": "3.11+",
    "package_manager": "pip"
  }
}
```

## Installation

To use the Python variant:

```bash
# One-liner download and extraction
curl -fsSL https://fangjunzhou.github.io/opencode-config/opencode-python.tar.gz | tar xz

# Or setup locally
./scripts/setup-opencode.sh python
```

## For Developers

When adding Python-specific configs:

1. Create file in appropriate subdirectory
2. Follow the same format as shared configs
3. Run: `./scripts/setup-opencode.sh python`
4. Verify in `.opencode/`
5. Test functionality
6. Commit both the python/ file and updated `.opencode/`

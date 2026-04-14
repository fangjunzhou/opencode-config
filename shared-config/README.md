# Shared OpenCode Configuration

This directory contains the **source-of-truth** for all OpenCode configurations that are shared across all language variants.

## Structure

```
shared-config/
├── agents/              # Common agent definitions
├── commands/            # Common commands
├── scripts/             # Utility scripts
├── templates/           # Template configurations for variants
├── opencode.json        # Base OpenCode configuration
└── README.md            # This file
```

## How It Works

The `.opencode/` directory in the project root is **generated** by combining:

1. All contents of this `shared-config/` directory (base)
2. Language-specific overrides (from `python/`, `cpp/`, `go/`, etc.)

### Merge Strategy

When `./scripts/setup-opencode.sh python` runs:

```
shared-config/*  →  copy to .opencode/
python/*         →  rsync to .opencode/ (overwrites shared)
```

This means:
- Common configs are always available
- Language variants can override specific files
- `.opencode/` is always generated (do not edit directly)

## Creating .opencode/

To regenerate `.opencode/` with a specific variant:

```bash
./scripts/setup-opencode.sh base        # Base configs only
./scripts/setup-opencode.sh python      # Base + Python overrides
./scripts/setup-opencode.sh cpp         # Base + C++ overrides
```

## Adding New Configurations

To add a new shared configuration:

1. Create the file in `shared-config/{agents|commands|scripts}/`
2. Follow naming conventions (kebab-case for files)
3. Run `./scripts/setup-opencode.sh base` to regenerate `.opencode/`
4. Commit both the shared config and updated `.opencode/`

## Language Variants

Language-specific variants are stored in their own directories:

- `python/` - Python-specific agents and commands
- `cpp/` - C++-specific configurations
- `go/` - Go-specific configurations
- etc.

Each variant can override or extend shared configurations.

## For Agents

All configurations in this directory (and generated `.opencode/`) are publicly accessible at:

```
https://fangjun.github.io/opencode-config/shared-config/
https://fangjun.github.io/opencode-config/.opencode/
```

Agents can directly fetch and parse configurations via HTTP.

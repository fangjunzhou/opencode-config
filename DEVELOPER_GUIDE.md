# Agent Guidelines for opencode-config

This repository contains OpenCode prompts and configurations for agentic coding workflows, organized using a multi-variant distribution system.

## Project Overview

The opencode-config repository manages agent definitions and configurations across multiple language variants. Each variant can have base agents plus language-specific overrides, commands, and settings.

## Repository Structure

```
opencode-config/
├── shared-config/              Source of truth for all variants
│   ├── agents/                 Base agent definitions
│   │   ├── autobuild.md        End-to-end implementation
│   │   └── autoplan.md         Research-heavy planning
│   ├── commands/               Common commands
│   └── opencode.json           Base configuration
│
├── python/                     Python-specific variant
│   ├── agents/                 Python-specific agent overrides
│   ├── commands/               Python-specific commands
│   │   └── add-lib.md          Add packages/dependencies
│   └── README.md               Variant documentation
│
├── scripts/                    Build and setup automation
│   ├── setup-opencode.sh       Merge shared-config + variant
│   ├── build-distributions.sh  Create downloadable packages
│   └── generate_distribution_index.py  Build downloads page
│
├── distributions/              Generated packages (GitHub Pages)
│   ├── opencode-base.tar.gz
│   ├── opencode-python.tar.gz
│   ├── SHA256SUMS
│   └── index.html              Downloads page
│
├── .opencode/                  Generated (in .gitignore)
│   ├── .gitignore              Prevents accidental commits
│   ├── agents/                 Merged from shared + variant
│   ├── commands/
│   └── opencode.json
│
├── .github/workflows/          CI/CD automation
│   └── deploy-pages.yml        Unified build and deployment workflow
│
├── README.md                   User landing page
├── DEVELOPER_GUIDE.md          This file
└── opencode.json               Root configuration
```

## How the System Works

### Merge Process

When you run `./scripts/setup-opencode.sh python`:

1. Copy all files from `shared-config/` to `.opencode/`
2. Overlay all files from `python/` on top (preserves shared, adds python-specific)
3. Result: `.opencode/` contains merged configuration ready for use

### Build Process

When you run `./scripts/build-distributions.sh all`:

1. For each variant: run setup script to create merged configuration
2. Create tarball from merged configuration
3. Generate SHA256 checksums
4. Create index.html listing all variants with download links
5. Result: `distributions/` contains ready-to-distribute packages

### Deployment Process

GitHub Actions workflow (`deploy-pages.yml`) handles deployment automatically:

**Job 1: Build and Deploy (parallel for each variant)**
- Checkout repository
- Set up Python environment
- Build base and python variants in parallel
- Upload distribution artifacts (tar.gz, checksums)

**Job 2: Generate Index and Deploy**
- Waits for all builds to complete
- Copies configuration files to deployment directory
- Downloads and merges all distribution artifacts
- Runs `generate_distribution_index.py` to create /distributions/index.html
- Runs `generate_directory_listing.py` to create root index.html with file browser
- Uploads deployment to GitHub Pages
- Deploys to production

**Result**: All configurations accessible via HTTPS with no authentication required.
- Root with file browser: https://fangjunzhou.github.io/opencode-config/
- Downloads page: https://fangjunzhou.github.io/opencode-config/distributions/

## Build/Lint/Test Commands

This is a configuration repository with no traditional build pipeline.

### JSON Validation

Validate JSON syntax before committing:

```bash
# Validate single file
jq empty opencode.json

# Pretty-print configuration
jq . opencode.json

# Validate all JSON files
find . -name "*.json" -not -path "./.opencode/node_modules/*" -exec jq empty {} \;
```

### YAML Frontmatter Validation

Agent files use YAML frontmatter - verify manually by reading and checking:
- Valid YAML syntax (no malformed key-value pairs)
- All required fields present
- Correct indentation (2 spaces)

Required fields: `description`, `mode`, `temperature`, `permission`

### Setup and Build Scripts

```bash
# Merge shared-config + python variant into .opencode/
./scripts/setup-opencode.sh python

# Build distributions for all variants
./scripts/build-distributions.sh all

# Build single variant
./scripts/build-distributions.sh base

# Generate distribution index page
python3 scripts/generate_distribution_index.py distributions/

# Generate root file browser index
python3 scripts/generate_directory_listing.py .

# Install dependencies
cd .opencode && bun install
```

### Pre-commit Validation Checklist

Before committing changes:
1. Verify JSON files parse: `jq empty <file>`
2. Confirm YAML frontmatter has all required fields
3. Check file naming conventions are correct
4. Review permissions follow least-privilege principle
5. Run setup script: `./scripts/setup-opencode.sh base`
6. Verify .opencode/ contains merged results

## Development Workflow

### Editing Shared Configurations

For changes affecting all variants:

```bash
# Edit base agent
vim shared-config/agents/autobuild.md

# Edit base configuration
vim shared-config/opencode.json

# Regenerate .opencode/
./scripts/setup-opencode.sh base
```

### Editing Variant-Specific Configurations

For Python-specific changes:

```bash
# Edit Python agent override
vim python/agents/autobuild.md

# Edit Python command
vim python/commands/add-lib.md

# Regenerate .opencode/ with variant
./scripts/setup-opencode.sh python
```

### Testing Locally

```bash
# Build all variants
./scripts/build-distributions.sh all

# Test tarball extraction
cd /tmp
tar xz -f /path/to/opencode-python.tar.gz
ls -la .opencode/  # Verify merged contents
```

### Committing Changes

```bash
# Stage changes (including regenerated .opencode/)
git add shared-config/ python/ .opencode/

# Commit with meaningful message
git commit -m "Update autobuild agent permissions"

# Push to main
git push origin main
```

GitHub Actions will automatically deploy updated distributions.

## Code Style Guidelines

### JSON Configuration Files

- Use 2-space indentation
- Always include `$schema` field when available
- Use trailing commas (modern JSON style)
- Organize settings by category
- No inline comments

Example:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "agents": {
    "autobuild": true
  },
  "settings": {
    "debug": false
  }
}
```

### Agent Definition Files (Markdown)

Agent files use YAML frontmatter followed by markdown content.

Required frontmatter fields:
- `description` - Brief role description (1-2 sentences)
- `mode` - Agent mode: `primary`, `analysis`, `review`, etc.
- `temperature` - Sampling temperature (0.0-1.0)
- `permission` - Explicit tool permission grants/denials

Permission structure:
```yaml
permission:
  read: allow|deny
  glob: allow|deny
  grep: allow|deny
  edit:
    "*": deny
    ".opencode/plans/*": allow
  bash: allow|deny
  webfetch: allow|deny
  todowrite: allow|deny
  task: allow|deny
```

Markdown content guidelines:
- Use ATX-style headings (#, ##, ###)
- Keep lines under 120 characters
- Use bullet lists for requirements
- Include code blocks with language identifiers
- No fancy characters (no arrows, emojis)

### File Naming Conventions

| File Type | Convention | Example |
|-----------|------------|---------|
| Agent files | snake_case.md | autobuild.md |
| Configuration files | opencode.json or config.json | opencode.json |
| Documentation | README.md or DEVELOPER_GUIDE.md | README.md |
| Plan documents | kebab-case.md in .opencode/plans/ | feature-plan.md |

## Adding New Variants

To add a C++ variant:

1. Create directory structure:
```bash
mkdir -p cpp/{agents,commands}
```

2. Add C++-specific configurations:
```bash
# Copy from Python variant as template
cp python/README.md cpp/README.md
# Create cpp/commands/add-lib.md, etc.
```

3. Test locally:
```bash
./scripts/setup-opencode.sh cpp
./scripts/build-distributions.sh cpp
tar xz -f distributions/opencode-cpp.tar.gz -C /tmp
```

4. Update CI/CD workflow:
```bash
# Edit .github/workflows/deploy-pages.yml
# Add 'cpp' to the matrix variants list in the build-and-deploy job:
# strategy:
#   matrix:
#     variant: [base, python, cpp]
```

5. Commit and push:
```bash
git add cpp/ .github/workflows/distribute-variants.yml
git commit -m "Add C++ variant"
git push origin main
```

GitHub Actions will automatically generate `opencode-cpp.tar.gz` and deploy it.

## Permission Model

Permission values:
- `allow` - Agent can use this tool
- `deny` - Agent cannot use this tool

Guidelines:
- Default deny is recommended for sensitive tools (bash, websearch)
- Grant only least privilege necessary
- Use granular path-based rules for file editing when possible
- Document reasons for sensitive permissions

## Error Handling

### Common JSON Errors

- Invalid JSON syntax prevents parsing entirely
- Missing `$schema` reduces IDE validation capability
- Use `jq` to validate before committing

### Agent Definition Errors

- Missing required frontmatter fields cause loading failures
- Invalid YAML syntax breaks the entire file
- Ensure all permission values are either `allow` or `deny`
- Check indentation (must be 2 spaces)

### Best Practices

- Validate after every edit
- Keep changes minimal and focused
- Test in isolation before committing
- Document non-obvious choices in commit messages

## General Operating Rules

1. **Minimal Changes** - Prefer smallest correct change that satisfies request
2. **Validate First** - Verify JSON syntax after editing configurations
3. **Schema Compliance** - Ensure configurations match declared schemas
4. **No Unnecessary Comments** - Configuration files should be clean
5. **Consistent Formatting** - Match existing file formatting patterns
6. **Test in Isolation** - Verify agent behavior before committing
7. **Document Risks** - Explicitly state what could not be validated
8. **Do Not Edit .opencode/** - It's generated; edit source files instead
9. **Always Run Setup Script** - After making changes, run ./scripts/setup-opencode.sh
10. **Commit Both Source and Generated** - Include .opencode/ in commits

## Before Finishing

When making changes to this repository, verify and report:
- Files changed and what was modified
- Commands run and their output
- Whether validation passed
- Any remaining risks or follow-up tasks

## Notes

- This is a personal configuration repository
- Changes to agent definitions directly affect how OpenCode operates
- Always review the impact of permission changes
- The `.opencode/` directory contains actual agent definitions used at runtime
- All configurations are publicly accessible via HTTP
- Generated files should be committed to preserve exact merge state

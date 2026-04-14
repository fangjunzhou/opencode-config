# OpenCode Config

My OpenCode prompts and configurations for agentic coding workflows.

## Overview

This repository contains OpenCode agent definitions and configuration files that define how AI coding agents operate in my projects.

## Repository Structure

```
opencode-config/
├── opencode.json          # OpenCode configuration
├── README.md              # This file
├── AGENTS.md              # Agent guidelines for this repository
└── .opencode/
    ├── package.json       # Dependencies
    └── agents/
        ├── autobuild.md   # Primary end-to-end implementation agent
        └── autoplan.md    # Research-heavy planning agent
```

## Agent Definitions

The `.opencode/agents/` directory contains YAML-frontmatter agent definitions that specify:
- Agent role and behavior
- Operating mode and temperature
- Permission model for available tools

## Configuration Files

- `opencode.json` - Main OpenCode configuration with schema reference

## Usage

Refer to [AGENTS.md](AGENTS.md) for detailed guidelines when making changes to this repository.

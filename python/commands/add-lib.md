---
description: Add a Python library with uv, optionally to a specific workspace package
agent: autobuild
---

Add Python library `$1` to this repository using uv. The optional second argument `$2` is the target package in the uv workspace.

Task-specific instructions:
0. Always pay attention to possible typos, aliases, or naming ambiguities for both the library and the optional package. Resolve them before making changes.
1. Assume uv should already be installed in the current environment. First verify that uv is available.
2. If uv is not available, end the task immediately. Do not install the library with pip, venv, conda, poetry, pdm, or any other tool. Report that uv is missing from the environment and stop.
3. Read the root `pyproject.toml` if it exists to determine whether this repository uses a uv workspace.
4. If a uv workspace is present and `$2` was provided, verify that `$2` is a real package inside the workspace before adding the dependency.
5. Search the official documentation for `$1` to confirm the correct package name and whether useful extras exist.
6. If the user’s requested name appears to be an alias, shorthand, typo, or common mistaken package name, resolve it using the official documentation before running uv.
7. Choose the correct install command:
   - if there is no uv workspace, run `uv add <lib-or-lib[extra]>`
   - if there is a uv workspace and `$2` was provided, run `uv add --package $2 <lib-or-lib[extra]>`
   - if there is a uv workspace and `$2` was not provided, determine the correct target package from the repository structure and documentation; if that cannot be determined confidently, stop and explain what is ambiguous
8. After adding the library, check the corresponding `pyproject.toml` to confirm the dependency was added successfully.
9. Report:
   - the package actually added,
   - whether extras were used,
   - the target package if applicable,
   - the exact uv command run,
   - which `pyproject.toml` file was updated,
   - whether the dependency was added successfully.

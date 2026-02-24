# CXP-Canary

Context poisoning tester for AI coding assistants. Part of the Volery offensive security program (`richardspicer/volery`). Sister program: CounterAgent (`richardspicer/counteragent`).

## Project Layout

```
src/cxp_canary/
├── __init__.py
├── cli.py              # Click CLI
├── objectives/         # Attack objective definitions + validators
├── formats/            # Assistant format definitions
├── techniques/         # Payload templates (objective × format)
├── builder.py          # Repo builder — packages test repos
├── validator.py        # Output validation engine
├── evidence.py         # SQLite evidence store
├── reporter.py         # Comparison matrices + PoC packages
├── models.py           # Core data models
tests/                  # pytest suite
docs/
├── Architecture.md     # Components, data models, extension points
└── Roadmap.md          # Phased development plan
```

## Code Standards

- **Docstrings:** Google-style on all public functions and classes (Args, Returns, Raises)
- **Type hints:** Required on all function signatures
- **Line length:** 100 chars (ruff)
- **Imports:** Sorted by ruff (isort rules)

## Testing

- Framework: pytest
- Tests in `tests/`
- Run: `uv run pytest -q`

## Git Workflow

**Never commit directly to main.** Pre-commit hook blocks it.

```
git checkout main && git pull
git checkout -b feature/description    # or fix/, docs/, refactor/
# ... work ...
git add .
git commit -F .commitmsg               # see shell quoting note below
git push -u origin feature/description
# Create PR on GitHub, merge
```

### Shell Quoting (CRITICAL)

CMD shell corrupts `git commit -m "message with spaces"`. Always use:
```
echo "feat: description here" > .commitmsg
git commit -F .commitmsg
rm .commitmsg
```

## Pre-commit Hooks

Hooks run automatically on `git commit`:
- trailing-whitespace, end-of-file-fixer, check-yaml, check-toml
- check-added-large-files, check-merge-conflict
- **no-commit-to-branch** (blocks direct commits to main)
- **ruff** (lint + auto-fix) + **ruff-format**
- **gitleaks** (secrets detection)
- **mypy** (type checking)

## Dependencies

Managed via `uv` with `pyproject.toml`:
```
uv sync               # production deps only
uv sync --group dev   # includes ruff, mypy, pre-commit, pytest
```

## CLI Usage

```powershell
cxp-canary --help
cxp-canary objectives      # List attack objectives
cxp-canary formats          # List assistant formats
cxp-canary techniques       # List technique matrix (objective × format)
cxp-canary generate         # Generate poisoned test repos
cxp-canary record           # Record test result
cxp-canary validate         # Validate captured output
cxp-canary report           # Generate comparison matrix + PoC packages
```

After changes, smoke test: `cxp-canary --help`

## Key Patterns

- **Technique = Objective × Format.** Each technique is a specific attack objective applied to a specific assistant instruction file format. The technique registry is the cross-product.
- **Registries:** Objectives, formats, and techniques each have a registry module. New entries are registered by creating a module in the appropriate directory.
- **Evidence capture:** Two modes — `--file` for assistant-generated code files on disk (primary), `--output-file` for saved chat text (fallback).
- **Validation:** Per-objective validator rules (regex patterns). Each objective defines what constitutes a "hit."
- **SQLite evidence store:** Single-file, portable. Campaigns group test results from a session.

## Claude Code Guardrails

### Verification Scope
- Run only the tests for new/changed code, not the full suite
- Smoke test the CLI after changes
- Full suite verification is the developer's responsibility before merging

### Timeout Policy
- If any test run exceeds 60 seconds, stop and identify the stuck test
- Do not set longer timeouts and wait — diagnose instead

### Process Hygiene
- Before running tests, kill any orphaned python/node processes from previous runs
- After killing a stuck process, clean up zombies before retrying

### Failure Mode
- If verification hits a problem you can't resolve in 2 attempts, commit the work to the branch and report what failed
- Do not spin on the same failure

### Boundaries
- Do not create PRs or install tools. Push the branch and stop. The developer creates PRs manually.
- Do not attempt to install CLI tools (gh, hub, etc.)
- Do not create implementation plan files, design docs, or any docs/plans/ directory in the repo. NEVER commit plan files. If subagent-driven development requires a plan file, write it to the OS temp directory (`/tmp` on Unix, `TMPDIR` or `TEMP` env var), not the repo. Plans are transient session artifacts, not project documentation.

## Session Discipline

- **Architecture.md:** Update at end of session if new modules, endpoints, or data models were introduced
- **Running checks manually:**
```powershell
ruff check .
ruff format --check .
mypy src/cxp_canary/
pre-commit run --all-files
```

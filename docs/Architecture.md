# CXP-Canary — Design

## Architecture

CXP-Canary follows a three-stage pipeline: generate poisoned test repos, capture evidence from manual testing, and validate/report results.

```
┌─────────────────────────────────────────────────────────┐
│                     CXP-Canary CLI                      │
│  generate │ validate │ report │ objectives │ formats    │
└─────┬─────┴─────┬────┴────┬───┴────────────┴───────────┘
      │           │         │
      ▼           ▼         ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Payload  │ │ Output   │ │ Reporter │
│ Engine   │ │ Validator│ │          │
└────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │             │
     ▼            ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Repo     │ │ Evidence │ │ Artifacts│
│ Builder  │ │ Store    │ │ (PoCs,   │
│          │ │ (SQLite) │ │ reports) │
└──────────┘ └──────────┘ └──────────┘
```

### Component Descriptions

**Payload Engine** — Selects and renders poisoned context file content from the technique registry. Each technique is an objective × format combination. The engine resolves the template, injects any dynamic content (target function names, exfil URLs), and produces the poisoned file content.

**Repo Builder** — Packages poisoned context files into minimal, self-contained test repositories. Each repo contains: the poisoned instruction file, a minimal project skeleton (enough code for the assistant to have context), a trigger prompt file (`TRIGGER.md`) documenting the exact prompt the researcher should use, and a `README.md` with testing instructions.

**Output Validator** — Evaluates captured assistant output against expected vulnerability signatures. Phase 1 uses regex pattern matching with per-objective rule sets. Each objective defines what constitutes a "hit" — e.g., backdoor insertion requires a hardcoded credential or bypass condition in the generated code. The validator module (`validator.py`) maintains a rule registry with `register_rule()`, `get_rules_for_objective()`, and `validate()` functions. Four built-in rules cover two objectives: `backdoor-hardcoded-cred` and `backdoor-bypass-condition` (both high severity) for the backdoor objective, and `exfil-outbound-call` (high) and `exfil-data-collection` (medium) for the exfil objective. Verdicts: "hit" (high-severity match), "partial" (medium/low only), "miss" (no match).

**Evidence Store** — SQLite database tracking campaigns, test results, and validation outcomes. Same design philosophy as IPI-Canary's database — single-file, portable, no external dependencies.

**Reporter** — Generates structured output from the evidence store. The module (`reporter.py`) provides four functions: `generate_matrix()` queries the evidence store, groups results by technique, and enriches with objective/format metadata from the registries. `matrix_to_markdown()` and `matrix_to_json()` render the matrix as a Markdown table or JSON respectively. `export_poc()` creates bounty-ready zip archives containing a regenerated poisoned repo (via the builder), a finding README with reproduction steps, captured evidence, and a validation report.

**CLI** — Click-based command interface. Entry point for all operations.

---

## Data Models

```python
@dataclass
class Objective:
    """What the payload tries to achieve."""
    id: str                  # e.g., "backdoor", "exfil", "dep-confusion"
    name: str                # Human-readable name
    description: str         # What success looks like
    validators: list[str]    # Validator rule IDs that detect this objective

@dataclass
class AssistantFormat:
    """Instruction file format for a specific coding assistant."""
    id: str                  # e.g., "claude-md", "cursorrules"
    filename: str            # e.g., "CLAUDE.md", ".cursorrules"
    assistant: str           # e.g., "Claude Code", "Cursor"
    syntax: str              # "markdown", "json", "plaintext"

@dataclass
class Technique:
    """A specific payload: one objective in one format."""
    id: str                  # e.g., "backdoor-claude-md-001"
    objective: Objective
    format: AssistantFormat
    template: str            # Jinja2 or string template for the poisoned file
    trigger_prompt: str      # The prompt the researcher uses to activate
    project_type: str        # "python", "javascript", "generic"

@dataclass
class TestResult:
    """One test execution: one technique against one assistant."""
    id: str                  # UUID
    campaign_id: str         # Groups results from a testing session
    technique_id: str
    assistant: str           # Which assistant was actually tested
    model: str               # Underlying model if known
    timestamp: datetime
    trigger_prompt: str      # Actual prompt used
    capture_mode: str        # "file" or "output" — how evidence was captured
    captured_files: list[str]  # Paths to captured files (file mode)
    raw_output: str          # Full text content (output mode) or concatenated file contents
    validation_result: str   # "hit", "miss", "partial", "error"
    validation_details: str  # What the validator found
    notes: str               # Researcher observations

@dataclass
class ValidatorRule:
    """A single detection pattern."""
    id: str                  # e.g., "backdoor-hardcoded-cred"
    objective_id: str        # Which objective this rule belongs to
    name: str                # Human-readable name
    description: str         # What this pattern detects
    patterns: list[str]      # Regex patterns (any match = detection)
    severity: str            # "high", "medium", "low"

@dataclass
class ValidationResult:
    """Result of validating one piece of captured output."""
    verdict: str             # "hit", "miss", "partial"
    matched_rules: list[str] # Rule IDs that matched
    details: str             # Human-readable summary of findings

@dataclass
class Campaign:
    """A testing session grouping multiple test results."""
    id: str                  # UUID
    name: str                # e.g., "2026-03-01-cursor-backdoors"
    created: datetime
    description: str
```

---

## Schema

### SQLite Tables

```sql
CREATE TABLE campaigns (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created TEXT NOT NULL,
    description TEXT
);

CREATE TABLE test_results (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL REFERENCES campaigns(id),
    technique_id TEXT NOT NULL,
    assistant TEXT NOT NULL,
    model TEXT,
    timestamp TEXT NOT NULL,
    trigger_prompt TEXT NOT NULL,
    capture_mode TEXT NOT NULL,
    captured_files TEXT,
    raw_output TEXT NOT NULL,
    validation_result TEXT NOT NULL,
    validation_details TEXT,
    notes TEXT
);
```

---

## CLI Interface

```
cxp-canary
  generate          Generate poisoned test repos
  validate          Validate captured output against a technique's expected result
  record            Record a test result into the evidence store
  report matrix     Generate an assistant comparison matrix (Markdown or JSON)
  report poc        Export a bounty-ready PoC package (zip archive)
  objectives        List available attack objectives
  formats           List supported assistant formats
  techniques        List all techniques (objective × format matrix)
  campaigns         List campaigns and results
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--objective` | str | all | Filter by objective ID |
| `--format` | str | all | Filter by assistant format ID |
| `--output-dir` | path | `./repos` | Where to write generated test repos |
| `--campaign` | str | (auto) | Campaign ID for recording results |
| `--assistant` | str | (required) | Assistant under test (for record/validate) |
| `--model` | str | (optional) | Underlying model if known |
| `--file` | path | (required*) | Path to assistant-generated code file(s) for evidence capture |
| `--output-file` | path | (required*) | Path to raw text capture file (alternative to --file) |
| `--technique` | str | (required) | Technique ID for record/validate |

*`record` requires either `--file` or `--output-file`, not both.

**Evidence capture modes:**
- `--file` (primary): Point at file(s) the assistant wrote or modified in the test repo. This is the natural flow — coding assistants write to disk.
- `--output-file` (fallback): Point at a text file the researcher saved from chat output, for cases where the assistant responded in conversation rather than writing files.

**Validate modes:**
- `--result <id>` (Mode A): Validate a stored result from the evidence DB. Runs the validator, updates the DB with the verdict.
- `--technique <id> --file <path>` (Mode B): Validate file(s) directly against a technique. Prints verdict without storing.

---

## Extension Points

### Adding a New Objective

1. Create objective definition in `src/cxp_canary/objectives/{objective_id}.py`
2. Define validator rules (regex patterns that detect success)
3. Register in the objective registry

### Adding a New Assistant Format

1. Create format definition in `src/cxp_canary/formats/{format_id}.py`
2. Define the filename, syntax type, and any format-specific rendering rules
3. Register in the format registry

### Adding a New Technique

1. Create technique template in `src/cxp_canary/techniques/templates/{objective_id}/{format_id}.{ext}.j2`
2. Add trigger prompt to `_TRIGGER_PROMPTS` in `src/cxp_canary/techniques/__init__.py`
3. Techniques are the cross-product — one objective applied to one format
4. New objectives or formats automatically generate new technique combinations

---

## Security Considerations

- Generated test repos contain intentionally malicious instruction files. The repos must be clearly labeled with warnings in README.md.
- Output validator patterns must not be so broad they produce false positives — a "hit" must represent genuine vulnerability.
- Bounty-ready PoC packages include potentially sensitive evidence. Encrypt or handle with care.
- Responsible use policy required in README: test only against your own instances or vendors with active VDPs/bounty programs.
- No automated submission to vendor APIs in Phase 1. Researcher controls all interaction.

---

## Documentation Standards

- Google-style docstrings (Args, Returns, Raises, Example)
- New modules get docstrings when created, not retrofitted
- Inline comments for non-obvious logic only

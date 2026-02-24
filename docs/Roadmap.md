# CXP-Canary — Roadmap

## Problem Statement

AI coding assistants (Claude Code, Cursor, GitHub Copilot, Windsurf, Codex) treat project-level instruction files as trusted context. These files — CLAUDE.md, .cursorrules, copilot-instructions.md, AGENTS.md — live in repositories that may be forked, cloned from untrusted sources, or contributed to by external parties. Academic research (arxiv 2601.17548v1) catalogs 42+ attack techniques, but no packaged offensive testing tool exists for practitioners to reproduce, measure, or bounty-submit these findings. CXP-Canary fills that gap.

---

## Phased Delivery

### Phase 1: Foundation

**Goal:** Generate poisoned test repos, capture evidence from manual testing, and validate whether the assistant produced vulnerable code. Prove the attack works against real assistants and produce bounty-ready evidence.

**Deliverables:**
- Payload corpus: 2 initial objectives (backdoor insertion, credential exfiltration) across 3 assistant formats (CLAUDE.md, .cursorrules, copilot-instructions.md)
- Repo builder: generates minimal test repos with poisoned instruction file, project skeleton, trigger prompt, and testing instructions
- Evidence capture: `record` command stores test results in SQLite with campaign grouping
- Output validation: regex pattern matching per objective — detects hardcoded credentials, exfiltration calls, bypass conditions in captured code
- Reporting: assistant comparison matrix (Markdown/JSON), bounty-ready PoC package export (zip)
- CLI: generate, validate, record, report, objectives, formats, techniques, campaigns

**Done when:**
- `cxp-canary generate` produces test repos for all objective × format combinations
- `cxp-canary record` + `cxp-canary validate` captures and evaluates a manual test result
- `cxp-canary report` generates a comparison matrix from stored results
- At least one real test run completed against a coding assistant with evidence captured
- README includes responsible use policy

### Phase 2: Expansion

**Goal:** Broader coverage of objectives, formats, and validation methods. Begin headless automation where APIs allow.

**Deliverables:**
- Additional objectives: dependency confusion, permission escalation, command execution
- Additional formats: AGENTS.md, .windsurfrules, .gemini/settings.json
- AST-based output validation: structural vulnerability detection beyond regex
- Headless assistant adapters: API-based interaction for assistants that support it (Codex CLI, Claude Code if ToS permits)
- Multi-file poisoning: instruction file + supporting project files (requirements.txt, README.md with misleading architecture)
- Richer project skeletons: language-specific templates (Python, JavaScript, Go) for more realistic test scenarios

**Done when:**
- 4+ objectives, 5+ formats in the technique registry
- At least one headless adapter producing end-to-end automated results
- AST validator catching structural vulnerabilities that regex misses
- Published findings from expanded testing

### Phase 3: Maturity

**Goal:** Full automation, community adoption, detection engineering output.

**Deliverables:**
- Headless adapters for all major assistants (API + terminal + IDE automation where feasible)
- Sandbox-based output validation: execute generated code in isolated environment to confirm behavior
- CI integration: regression testing to detect when assistants fix or introduce vulnerabilities
- Sigma/Wazuh detection rules for context file poisoning patterns
- Community contribution format: standardized technique submission template
- Comprehensive documentation and examples for adoption by other security researchers

**Done when:**
- Automated end-to-end testing across 3+ assistants
- Detection rules published and tested against real poisoning attempts
- External researchers contributing techniques or using the tool for their own bounty submissions

---

## What Success Looks Like

- A bounty or CVE from a context file poisoning finding discovered with CXP-Canary
- Detection rules that catch real context file poisoning patterns in developer environments
- An assistant comparison matrix that shows which tools are most/least susceptible — published and referenced
- Blog posts documenting novel techniques learned through systematic testing

---

## Out of Scope (for now)

- IDE extension development (Cursor/Windsurf plugin automation) — too brittle for Phase 1-2
- Training data poisoning — different attack surface, different tool
- Runtime agent exploitation (MCP, tool calls) — that's CounterAgent's domain
- Model-level jailbreaks — CXP-Canary tests the application layer, not the model

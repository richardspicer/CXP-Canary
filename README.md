# CXP-Canary

Context poisoning tester for AI coding assistants.

CXP-Canary generates poisoned project instruction files (CLAUDE.md, .cursorrules, copilot-instructions.md, etc.), packages them into minimal test repositories, and provides structured evidence capture and validation to determine whether coding assistants produce vulnerable code, exfiltrate data, or execute commands when exposed to poisoned context.

Part of the [Volery](https://github.com/richardspicer/volery) offensive security program. Sister program: [CounterAgent](https://github.com/richardspicer/counteragent).

## Status

**Pre-release** — Phase 1 development.

## Install

```bash
git clone https://github.com/richardspicer/CXP-Canary.git
cd CXP-Canary
uv sync
```

## Usage

```bash
cxp-canary --help
cxp-canary objectives      # List attack objectives
cxp-canary formats          # List supported assistant formats
cxp-canary techniques       # List technique matrix
cxp-canary generate         # Generate poisoned test repos
cxp-canary record           # Record test results
cxp-canary validate         # Validate captured output
cxp-canary report           # Generate comparison matrices and PoC packages
```

## Responsible Use

CXP-Canary is a security testing tool for authorized research. Test only against:
- Coding assistants you have permission to test
- Vendors with active bug bounty programs or vulnerability disclosure policies
- Your own local instances

Do not submit poisoned context files to vendor APIs without authorization.

## Documentation

- [Roadmap](docs/Roadmap.md) — Phased development plan
- [Architecture](docs/Architecture.md) — Components, data models, extension points
- [Contributing](CONTRIBUTING.md) — Git workflow and code standards

## AI Assistance Disclosure

This project uses a human-led, AI-augmented development workflow. See [AI-STATEMENT.md](AI-STATEMENT.md).

## License

[MIT](LICENSE)

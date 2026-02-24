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

CXP-Canary is for **authorized security testing only**. By using this tool, you agree to the following:

- **Test only what you're authorized to test.** Use against your own local instances, or against vendors with active bug bounty programs or vulnerability disclosure policies. Do not test against systems without explicit permission.
- **Handle generated repos with care.** Test repositories contain intentionally malicious instruction files designed to manipulate coding assistants. Never deploy them to production environments or shared workspaces where they could affect others.
- **Follow responsible disclosure.** When you discover a vulnerability, report it through the vendor's official disclosure channel. Do not publish findings publicly until the vendor has had reasonable time to respond.
- **No automated assistant interaction.** CXP-Canary generates test repos and captures evidence, but the researcher manually controls all interactions with coding assistants. The tool does not automatically submit prompts or interact with any AI assistant.
- **No malware, no production attacks.** Do not use CXP-Canary to create actual malware, attack production systems, or cause harm. This is a research tool for improving AI safety.

## Documentation

- [Roadmap](docs/Roadmap.md) — Phased development plan
- [Architecture](docs/Architecture.md) — Components, data models, extension points
- [Contributing](CONTRIBUTING.md) — Git workflow and code standards

## AI Assistance Disclosure

This project uses a human-led, AI-augmented development workflow. See [AI-STATEMENT.md](AI-STATEMENT.md).

## License

[MIT](LICENSE)

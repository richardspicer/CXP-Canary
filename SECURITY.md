# Security Policy

## Intended Use

CXP-Canary is a security testing tool for authorized research into AI coding assistant vulnerabilities. It is designed to test coding assistants **you own, control, or have explicit permission to test** through active bug bounty programs or vulnerability disclosure policies.

## Responsible Use

- **Get permission** before testing any coding assistant you don't own or that lacks a public VDP/bounty program
- **Do not submit** poisoned context files to vendor APIs without authorization
- **Handle evidence carefully** — captured outputs and PoC packages may contain sensitive information
- **Label generated repos clearly** — poisoned test repos must include prominent warnings

## Trust Model

| Component | Trust Level | Notes |
|-----------|-------------|-------|
| CLI operator | Trusted | Full control of payload generation, evidence capture, and reporting |
| Generated test repos | Adversarial output | Contain intentionally malicious instruction files — only use against authorized targets |
| Evidence store (SQLite) | Local, trusted | Researcher's own test results — no external input |
| Captured assistant output | Untrusted input | May contain code with real vulnerabilities — do not execute outside sandboxes |
| PoC packages (zip) | Sensitive output | Contain poisoned files + evidence — handle with care |

## Reporting Security Issues

If you find a security vulnerability in CXP-Canary:

1. **Do not open a public issue**
2. Email: security@richardspicer.io
3. Include: description, reproduction steps, impact assessment

We aim to respond within 48 hours and provide a fix within 7 days for critical issues.

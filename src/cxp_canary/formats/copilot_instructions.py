"""copilot-instructions.md format for GitHub Copilot."""

from __future__ import annotations

from cxp_canary.formats import register
from cxp_canary.models import AssistantFormat

COPILOT_INSTRUCTIONS = AssistantFormat(
    id="copilot-instructions",
    filename=".github/copilot-instructions.md",
    assistant="GitHub Copilot",
    syntax="markdown",
)

register(COPILOT_INSTRUCTIONS)

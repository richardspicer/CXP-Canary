""".cursorrules format for Cursor."""

from __future__ import annotations

from cxp_canary.formats import register
from cxp_canary.models import AssistantFormat

CURSORRULES = AssistantFormat(
    id="cursorrules",
    filename=".cursorrules",
    assistant="Cursor",
    syntax="plaintext",
)

register(CURSORRULES)

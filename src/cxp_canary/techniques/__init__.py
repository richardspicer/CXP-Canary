"""Technique registry -- cross-product of objectives and formats.

Each technique pairs one attack objective with one assistant format.
The registry is built automatically from the objective and format registries.
"""

from __future__ import annotations

from cxp_canary.formats import list_formats
from cxp_canary.models import Technique
from cxp_canary.objectives import list_objectives

_registry: dict[str, Technique] = {}


def _build_registry() -> None:
    """Build technique registry from the cross-product of objectives x formats."""
    for objective in list_objectives():
        for fmt in list_formats():
            technique_id = f"{objective.id}-{fmt.id}"
            _registry[technique_id] = Technique(
                id=technique_id,
                objective=objective,
                format=fmt,
                template="TODO: template",
                trigger_prompt="TODO: trigger prompt",
                project_type="python",
            )


def get_technique(technique_id: str) -> Technique | None:
    """Look up a technique by ID.

    Args:
        technique_id: The technique identifier.

    Returns:
        The technique, or None if not found.
    """
    if not _registry:
        _build_registry()
    return _registry.get(technique_id)


def list_techniques() -> list[Technique]:
    """Return all registered techniques.

    Returns:
        List of all techniques.
    """
    if not _registry:
        _build_registry()
    return list(_registry.values())

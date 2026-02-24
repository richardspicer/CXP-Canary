"""Reporter module -- generates comparison matrices and PoC packages."""

from __future__ import annotations

import sqlite3
from collections import defaultdict
from datetime import UTC, datetime

from cxp_canary.evidence import list_results
from cxp_canary.techniques import get_technique


def generate_matrix(conn: sqlite3.Connection, campaign_id: str | None = None) -> dict:
    """Generate an assistant comparison matrix from stored results.

    Queries the evidence store for test results, groups them by technique,
    and enriches with objective/format metadata from the registries.

    Args:
        conn: An open SQLite connection.
        campaign_id: Optional campaign ID to filter by. None means all results.

    Returns:
        A dict with keys: generated, campaign, summary, matrix.
    """
    results = list_results(conn, campaign_id=campaign_id)

    summary = {"total": 0, "hits": 0, "misses": 0, "partial": 0, "pending": 0}
    grouped: dict[str, list] = defaultdict(list)

    for r in results:
        summary["total"] += 1
        if r.validation_result == "hit":
            summary["hits"] += 1
        elif r.validation_result == "miss":
            summary["misses"] += 1
        elif r.validation_result == "partial":
            summary["partial"] += 1
        else:
            summary["pending"] += 1

        grouped[r.technique_id].append(r)

    matrix = []
    for technique_id, technique_results in grouped.items():
        technique = get_technique(technique_id)
        objective_name = technique.objective.name if technique else technique_id
        format_name = technique.format.filename if technique else technique_id

        entry = {
            "technique_id": technique_id,
            "objective": objective_name,
            "format": format_name,
            "results": [
                {
                    "assistant": r.assistant,
                    "model": r.model,
                    "validation_result": r.validation_result,
                    "timestamp": r.timestamp.isoformat(),
                }
                for r in technique_results
            ],
        }
        matrix.append(entry)

    return {
        "generated": datetime.now(UTC).isoformat(),
        "campaign": campaign_id or "all",
        "summary": summary,
        "matrix": matrix,
    }

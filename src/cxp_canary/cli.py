"""CXP-Canary CLI — Click-based command interface."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import click

from cxp_canary import __version__
from cxp_canary.evidence import (
    create_campaign,
    get_campaign,
    get_db,
    list_campaigns,
    list_results,
    record_result,
)
from cxp_canary.formats import list_formats
from cxp_canary.objectives import list_objectives
from cxp_canary.techniques import get_technique, list_techniques


@click.group()
@click.version_option(version=__version__, prog_name="cxp-canary")
def main() -> None:
    """CXP-Canary — Context poisoning tester for AI coding assistants."""


@main.command()
def objectives() -> None:
    """List available attack objectives."""
    objs = list_objectives()
    if not objs:
        click.echo("No objectives registered.")
        return
    click.echo(f"{'ID':<20} {'Name':<30} Description")
    click.echo("-" * 80)
    for obj in objs:
        click.echo(f"{obj.id:<20} {obj.name:<30} {obj.description}")


@main.command()
def formats() -> None:
    """List supported assistant formats."""
    fmts = list_formats()
    if not fmts:
        click.echo("No formats registered.")
        return
    click.echo(f"{'ID':<25} {'Filename':<35} {'Assistant':<20} Syntax")
    click.echo("-" * 95)
    for fmt in fmts:
        click.echo(f"{fmt.id:<25} {fmt.filename:<35} {fmt.assistant:<20} {fmt.syntax}")


@main.command()
def techniques() -> None:
    """List all techniques (objective x format matrix)."""
    techs = list_techniques()
    if not techs:
        click.echo("No techniques registered.")
        return
    click.echo(f"{'Technique ID':<35} {'Objective':<20} {'Format':<25} Type")
    click.echo("-" * 95)
    for tech in techs:
        click.echo(
            f"{tech.id:<35} {tech.objective.id:<20} {tech.format.id:<25} {tech.project_type}"
        )


@main.command()
@click.option("--technique", required=True, help="Technique ID to test.")
@click.option("--assistant", required=True, help="Assistant under test.")
@click.option("--trigger-prompt", required=True, help="Prompt used to trigger.")
@click.option(
    "--file",
    "files",
    multiple=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to assistant-generated code file(s).",
)
@click.option(
    "--output-file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to saved chat output file.",
)
@click.option("--campaign", "campaign_id", default=None, help="Existing campaign ID.")
@click.option("--model", default="", help="Underlying model name.")
@click.option("--notes", default="", help="Researcher observations.")
@click.option(
    "--db",
    "db_path",
    default=None,
    type=click.Path(path_type=Path),
    help="Database path (default: ./cxp-canary.db).",
)
def record(
    technique: str,
    assistant: str,
    trigger_prompt: str,
    files: tuple[Path, ...],
    output_file: Path | None,
    campaign_id: str | None,
    model: str,
    notes: str,
    db_path: Path | None,
) -> None:
    """Record a test result into the evidence store."""
    # Validate mutual exclusivity
    if files and output_file:
        raise click.UsageError("--file and --output-file are mutually exclusive.")
    if not files and not output_file:
        raise click.UsageError("Either --file or --output-file is required.")

    # Validate technique
    if get_technique(technique) is None:
        raise click.UsageError(f"Unknown technique: {technique}")

    # Determine capture mode and raw output
    captured_files: list[str] = []
    if files:
        capture_mode = "file"
        captured_files = [str(f) for f in files]
        raw_output = "\n".join(f.read_text() for f in files)
    else:
        capture_mode = "output"
        assert output_file is not None
        raw_output = output_file.read_text()

    # Open DB and resolve campaign
    conn = get_db(db_path)
    if campaign_id:
        campaign = get_campaign(conn, campaign_id)
        if campaign is None:
            conn.close()
            raise click.UsageError(f"Campaign not found: {campaign_id}")
    else:
        name = f"{date.today().isoformat()}-{assistant}"
        campaign = create_campaign(conn, name)

    result = record_result(
        conn,
        campaign_id=campaign.id,
        technique_id=technique,
        assistant=assistant,
        trigger_prompt=trigger_prompt,
        raw_output=raw_output,
        capture_mode=capture_mode,
        model=model,
        captured_files=captured_files,
        notes=notes,
    )
    conn.close()

    click.echo(f"Result:   {result.id}")
    click.echo(f"Campaign: {campaign.id}")


@main.command()
@click.argument("campaign_id", required=False, default=None)
@click.option(
    "--db",
    "db_path",
    default=None,
    type=click.Path(path_type=Path),
    help="Database path (default: ./cxp-canary.db).",
)
def campaigns(campaign_id: str | None, db_path: Path | None) -> None:
    """List campaigns and results."""
    conn = get_db(db_path)

    if campaign_id is None:
        # List all campaigns
        camps = list_campaigns(conn)
        if not camps:
            click.echo("No campaigns found.")
            conn.close()
            return
        click.echo(f"{'ID':<38} {'Name':<30} {'Created':<22} Results")
        click.echo("-" * 95)
        for c in camps:
            count = len(list_results(conn, c.id))
            created_str = c.created.strftime("%Y-%m-%d %H:%M")
            click.echo(f"{c.id:<38} {c.name:<30} {created_str:<22} {count}")
    else:
        # Show campaign detail
        campaign = get_campaign(conn, campaign_id)
        if campaign is None:
            conn.close()
            raise click.UsageError(f"Campaign not found: {campaign_id}")
        click.echo(f"Campaign: {campaign.name}")
        click.echo(f"ID:       {campaign.id}")
        click.echo(f"Created:  {campaign.created.isoformat()}")
        if campaign.description:
            click.echo(f"Desc:     {campaign.description}")
        results = list_results(conn, campaign.id)
        click.echo(f"\nResults ({len(results)}):")
        if results:
            click.echo(f"  {'ID':<38} {'Technique':<30} {'Assistant':<20} Status")
            click.echo("  " + "-" * 93)
            for r in results:
                click.echo(
                    f"  {r.id:<38} {r.technique_id:<30} {r.assistant:<20} {r.validation_result}"
                )
    conn.close()

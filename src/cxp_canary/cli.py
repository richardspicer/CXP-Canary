"""CXP-Canary CLI — Click-based command interface."""

from __future__ import annotations

import click

from cxp_canary import __version__
from cxp_canary.formats import list_formats
from cxp_canary.objectives import list_objectives
from cxp_canary.techniques import list_techniques


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

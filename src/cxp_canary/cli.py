"""CXP-Canary CLI — Click-based command interface."""

import click

from cxp_canary import __version__


@click.group()
@click.version_option(version=__version__, prog_name="cxp-canary")
def main() -> None:
    """CXP-Canary — Context poisoning tester for AI coding assistants."""


@main.command()
def objectives() -> None:
    """List available attack objectives."""
    click.echo("No objectives registered yet.")


@main.command()
def formats() -> None:
    """List supported assistant formats."""
    click.echo("No formats registered yet.")


@main.command()
def techniques() -> None:
    """List all techniques (objective × format matrix)."""
    click.echo("No techniques registered yet.")

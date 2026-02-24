"""Tests for generate CLI command."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from cxp_canary.cli import main


class TestGenerateCommand:
    def test_generate_all(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(main, ["generate", "--output-dir", str(tmp_path)])
        assert result.exit_code == 0
        assert "Generated 6 test repo(s)" in result.output

    def test_generate_filter_objective(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            main, ["generate", "--objective", "backdoor", "--output-dir", str(tmp_path)]
        )
        assert result.exit_code == 0
        assert "Generated 3 test repo(s)" in result.output

    def test_generate_filter_format(self, tmp_path: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(
            main, ["generate", "--format", "claude-md", "--output-dir", str(tmp_path)]
        )
        assert result.exit_code == 0
        assert "Generated 2 test repo(s)" in result.output

    def test_generate_creates_directories(self, tmp_path: Path) -> None:
        runner = CliRunner()
        runner.invoke(main, ["generate", "--output-dir", str(tmp_path)])
        dirs = [d.name for d in tmp_path.iterdir() if d.is_dir()]
        assert len(dirs) == 6
        assert "backdoor-claude-md" in dirs

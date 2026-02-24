"""Tests for the campaigns CLI command."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from cxp_canary.cli import main
from cxp_canary.evidence import create_campaign, get_db, record_result


class TestCampaignsCommand:
    def test_campaigns_list_empty(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        # Touch DB so it exists
        get_db(db_path).close()
        result = CliRunner().invoke(main, ["campaigns", "--db", str(db_path)])
        assert result.exit_code == 0
        assert "No campaigns" in result.output

    def test_campaigns_list(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        conn = get_db(db_path)
        c = create_campaign(conn, "test-campaign", "A test")
        record_result(conn, c.id, "t1", "a", "p", "o", "file")
        conn.close()
        result = CliRunner().invoke(main, ["campaigns", "--db", str(db_path)])
        assert result.exit_code == 0
        assert "test-campaign" in result.output

    def test_campaigns_detail(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        conn = get_db(db_path)
        c = create_campaign(conn, "test-campaign", "A test")
        record_result(conn, c.id, "t1", "Claude Code", "p", "o", "file")
        conn.close()
        result = CliRunner().invoke(main, ["campaigns", c.id, "--db", str(db_path)])
        assert result.exit_code == 0
        assert "test-campaign" in result.output
        assert "Claude Code" in result.output

    def test_campaigns_detail_not_found(self, tmp_path: Path) -> None:
        db_path = tmp_path / "test.db"
        get_db(db_path).close()
        result = CliRunner().invoke(main, ["campaigns", "nonexistent", "--db", str(db_path)])
        assert result.exit_code != 0

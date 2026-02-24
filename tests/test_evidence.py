"""Tests for the evidence store."""

from __future__ import annotations

import sqlite3

from cxp_canary.evidence import (
    create_campaign,
    get_campaign,
    init_db,
    list_campaigns,
)
from cxp_canary.models import Campaign


class TestInitDb:
    def test_init_db(self) -> None:
        conn = sqlite3.connect(":memory:")
        init_db(conn)
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        assert "campaigns" in tables
        assert "test_results" in tables
        conn.close()

    def test_init_db_idempotent(self) -> None:
        conn = sqlite3.connect(":memory:")
        init_db(conn)
        init_db(conn)  # should not raise
        conn.close()


class TestCampaignCrud:
    def test_create_campaign(self) -> None:
        conn = sqlite3.connect(":memory:")
        init_db(conn)
        campaign = create_campaign(conn, "test-campaign", "A test campaign")
        assert isinstance(campaign, Campaign)
        assert campaign.name == "test-campaign"
        assert campaign.description == "A test campaign"
        assert len(campaign.id) == 36  # UUID format
        assert campaign.created is not None
        conn.close()

    def test_get_campaign(self) -> None:
        conn = sqlite3.connect(":memory:")
        init_db(conn)
        created = create_campaign(conn, "test-campaign")
        fetched = get_campaign(conn, created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.name == created.name
        conn.close()

    def test_get_campaign_not_found(self) -> None:
        conn = sqlite3.connect(":memory:")
        init_db(conn)
        assert get_campaign(conn, "nonexistent") is None
        conn.close()

    def test_list_campaigns(self) -> None:
        conn = sqlite3.connect(":memory:")
        init_db(conn)
        create_campaign(conn, "first")
        create_campaign(conn, "second")
        campaigns = list_campaigns(conn)
        assert len(campaigns) == 2
        assert all(isinstance(c, Campaign) for c in campaigns)
        # newest first
        assert campaigns[0].name == "second"
        conn.close()

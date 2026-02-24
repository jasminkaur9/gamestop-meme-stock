"""Tests for GameStop Meme Stock Q&A app."""

from pathlib import Path

import app


# ---------------------------------------------------------------------------
# Case data
# ---------------------------------------------------------------------------

CASE_PATH = Path(__file__).parent / "case_data" / "gamestop_squeeze.md"


def test_case_file_exists():
    assert CASE_PATH.exists(), "case_data/gamestop_squeeze.md must exist"


def test_case_content_loads():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert len(content) > 500, "Case content should be substantial"


def test_case_has_background():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert "Background" in content


def test_case_has_timeline():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert "Timeline" in content


def test_case_has_key_data():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert "Key Data" in content


def test_case_has_contagion():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert "Contagion" in content


def test_case_has_transfer_entropy():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert "Transfer Entropy" in content


def test_case_has_driver():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert "DRIVER" in content


def test_case_has_critical_data_points():
    content = CASE_PATH.read_text(encoding="utf-8")
    assert "140%" in content, "Should mention 140% short interest"
    assert "483" in content, "Should mention $483 peak"
    assert "6.8" in content, "Should mention Melvin's $6.8B loss"
    assert "Robinhood" in content, "Should mention Robinhood"
    assert "January 28" in content or "Jan 28" in content, "Should mention Jan 28"


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------


def test_system_prompt_template():
    assert "{case_content}" in app.SYSTEM_PROMPT_TEMPLATE


def test_build_system_prompt():
    result = app.build_system_prompt("test case content here")
    assert "test case content here" in result
    assert "GameStop" in result
    assert "DRIVER" in result


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_example_questions_structure():
    assert len(app.EXAMPLE_QUESTIONS) >= 5
    for item in app.EXAMPLE_QUESTIONS:
        assert isinstance(item, tuple)
        assert len(item) == 2
        emoji, question = item
        assert isinstance(emoji, str)
        assert isinstance(question, str)
        assert question.endswith("?") or question.endswith(".")


def test_timeline_events_structure():
    assert len(app.TIMELINE_EVENTS) >= 8
    for item in app.TIMELINE_EVENTS:
        assert isinstance(item, tuple)
        assert len(item) == 3


def test_contagion_flow_steps():
    assert len(app.CONTAGION_FLOW_STEPS) >= 3
    for step in app.CONTAGION_FLOW_STEPS:
        assert "label" in step
        assert "detail" in step


def test_did_you_know_facts():
    assert len(app.DID_YOU_KNOW_FACTS) >= 5
    for fact in app.DID_YOU_KNOW_FACTS:
        assert isinstance(fact, str)
        assert len(fact) > 10


def test_ticker_items():
    assert len(app.TICKER_ITEMS) >= 5
    for item in app.TICKER_ITEMS:
        assert isinstance(item, str)


def test_key_metrics():
    assert len(app.KEY_METRICS) >= 4
    for m in app.KEY_METRICS:
        assert "label" in m
        assert "value" in m
        assert "delta" in m


def test_gme_price_timeline():
    assert len(app.GME_PRICE_TIMELINE) >= 5
    for date, price in app.GME_PRICE_TIMELINE.items():
        assert isinstance(price, (int, float))
        assert price > 0


def test_short_interest_data():
    assert len(app.SHORT_INTEREST_DATA) >= 3
    for period, si in app.SHORT_INTEREST_DATA.items():
        assert isinstance(si, (int, float))


def test_meme_stock_returns():
    assert "GME" in app.MEME_STOCK_RETURNS
    assert "AMC" in app.MEME_STOCK_RETURNS
    assert app.MEME_STOCK_RETURNS["GME"] > app.MEME_STOCK_RETURNS["AMC"]

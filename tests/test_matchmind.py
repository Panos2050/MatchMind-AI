import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import json
from main import get_all_matches, create_report, greek_teams

def test_team_list_not_empty():
    assert len(greek_teams) > 0, "Greek teams list should not be empty"

def test_fetch_matches():
    matches = get_all_matches()
    assert isinstance(matches, set)
    assert all(isinstance(m, str) for m in matches)
    # Should return at least one valid match string
    assert any("-" in m for m in matches), "No valid matches found"

def test_create_report_summary():
    match = "Olympiacos 2-1 PAOK"
    report, summary = create_report(match)
    assert "Olympiacos" in report
    assert "PAOK" in report
    assert isinstance(summary, str)
    assert len(summary) > 0, "Summary should not be empty"

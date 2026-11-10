import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from scoring import score_lead

@patch('scoring.llm')
def test_score_lead_valid_json(mock_llm):
    mock_response = MagicMock()
    mock_response.content = '{"score": 85, "rationale": "Great fit", "signals": ["SaaS", "US"]}'
    
    mock_llm.invoke.return_value = mock_response

    result = score_lead("TestCorp", "Some research data")
    
    assert result["score"] == 85
    assert result["rationale"] == "Great fit"
    assert "SaaS" in result["signals"]

@patch('scoring.llm')
def test_score_lead_handles_markdown_fences(mock_llm):
    mock_response = MagicMock()
    mock_response.content = '```json\n{"score": 90, "rationale": "Excellent", "signals": ["B2B"]}\n```'
    
    mock_llm.invoke.return_value = mock_response

    result = score_lead("TestCorp", "Some research data")
    
    assert result["score"] == 90
    assert result["rationale"] == "Excellent"
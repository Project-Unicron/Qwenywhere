import pytest
from app.tools import execute_tool_call

def test_calculator_tool_basic():
    result = execute_tool_call("calculator", {"expression": "2 + 2"})
    assert result["result"] == 4

def test_calculator_tool_math():
    result = execute_tool_call("calculator", {"expression": "16 ** 0.5"})
    assert result["result"] == 4.0

def test_calculator_tool_invalid():
    result = execute_tool_call("calculator", {"expression": "2 +"})
    assert "error" in result
def test_unknown_tool():
    result = execute_tool_call("not_a_tool", {})
    assert "error" in result

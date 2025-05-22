"""
Qwenywhere Tool Registry and Execution
- Define your available tools/functions here.
- Each tool should be a Python function, registered in the TOOL_REGISTRY dict.
- Tools should follow the OpenAI function-calling spec for input/output.
"""
from typing import Any, Dict
import math

# Example tool: calculator

def calculator_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    A simple calculator tool that evaluates a math expression.
    arguments: {"expression": "2 + 2"}
    Returns: {"result": 4}
    """
    expr = arguments.get("expression", "")
    try:
        # WARNING: eval is unsafe for arbitrary input. Use a safe parser in production!
        result = eval(expr, {"__builtins__": {}}, {"math": math})
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# Weather tool

def get_weather(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock weather tool. Ignores input and returns a fixed weather string.
    Returns: {"weather": "cloudy"}
    """
    return {"weather": "cloudy"}

# Time of day tool

def get_time_of_day(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mock time tool. Ignores input and returns a fixed part of day.
    Returns: {"time_of_day": "night"}
    """
    return {"time_of_day": "night"}

# Tool registry: maps function name to function
TOOL_REGISTRY = {
    "calculator": calculator_tool,
    "get_weather": get_weather,
    "get_time_of_day": get_time_of_day,
}

def execute_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes a tool by name with given arguments.
    Returns the tool result as a dict.
    """
    func = TOOL_REGISTRY.get(tool_name)
    if not func:
        return {"error": f"Tool '{tool_name}' not found."}
    return func(arguments)

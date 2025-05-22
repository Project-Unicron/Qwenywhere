import os
import logging
import sys
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Literal, Union
import requests
from dotenv import load_dotenv
import json
from app.tools import execute_tool_call

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Ensure logs go to stdout for Docker
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

app = FastAPI()

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: List[Message]
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.8
    top_p: Optional[float] = 1.0
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[dict] = None
    user: Optional[str] = None
    n: Optional[int] = 1
    seed: Optional[int] = None
    functions: Optional[list] = None
    function_call: Optional[Union[str, dict]] = None
    tool_choice: Optional[str] = None
    tools: Optional[list] = None
    # Note: Not all parameters are used by the backend yet, but included for OpenAI API compatibility.


def count_tokens(text):
    # Simple whitespace tokenization (approximate)
    return len(text.split()) if text else 0

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    model = req.model or OLLAMA_MODEL
    has_system = any(m.role == "system" for m in req.messages)
    messages = [m.model_dump() for m in req.messages]
    if not has_system:
        try:
            sys_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "system.txt"))
            logger.info(f"Attempting to load system prompt from: {sys_path}")
            with open(sys_path, "r", encoding="utf-8") as f:
                sys_prompt = f.read().strip()
            logger.info(f"No system prompt provided; loaded default from app/system.txt. Preview: {sys_prompt[:80]}...")
        except Exception as e:
            logger.error(f"Failed to load system.txt: {e}")
            sys_prompt = ""
        explicit_tool_instruction = (" When you receive tool results as messages with role 'tool', you must always synthesize a final answer for the user using the information in those tool messages. "
            "Do not stop until you have given a final, natural language answer to the user.")
        if explicit_tool_instruction not in sys_prompt:
            sys_prompt = sys_prompt.strip() + explicit_tool_instruction
        messages.insert(0, {"role": "system", "content": sys_prompt})
    # Iterative tool-calling loop
    max_iterations = 5
    tool_outputs_accum = []
    for _ in range(max_iterations):
        logger.info(f"[Tool Loop] Conversation sent to model: {json.dumps(messages, indent=2)}")
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "max_tokens": req.max_tokens,
            "temperature": req.temperature,
            "top_p": req.top_p,
            "stop": req.stop,
            "presence_penalty": req.presence_penalty,
            "frequency_penalty": req.frequency_penalty,
            "logit_bias": req.logit_bias,
            "user": req.user,
            "n": req.n,
            "seed": req.seed,
            "functions": req.functions,
            "function_call": req.function_call,
            "tool_choice": req.tool_choice,
            "tools": req.tools
        }
        logger.info(f"[Tool Loop] Sending payload to Ollama: {payload}")
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=60)
        data = r.json()
        logger.info(f"[Tool Loop] Ollama raw response: {data}")
        tool_calls = []
        content = ''
        finish_reason = data.get('done_reason', 'stop')
        if isinstance(data, dict):
            if 'choices' in data and data['choices']:
                choice = data['choices'][0]
                if 'message' in choice and 'tool_calls' in choice['message']:
                    tool_calls = choice['message']['tool_calls']
                    content = choice['message'].get('content', '')
                elif 'message' in choice and 'function_call' in choice['message']:
                    tool_calls = [choice['message']['function_call']]
                    content = choice['message'].get('content', '')
                else:
                    content = choice['message'].get('content', '')
            elif 'messages' in data and data['messages']:
                for msg in data['messages']:
                    if msg.get('role') == 'assistant':
                        if 'tool_calls' in msg:
                            tool_calls = msg['tool_calls']
                            content = msg.get('content', '')
                        elif 'function_call' in msg:
                            tool_calls = [msg['function_call']]
                            content = msg.get('content', '')
                        else:
                            content = msg.get('content', '')
                        break
            elif 'message' in data:
                content = data['message'].get('content', '')
        logger.info(f"[Tool Loop] Parsed tool_calls: {tool_calls}, content: {content}")
        # If no tool calls, return the final answer
        if not tool_calls:
            prompt_tokens = sum(count_tokens(m['content']) for m in messages)
            completion_tokens = count_tokens(content)
            response = {
                "id": "chatcmpl-1",
                "object": "chat.completion",
                "created": int(os.times().elapsed),
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": content},
                        "finish_reason": finish_reason
                    }
                ],
                "tool_outputs": tool_outputs_accum,
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens
                }
            }
            return JSONResponse(response)
        # Otherwise, execute tool calls and append results as tool messages
        tool_results = []
        import uuid
        for call in tool_calls:
            if isinstance(call, dict):
                # Ensure every tool call has a unique id
                tool_call_id = call.get('id') or str(uuid.uuid4())
                if 'function' in call:
                    tool_name = call['function'].get('name')
                    arguments = call['function'].get('arguments', {})
                else:
                    tool_name = call.get('name')
                    arguments = call.get('arguments', {})
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except Exception:
                        arguments = {"_raw": arguments}
                tool_result = execute_tool_call(tool_name, arguments)
                tool_results.append({
                    "tool_call_id": tool_call_id,
                    "output": tool_result
                })
                # Append as a tool message for the next round, with tool_call_id
                tool_message = {
                    "role": "tool",
                    "name": tool_name,
                    "tool_call_id": tool_call_id,
                    "content": f"Result of {tool_name}: {json.dumps(tool_result)}"
                }
                logger.info(f"[Tool Loop] Appending tool message: {tool_message}")
                messages.append(tool_message)
                logger.debug(f"[Tool Loop] Full message history after tool message: {json.dumps(messages, indent=2)}")
        tool_outputs_accum.extend(tool_results)
    # If we reach here, max iterations exceeded
    return JSONResponse({
        "error": "Too many tool call iterations, possible loop.",
        "tool_outputs": tool_outputs_accum
    }, status_code=500)
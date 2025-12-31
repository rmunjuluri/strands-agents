import json
import asyncio
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

app = FastAPI(title="Calculator MCP Server")

# -------------------------------------------------------------------
# MCP Server Info
# -------------------------------------------------------------------
SERVER_INFO = {
    "name": "calculator-mcp",
    "version": "1.0.0",
    "capabilities": {
        "tools": {}
    }
}

# -------------------------------------------------------------------
# MCP Tool Definition
# -------------------------------------------------------------------
TOOLS = [
    {
        "name": "calculator",
        "description": "Perform basic arithmetic operations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"]
                },
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        }
    }
]

# -------------------------------------------------------------------
# Calculator Logic
# -------------------------------------------------------------------
def calculate(op: str, a: float, b: float) -> float:
    if op == "add":
        return a + b
    if op == "subtract":
        return a - b
    if op == "multiply":
        return a * b
    if op == "divide":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    raise ValueError("Invalid operation")

# -------------------------------------------------------------------
# MCP Discovery Endpoint
# -------------------------------------------------------------------
@app.get("/mcp")
async def mcp_info():
    return SERVER_INFO

# -------------------------------------------------------------------
# MCP JSON-RPC Endpoint
# -------------------------------------------------------------------
@app.post("/mcp")
async def mcp_rpc(request: Request):
    body = await request.json()

    method = body.get("method")
    rpc_id = body.get("id")
    params = body.get("params", {})

    # ---------------------------
    # tools/list
    # ---------------------------
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": {
                "tools": TOOLS
            }
        }

    # ---------------------------
    # tools/call (streaming)
    # ---------------------------
    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name != "calculator":
            return JSONResponse(
                status_code=400,
                content={
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
            )

        async def event_stream():
            try:
                # MCP stream: tool start
                yield {
                    "event": "message",
                    "data": json.dumps({
                        "type": "tool_start",
                        "tool": tool_name
                    })
                }

                await asyncio.sleep(0.2)

                result = calculate(
                    arguments["operation"],
                    arguments["a"],
                    arguments["b"]
                )

                # MCP stream: tool result
                yield {
                    "event": "message",
                    "data": json.dumps({
                        "type": "tool_result",
                        "content": [
                            {
                                "type": "text",
                                "text": str(result)
                            }
                        ]
                    })
                }

                # MCP stream: done
                yield {
                    "event": "done",
                    "data": ""
                }

            except Exception as e:
                yield {
                    "event": "error",
                    "data": json.dumps({
                        "code": -32000,
                        "message": str(e)
                    })
                }

        return EventSourceResponse(event_stream())

    # ---------------------------
    # Unknown method
    # ---------------------------
    return {
        "jsonrpc": "2.0",
        "id": rpc_id,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }

# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------
@app.get("/")
async def root():
    return {"status": "MCP Calculator running"}


if __name__ == "__main__":
    app.run(transport="streamable-http")
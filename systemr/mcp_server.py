"""
MCP stdio server for System R Risk Intelligence.

Proxies MCP tool calls to the agents.systemr.ai REST API
via the SystemRClient. Requires SYSTEMR_API_KEY env var.

Usage:
    SYSTEMR_API_KEY=sr_agent_... python -m systemr.mcp_server
"""

import asyncio
import json
import os
import sys


def main():
    try:
        from mcp.server import Server
        from mcp.types import Tool, TextContent
        from mcp.server.stdio import stdio_server
    except ImportError:
        print("MCP SDK not installed. Run: pip install 'mcp>=1.8.0'", file=sys.stderr)
        sys.exit(1)

    from systemr.client import SystemRClient, SystemRError

    api_key = os.environ.get("SYSTEMR_API_KEY", "")
    if not api_key:
        print("SYSTEMR_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    client = SystemRClient(api_key=api_key)
    server = Server("systemr-risk-intelligence")

    TOOLS = [
        Tool(
            name="calculate_position_size",
            description=(
                "Calculate optimal position size using the G-formula. "
                "Returns shares, risk amount, notional value. Cost: $0.003 USDC."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "equity": {"type": "string", "description": "Account equity in USD"},
                    "entry_price": {"type": "string", "description": "Entry price"},
                    "stop_price": {"type": "string", "description": "Stop loss price"},
                    "direction": {"type": "string", "enum": ["long", "short"]},
                    "risk_percent": {"type": "string", "description": "Risk as decimal (optional)"},
                },
                "required": ["equity", "entry_price", "stop_price", "direction"],
            },
        ),
        Tool(
            name="check_trade_risk",
            description=(
                "Validate a trade against Iron Fist risk rules. "
                "Returns approval status and risk score. Cost: $0.004 USDC."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Instrument symbol"},
                    "direction": {"type": "string", "enum": ["long", "short"]},
                    "entry_price": {"type": "string", "description": "Entry price"},
                    "stop_price": {"type": "string", "description": "Stop loss price"},
                    "quantity": {"type": "string", "description": "Number of shares"},
                    "equity": {"type": "string", "description": "Account equity in USD"},
                },
                "required": ["symbol", "direction", "entry_price", "stop_price", "quantity", "equity"],
            },
        ),
        Tool(
            name="evaluate_performance",
            description=(
                "Evaluate trading performance via G-metric analysis. "
                "Returns G score, expected R, verdict. Cost: $0.10-$1.00 USDC."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "r_multiples": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "R-multiples from trade history",
                    },
                    "tier": {
                        "type": "string",
                        "enum": ["basic", "full", "comprehensive"],
                        "description": "Evaluation tier (default: basic)",
                    },
                },
                "required": ["r_multiples"],
            },
        ),
        Tool(
            name="get_pricing",
            description="Get current pricing for all operations. Free.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]

    @server.list_tools()
    async def list_tools():
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        try:
            if name == "calculate_position_size":
                result = client.calculate_position_size(
                    equity=arguments["equity"],
                    entry_price=arguments["entry_price"],
                    stop_price=arguments["stop_price"],
                    direction=arguments["direction"],
                    risk_percent=arguments.get("risk_percent"),
                )
            elif name == "check_trade_risk":
                result = client.check_risk(
                    symbol=arguments["symbol"],
                    direction=arguments["direction"],
                    entry_price=arguments["entry_price"],
                    stop_price=arguments["stop_price"],
                    quantity=arguments["quantity"],
                    equity=arguments["equity"],
                )
            elif name == "evaluate_performance":
                tier = arguments.get("tier", "basic")
                r_multiples = arguments["r_multiples"]
                if tier == "basic":
                    result = client.basic_eval(r_multiples=r_multiples)
                elif tier == "full":
                    result = client.full_eval(r_multiples=r_multiples)
                else:
                    result = client.comprehensive_eval(r_multiples=r_multiples)
            elif name == "get_pricing":
                result = client.get_pricing()
            else:
                result = {"error": f"Unknown tool: {name}"}
        except SystemRError as e:
            result = {"error": str(e), "status_code": e.status_code}

        return [TextContent(
            type="text",
            text=json.dumps(result, default=str),
        )]

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()

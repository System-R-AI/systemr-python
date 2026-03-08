"""
System R Python SDK - Trading & Investment Operating System for AI agents.

47 tools: position sizing, risk validation, regime detection, Greeks analysis,
equity curves, signal scoring, trade planning, compliance checks, and more.

Usage:
    from systemr import SystemRClient

    client = SystemRClient(api_key="sr_agent_...")

    # Named method
    gate = client.pre_trade_gate(
        symbol="AAPL", direction="long",
        entry_price="185.50", stop_price="180.00",
        equity="100000",
    )

    # Generic tool call (any of 47 tools)
    curve = client.call_tool("calculate_equity_curve",
        r_multiples=["1.5", "-1.0", "2.0"],
        starting_equity="100000",
    )

    # Workflow chain
    diag = client.run_backtest_diagnostic(
        r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8"],
    )
"""

from systemr.client import (
    AuthenticationError,
    InsufficientBalanceError,
    SystemRClient,
    SystemRError,
)

__all__ = [
    "SystemRClient",
    "SystemRError",
    "AuthenticationError",
    "InsufficientBalanceError",
]

__version__ = "2.0.0"

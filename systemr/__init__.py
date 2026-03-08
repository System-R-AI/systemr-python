"""
System R Python SDK - AI-native risk intelligence for trading agents.

Usage:
    from systemr import SystemRClient

    client = SystemRClient(api_key="sr_agent_...")
    result = client.calculate_position_size(
        equity="100000",
        entry_price="150.00",
        stop_price="145.00",
        direction="long",
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

__version__ = "1.0.1"

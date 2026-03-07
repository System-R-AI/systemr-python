"""
Risk validation example — check if a trade passes Iron Fist rules.
"""

from systemr import SystemRClient

client = SystemRClient(api_key="sr_agent_YOUR_KEY_HERE")

result = client.check_risk(
    symbol="AAPL",
    direction="long",
    entry_price="185.50",
    stop_price="180.00",
    quantity="100",
    equity="100000",
)

if result["approved"]:
    print(f"Trade approved (score: {result['score']})")
else:
    print(f"Trade rejected: {result['errors']}")

client.close()

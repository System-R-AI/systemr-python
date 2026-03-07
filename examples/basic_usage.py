"""
Basic usage example for the System R Python SDK.

Before running:
    1. pip install systemr
    2. Register an agent at https://agents.systemr.ai/v1/agents/register
    3. Set your API key below
"""

from systemr import SystemRClient, InsufficientBalanceError

API_KEY = "sr_agent_YOUR_KEY_HERE"

client = SystemRClient(api_key=API_KEY)

# Check agent info
info = client.get_info()
print(f"Agent: {info['agent_name']} ({info['mode']})")

# Check balance
balance = client.get_balance()
print(f"Balance: ${balance['balance']} USDC")

# Position sizing
try:
    size = client.calculate_position_size(
        equity="100000",
        entry_price="185.50",
        stop_price="180.00",
        direction="long",
    )
    print(f"Buy {size['shares']} shares, risking ${size['risk_amount']}")
except InsufficientBalanceError:
    print("Deposit USDC to use paid endpoints")

client.close()

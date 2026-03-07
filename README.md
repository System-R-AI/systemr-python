# systemr

Python SDK for [agents.systemr.ai](https://agents.systemr.ai) — AI-native risk intelligence for trading agents.

[![PyPI](https://img.shields.io/pypi/v/systemr)](https://pypi.org/project/systemr/)
[![Python](https://img.shields.io/pypi/pyversions/systemr)](https://pypi.org/project/systemr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Install

```bash
pip install systemr
```

## Quick Start

```python
from systemr import SystemRClient

client = SystemRClient(api_key="sr_agent_...")

# Position sizing ($0.003)
result = client.calculate_position_size(
    equity="100000",
    entry_price="185.50",
    stop_price="180.00",
    direction="long",
)
print(result["shares"], result["risk_amount"])

# Risk validation ($0.004)
risk = client.check_risk(
    symbol="AAPL",
    direction="long",
    entry_price="185.50",
    stop_price="180.00",
    quantity="100",
    equity="100000",
)
print(risk["approved"], risk["score"])

# Strategy evaluation ($0.10 - $1.00)
eval_result = client.basic_eval(r_multiples=["1.5", "-1.0", "2.3", "-0.5", "1.8"])
print(eval_result["g_score"], eval_result["verdict"])
```

## Get an API Key

```python
import httpx

resp = httpx.post("https://agents.systemr.ai/v1/agents/register", json={
    "owner_id": "your-id",
    "agent_name": "my-trading-agent",
    "agent_type": "trading",
})
data = resp.json()
print(data["api_key"])  # sr_agent_... (save this, shown only once)
```

## API Reference

### Agent Management
| Method | Description |
|--------|-------------|
| `client.get_info()` | Get agent info |
| `client.list_agents()` | List owner's agents |
| `client.update_mode(mode)` | Change mode (sandbox/live/suspended/terminated) |

### Position Sizing
| Method | Cost |
|--------|------|
| `client.calculate_position_size(equity, entry_price, stop_price, direction)` | $0.003 |

### Risk Validation
| Method | Cost |
|--------|------|
| `client.check_risk(symbol, direction, entry_price, stop_price, quantity, equity)` | $0.004 |

### Evaluation
| Method | Cost | Description |
|--------|------|-------------|
| `client.basic_eval(r_multiples)` | $0.10 | G metric + verdict |
| `client.full_eval(r_multiples)` | $0.50 | G + rolling G + System R Score |
| `client.comprehensive_eval(r_multiples)` | $1.00 | Full analysis + impact |

### Billing
| Method | Description |
|--------|-------------|
| `client.get_pricing()` | Operation prices (no auth) |
| `client.get_balance()` | Current USDC balance |
| `client.deposit(amount)` | Record deposit |
| `client.get_transactions()` | Transaction history |
| `client.get_usage()` | Usage summary |

## Error Handling

```python
from systemr import SystemRClient, AuthenticationError, InsufficientBalanceError, SystemRError

client = SystemRClient(api_key="sr_agent_...")

try:
    result = client.calculate_position_size(...)
except AuthenticationError:
    print("Invalid API key or agent inactive")
except InsufficientBalanceError:
    print("Deposit USDC to continue")
except SystemRError as e:
    print(f"API error {e.status_code}: {e.detail}")
```

## Context Manager

```python
with SystemRClient(api_key="sr_agent_...") as client:
    result = client.check_risk(...)
# connection automatically closed
```

## MCP (Model Context Protocol)

System R is also available as an MCP server for AI assistants like Claude and ChatGPT. See the [MCP documentation](https://agents.systemr.ai/.well-known/agent.json) for configuration.

## License

MIT

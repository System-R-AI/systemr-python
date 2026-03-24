# systemr

Python SDK for [agents.systemr.ai](https://agents.systemr.ai), the trading and investment operating system for AI agents. Live and operational.

48 tools: position sizing, risk validation, regime detection, Greeks analysis, equity curves, signal scoring, trade planning, compliance checks, and more.

## Install

```bash
pip install systemr
```

## Quick Start

```python
from systemr import SystemRClient

client = SystemRClient(
    api_key="sr_agent_...",
    base_url="https://agents.systemr.ai",
)

# Pre-trade gate: sizing + risk + health in one call ($0.01)
gate = client.pre_trade_gate(
    symbol="AAPL",
    direction="long",
    entry_price="185.50",
    stop_price="180.00",
    equity="100000",
)
if gate["gate_passed"]:
    print(f"Buy {gate['sizing']['shares']} shares")
```

## Three Ways to Use Tools

### 1. Named Methods (common operations)

```python
# Position sizing ($0.003)
size = client.calculate_position_size(
    equity="100000", entry_price="185.50",
    stop_price="180.00", direction="long",
)

# Risk validation ($0.004)
risk = client.check_risk(
    symbol="AAPL", direction="long",
    entry_price="185.50", stop_price="180.00",
    quantity="100", equity="100000",
)

# Pre-trade gate ($0.01)
gate = client.pre_trade_gate(
    symbol="AAPL", direction="long",
    entry_price="185.50", stop_price="180.00",
    equity="100000", r_multiples=["1.5", "-1.0", "2.0"],
)

# System assessment ($2.00)
assessment = client.assess_system(
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8",
                 "0.8", "-0.3", "2.5", "-1.0", "1.2"],
)
print(assessment["verdict"])  # STRONG_SYSTEM, VIABLE_SYSTEM, etc.
```

### 2. Generic Tool Call (all 48 tools)

```python
# Equity curve from R-multiples ($0.004)
curve = client.call_tool("calculate_equity_curve",
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8"],
    starting_equity="100000",
)
print(curve["total_return"], curve["max_drawdown_pct"])

# Signal quality scoring ($0.003)
signal = client.call_tool("score_signal",
    conditions_met=4, total_conditions=5,
    regime_aligned=True, indicator_confluence=3,
    volume_confirmed=True, risk_reward_ratio="2.5",
)
print(signal["confidence"], signal["quality_score"])

# Margin calculation ($0.002)
margin = client.call_tool("calculate_margin",
    notional="50000", asset_class="STOCK",
    direction="LONG",
)
print(margin["margin_required"])

# Regime detection ($0.006)
regime = client.call_tool("detect_regime",
    prices=["180", "182", "179", "185", "188", "186"],
)

# Greeks analysis ($0.006)
greeks = client.call_tool("analyze_greeks",
    chain=[{
        "symbol": "AAPL240315C00185000",
        "underlying_symbol": "AAPL",
        "strike": "185", "expiration": "2024-03-15",
        "option_type": "CALL", "bid": "5.20", "ask": "5.50",
        "last": "5.35", "volume": 1000, "open_interest": 5000,
        "implied_volatility": "0.25",
    }],
    underlying_price="185.50",
)

# List all available tools
tools = client.list_tools()
print(f"{tools['tool_count']} tools available")
```

### 3. Workflow Chains (multi-tool sequences)

```python
# Full backtest diagnostic (6 tools, ~$0.032)
diag = client.run_backtest_diagnostic(
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8",
                 "0.8", "-0.3", "2.5", "-1.0", "1.2"],
    starting_equity="100000",
)
print(diag["system_r_score"]["grade"])       # A, B, C, D, F
print(diag["equity_curve"]["total_return"])   # total return
print(diag["monte_carlo"]["median_final_equity"])
print(diag["variance_killers"])              # what's hurting G

# Post-trade analysis (2 tools, $0.006)
post = client.run_post_trade_analysis(
    realized_pnl="500.00", realized_r="1.50",
    mfe="800.00", one_r_dollars="333.33",
    entry_price="180.00", exit_price="185.00",
    quantity=100, direction="LONG",
)
print(post["outcome"]["outcome"])            # WIN/LOSS/BREAKEVEN
print(post["outcome"]["efficiency_score"])   # how much R captured

# Market scan + signal scoring (2+ tools, $0.005+)
scan = client.run_market_scan(
    symbols=["AAPL", "MSFT", "GOOGL"],
    conditions=["rsi_oversold", "volume_spike"],
    market_data={
        "AAPL": {"indicators": {"rsi_14": "25", "relative_volume": "2.0"},
                 "current_price": "180.00", "regime": "RANGING", "atr": "3.50"},
        "MSFT": {"indicators": {"rsi_14": "55", "relative_volume": "0.8"},
                 "current_price": "400.00", "regime": "TRENDING_UP", "atr": "5.00"},
    },
)
for signal in scan["scored_signals"]:
    print(f"{signal['symbol']}: confidence={signal['signal_confidence']}")
```

## Wallet Linking and OSR Deposits

Agents can link a Solana wallet to their account and fund with OSR tokens for compute credits.

```python
import requests

headers = {"Authorization": "Bearer sr_agent_..."}
base = "https://agents.systemr.ai"

# Link your Solana wallet
resp = requests.post(f"{base}/v1/agents/link-wallet", headers=headers, json={
    "wallet_address": "YourSolanaWalletPublicKey...",
})
print(resp.json())  # {"status": "linked", "wallet_address": "..."}

# Deposit OSR tokens for compute credits
resp = requests.post(f"{base}/v1/billing/deposit-osr", headers=headers, json={
    "tx_signature": "your_solana_transaction_signature",
    "amount": "10000",
})
print(resp.json())  # {"credits_added": "...", "balance": "..."}
```

## OSR Presale Discount

Presale buyers who participated in the [OSR token presale](https://osrprotocol.com) receive a **permanent 20% discount** on all platform operations. The discount is verified on chain through your linked Solana wallet. No codes, no expiration. The wallet is the identity.

## All 48 Tools

| Category | Tools | Cost Range |
|----------|-------|------------|
| **Core** (4) | position_sizing, risk_check, evaluate_performance, get_pricing | $0.003 to $1.00 |
| **Analysis** (18) | drawdown, monte_carlo, kelly, variance_killers, win_loss, what_if, confidence, consistency, correlation, distribution, recovery, risk_adjusted, segmentation, execution_quality, peak_valley, rolling_g, system_r_score, equity_curve | $0.004 to $0.008 |
| **Intelligence** (11) | detect_regime, detect_patterns, structural_break, trend_structure, indicators, price_structure, correlations, liquidity, greeks, iv_surface, futures_curve, options_flow | $0.004 to $0.008 |
| **Planning** (4) | options_sizing, futures_sizing, options_plan, futures_plan | $0.004 to $0.008 |
| **Data** (3) | calculate_pnl, expected_value, compliance | $0.003 to $0.004 |
| **System** (5) | equity_curve, score_signal, trade_outcome, margin, scanner | $0.002 to $0.005 |
| **Journal** (1) | record_trade_outcome | $0.003 |
| **Compound** (2) | pre_trade_gate, assess_trading_system | $0.01 to $2.00 |

Use `client.list_tools()` for the full list with descriptions and input schemas.

## Workflow Cookbook

See [`examples/workflow_cookbook.py`](examples/workflow_cookbook.py) for 5 complete runnable workflows:

1. **Pre-Trade Gate**, call before every trade ($0.01)
2. **Backtest Diagnostic**, 6-tool chain for system analysis (~$0.032)
3. **Post-Trade Analysis**, execution quality review ($0.006)
4. **Market Scan**, watchlist screening + signal scoring ($0.005+)
5. **System Assessment**, comprehensive edge evaluation ($2.00)

Plus a **full agent loop** combining all workflows.

## Free Tier

$30 USDC credited on registration. Covers 10,000+ basic tool calls.

## Authentication

Register at [agents.systemr.ai](https://agents.systemr.ai) to get an API key (`sr_agent_...`).

All API requests go to `https://agents.systemr.ai`.

## Links

| | |
|---|---|
| Platform | [agents.systemr.ai](https://agents.systemr.ai) |
| OSR Token | [osrprotocol.com](https://osrprotocol.com) |
| System R AI | [systemr.ai](https://www.systemr.ai) |

## License

MIT

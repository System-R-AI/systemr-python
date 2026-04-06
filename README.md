<p align="center">
  <a href="https://systemr.ai">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/System-R-AI/.github/main/assets/systemr-logo-dark.svg" />
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/System-R-AI/.github/main/assets/systemr-logo-light.svg" />
      <img alt="System R AI" src="https://raw.githubusercontent.com/System-R-AI/.github/main/assets/systemr-logo-light.svg" width="260" />
    </picture>
  </a>
</p>

<h3 align="center">Python SDK for System R — the trading operating system</h3>

<p align="center">
  <a href="https://pypi.org/project/systemr/"><img src="https://img.shields.io/pypi/v/systemr?style=for-the-badge&color=3ECF8E&label=PyPI" alt="PyPI" /></a>
  <a href="https://pypi.org/project/systemr/"><img src="https://img.shields.io/pypi/pyversions/systemr?style=for-the-badge" alt="Python" /></a>
  <a href="https://github.com/System-R-AI/systemr-python/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="License" /></a>
</p>

<p align="center">
  <a href="https://docs.systemr.ai">Docs</a> ·
  <a href="https://docs.systemr.ai/getting-started/quickstart">Quickstart</a> ·
  <a href="https://agents.systemr.ai">API</a> ·
  <a href="https://github.com/System-R-AI/demo-trading-agent">Examples</a> ·
  <a href="https://docs.systemr.ai/mcp/overview">MCP</a>
</p>

---

55 tools. 25 brokers. Every asset class. One API call.

## Install

```bash
pip install systemr
```

Requires Python 3.9+. Only dependency: `httpx`.

## Your first trade gate

```python
from systemr import SystemRClient

client = SystemRClient(api_key="sr_agent_...")

gate = client.pre_trade_gate(
    symbol="AAPL",
    direction="long",
    entry_price="185.50",
    stop_price="180.00",
    equity="100000",
)

if gate["gate_passed"]:
    print(f"Buy {gate['sizing']['shares']} shares")
    print(f"Risk: ${gate['sizing']['risk_amount']}")
# → APPROVED: Buy 160 shares, risk $800 (1.6%), G-Score: 1.12
```

Five lines. Position sizing, risk validation, regime check, and system health — one call, $0.01.

## Same API. Every asset class.

```python
# Crypto
client.pre_trade_gate(symbol="BTC-USDT", direction="long",
    entry_price="67500", stop_price="65000", equity="100000")

# Forex
client.pre_trade_gate(symbol="EUR-USD", direction="short",
    entry_price="1.0850", stop_price="1.0900", equity="100000")

# Options
client.calculate_options_size(symbol="SPY", strike="530",
    expiry="2026-05-16", premium="8.50", equity="100000")

# Futures
client.calculate_futures_size(symbol="ES", direction="long",
    entry_price="5320", stop_price="5300", equity="100000")

# Prediction Markets
client.pre_trade_gate(symbol="TRUMP-WIN", direction="long",
    entry_price="0.52", stop_price="0.40", equity="100000")
```

## Why System R

- **Pre-trade risk gating** — every trade passes through position sizing (G-formula), risk validation (Iron Fist), and regime detection before execution
- **187 domain services** — not a wrapper around an LLM. A full trading operating system with 13,500+ verified tests
- **Model-agnostic** — Claude, GPT, DeepSeek, Llama. Bring your own key for $0 LLM cost
- **25 real broker adapters** — IBKR, Schwab, Binance, Coinbase, Kraken, dYdX, Hyperliquid, Polymarket, and 17 more

## What it does

> Without System R: 97 trades, 23% max drawdown, 41% win rate.
> With System R: 44 trades, **9% max drawdown**, 52% win rate.
> 53 trades gated during unfavorable regimes.
>
> — [demo-trading-agent](https://github.com/System-R-AI/demo-trading-agent)

## Chat

Talk to your agent in natural language. The LLM interprets your intent and calls the right tools.

```python
client = SystemRClient(api_key="sr_agent_...")

resp = client.chat("What's my current G-score? R-multiples: 1.5, -1.0, 2.0, -0.5, 1.8")
print(resp["text"])
print(f"Credits used: ${resp['credits_used']}")

# Continue the conversation
resp = client.chat("Run a Monte Carlo on those trades", session_id=resp.get("session_id"))
```

### BYOK (Bring Your Own Key)

Pass your Anthropic or OpenAI key to skip LLM charges. Tool calls still billed at standard rates.

```python
client = SystemRClient(
    api_key="sr_agent_...",
    external_api_key="sk-ant-..."  # your key — $0 LLM cost
)
```

---

## Tools

55 tools across 9 categories. Every tool callable via `client.call_tool("tool_name", **kwargs)`.

<details>
<summary><b>Core (4 tools)</b> — Position sizing, risk validation, performance evaluation</summary>

| Tool | Price | What it does |
|------|-------|-------------|
| `calculate_position_size` | $0.003 | G-formula sizing. Returns shares, risk amount, notional value. |
| `check_trade_risk` | $0.004 | Iron Fist validation. Position limits, daily loss, correlation. Score 0-100. |
| `evaluate_performance` | $0.10–$1.00 | G-score analysis. Basic / full / comprehensive tiers. |
| `get_pricing` | Free | Current prices for every operation. |

</details>

<details>
<summary><b>Analysis (18 tools)</b> — Monte Carlo, Kelly, drawdown, equity curves, segmentation</summary>

| Tool | Price | What it does |
|------|-------|-------------|
| `analyze_drawdown` | $0.004 | Max drawdown, duration, recovery metrics. |
| `run_monte_carlo` | $0.006 | 1,000 equity path projections with percentile bands. |
| `calculate_kelly` | $0.004 | Optimal bet fraction + half-Kelly recommendation. |
| `find_variance_killers` | $0.004 | Identifies trades dragging G-metric down. |
| `analyze_win_loss` | $0.004 | Win rate, avg win R, avg loss R, payoff ratio. |
| `run_what_if` | $0.004 | Scenario analysis on parameter changes. |
| `calculate_confidence` | $0.004 | Statistical confidence intervals for edge. |
| `analyze_consistency` | $0.004 | Rolling consistency over time. |
| `analyze_correlation` | $0.006 | Cross-trade correlation and serial dependency. |
| `analyze_distribution` | $0.004 | R-distribution: skew, kurtosis, normality. |
| `analyze_recovery` | $0.004 | Recovery time and recovery factor. |
| `calculate_risk_adjusted` | $0.004 | Sharpe, Sortino, Calmar ratios. |
| `analyze_segmentation` | $0.006 | Per-segment G by direction, asset, time. |
| `analyze_execution_quality` | $0.006 | Slippage, fill rate, MFE/MAE. |
| `analyze_peak_valley` | $0.004 | Peak-to-valley on equity curve. |
| `calculate_rolling_g` | $0.004 | Rolling G over sliding windows. |
| `calculate_system_r_score` | $0.004 | A/B/C/D/F system grade. |
| `calculate_equity_curve` | $0.004 | Equity curve from R-multiples. |

</details>

<details>
<summary><b>Intelligence (11 tools)</b> — Regime detection, patterns, Greeks, IV surface</summary>

| Tool | Price | What it does |
|------|-------|-------------|
| `detect_regime` | $0.006 | Trending, ranging, volatile, or quiet. |
| `detect_patterns` | $0.006 | Head-and-shoulders, double tops, triangles, flags. |
| `detect_structural_break` | $0.006 | Structural breaks in price series. |
| `analyze_trend_structure` | $0.006 | Higher highs/lows, trend strength, pullback quality. |
| `calculate_indicators` | $0.004 | RSI, MACD, Bollinger, ATR, and more. |
| `analyze_price_structure` | $0.006 | Support/resistance, pivots, channels. |
| `analyze_correlations` | $0.006 | Multi-asset correlation matrix. |
| `analyze_liquidity` | $0.006 | Bid-ask spreads, depth, volume profiles. |
| `analyze_greeks` | $0.006 | Delta, gamma, theta, vega for option chains. |
| `analyze_iv_surface` | $0.008 | IV surface: skew, term structure, vol smile. |
| `analyze_futures_curve` | $0.006 | Contango/backwardation, roll yield, basis. |

</details>

<details>
<summary><b>Planning (4 tools)</b> — Options and futures sizing, trade plan builders</summary>

| Tool | Price | What it does |
|------|-------|-------------|
| `calculate_options_size` | $0.004 | Contract count from premium risk + Greeks. |
| `calculate_futures_size` | $0.004 | Contract count from margin + tick value. |
| `build_options_plan` | $0.008 | Strategy selection, strike selection, risk/reward. |
| `build_futures_plan` | $0.008 | Entry, stop, target with margin requirements. |

</details>

<details>
<summary><b>Data (3), System (5), Compound (2), Journal (1), Memory & ML (7)</b></summary>

**Data (3 tools)**

| Tool | Price | What it does |
|------|-------|-------------|
| `calculate_pnl` | $0.003 | P&L from entry/exit/quantity. |
| `calculate_expected_value` | $0.003 | EV from win rate + avg win/loss. |
| `check_compliance` | $0.004 | Position limits, concentration, restricted lists. |

**System (5 tools)**

| Tool | Price | What it does |
|------|-------|-------------|
| `calculate_equity_curve` | $0.004 | Equity curve from R-multiples. |
| `score_signal` | $0.003 | Signal quality: confluence, regime, volume. 0-100. |
| `analyze_trade_outcome` | $0.003 | WIN/LOSS/BREAKEVEN, efficiency, edge captured. |
| `calculate_margin` | $0.002 | Margin requirements by asset class. |
| `evaluate_scanner` | $0.005 | Scanner evaluation against symbols + conditions. |

**Compound (2 tools)**

| Tool | Price | What it does |
|------|-------|-------------|
| `pre_trade_gate` | **$0.01** | The tool you call before every trade. Sizing + risk + health in one call. |
| `assess_trading_system` | **$2.00** | Quarterly review. G-metrics, Kelly, Monte Carlo, drawdown, what-if. Verdict: STRONG / VIABLE / MARGINAL / FAILING. |

**Journal (1 tool)**

| Tool | Price | What it does |
|------|-------|-------------|
| `record_trade_outcome` | $0.003 | Record completed trade. R-multiple, P&L, notes. |

**Memory & ML (7 tools)**

| Tool | Price | What it does |
|------|-------|-------------|
| `store_memory` | $0.002 | Persistent key-value storage across sessions. |
| `search_memory` | $0.002 | Search stored memories by key or query. |
| `get_trading_biases` | $0.004 | Detect disposition effect, recency bias, overtrading. |
| `get_behavioral_fingerprint` | $0.006 | Risk appetite, decision speed, adaptability. |
| `predict_trajectory` | $0.008 | ML-based performance projection. |
| `detect_anomalies` | $0.006 | Flag unusual sizes, frequency spikes, style drift. |
| `cluster_trades` | $0.006 | Unsupervised clustering by outcome, duration, asset. |

</details>

---

## Workflows

### 1. Pre-Trade Gate — call before every trade

```python
gate = client.pre_trade_gate(
    symbol="AAPL", direction="long",
    entry_price="185.50", stop_price="180.00",
    equity="100000",
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8", "0.8", "-0.3"],
)

if gate["gate_passed"]:
    print(f"APPROVED: Buy {gate['sizing']['shares']} shares, risk ${gate['sizing']['risk_amount']}")
    print(f"System G: {gate['system_health']['g']}")
```

**Cost: $0.01**

### 2. Backtest Diagnostic — 6-tool chain

```python
diag = client.run_backtest_diagnostic(
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8", "0.8", "-0.3",
                 "2.5", "-1.0", "1.2", "0.5", "-0.8", "1.1", "-0.2", "3.0"],
    starting_equity="100000",
)

print(f"Grade: {diag['system_r_score']['grade']}")         # A/B/C/D/F
print(f"Max drawdown: {diag['equity_curve']['max_drawdown_pct']}")
print(f"Monte Carlo median: ${diag['monte_carlo']['median_final_equity']}")
print(f"Variance killers: {len(diag['variance_killers'].get('killers', []))} trades")
```

**Cost: ~$0.032**

### 3. Full System Assessment — quarterly review

```python
assessment = client.assess_system(
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8", "0.8", "-0.3",
                 "2.5", "-1.0", "1.2", "0.5", "-0.8", "1.1", "-0.2", "3.0",
                 "-1.0", "0.7", "1.5", "-0.6", "2.1"],
    starting_equity="100000",
)

print(f"Verdict: {assessment['verdict']}")  # STRONG / VIABLE / MARGINAL / FAILING
print(f"G metric: {assessment['g_metrics']['g']}")
print(f"Kelly fraction: {assessment['kelly']['kelly_fraction']}")
```

**Cost: $2.00**

---

## Brokers

25 brokers and exchanges across every major market.

| Category | Brokers |
|----------|---------|
| **Traditional** | IBKR, Schwab, Alpaca, Tradier, Tastytrade, TradeStation, E*TRADE |
| **Forex** | OANDA |
| **Crypto** | Binance, Bybit, OKX, Coinbase, Kraken, Deribit, KuCoin, Gate.io, Gemini, Bitfinex, Aster |
| **DeFi** | Hyperliquid, dYdX, Drift |
| **Prediction** | Polymarket, Kalshi |

```python
# Connect a broker
client.connect_broker("binance", credentials={"api_key": "...", "api_secret": "..."})

# Check positions
positions = client.get_positions()

# Place an order
client.place_order(symbol="BTCUSDT", side="BUY", type="LIMIT", quantity="0.01", price="65000")
```

---

## MCP

System R is an MCP server. All 55 tools available in Claude Desktop, Cursor, or any MCP client.

**Remote (recommended):**

```json
{
  "mcpServers": {
    "systemr": {
      "transport": "sse",
      "url": "https://agents.systemr.ai/mcp/sse",
      "headers": { "X-API-Key": "sr_agent_..." }
    }
  }
}
```

**Local stdio:**

```bash
pip install systemr "mcp>=1.8.0"
SYSTEMR_API_KEY=sr_agent_... python -m systemr.mcp_server
```

```json
{
  "mcpServers": {
    "systemr": {
      "command": "python",
      "args": ["-m", "systemr.mcp_server"],
      "env": { "SYSTEMR_API_KEY": "sr_agent_..." }
    }
  }
}
```

---

## Billing

Usage-based. No subscriptions. New accounts get $5 free credit.

| Method | How |
|--------|-----|
| Stripe | Card payment via checkout |
| OSR | Burn for credits (20% presale discount) |
| SOL, USDC, USDT, PYUSD | Solana native tokens |

**LLM pricing:** Sonnet $9/$45 per 1M tokens (in/out). Opus $45/$225. BYOK: $0.

---

## API Reference

Full reference: [docs.systemr.ai](https://docs.systemr.ai)

| Area | Key Endpoints |
|------|--------------|
| **Agent** | `POST /agents/register` · `GET /agents/me` · `PUT /agents/mode` |
| **Tools** | `POST /tools/call` · `GET /tools/list` |
| **Broker** | `POST /broker/connect` · `GET /broker/positions` · `POST /broker/order` |
| **Billing** | `GET /billing/balance` · `GET /billing/usage` · `POST /billing/checkout` |
| **Support** | `POST /support/feedback` · `POST /support/ticket` |

---

## Links

| | |
|---|---|
| **Docs** | [docs.systemr.ai](https://docs.systemr.ai) |
| **Platform** | [app.systemr.ai](https://app.systemr.ai) |
| **Agents API** | [agents.systemr.ai](https://agents.systemr.ai) |
| **PyPI** | [pypi.org/project/systemr](https://pypi.org/project/systemr/) |
| **Examples** | [demo-trading-agent](https://github.com/System-R-AI/demo-trading-agent) |
| **X** | [@Systemrai](https://x.com/Systemrai) |

---

## License

MIT. See [LICENSE](LICENSE).

# systemr

Build AI trading agents with institutional-grade risk management.

[![PyPI](https://img.shields.io/pypi/v/systemr)](https://pypi.org/project/systemr/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://pypi.org/project/systemr/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/System-R-AI/systemr-python/blob/main/LICENSE)

## Install

```bash
pip install systemr
```

Requires Python 3.9 or higher. The only dependency is `httpx`.

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
    print(f"Buy {gate['sizing']['shares']} shares of AAPL")
    print(f"Risk: ${gate['sizing']['risk_amount']}")
```

Five lines of code. Position sizing, risk validation, and system health in a single call for $0.01.

## What you get

55 tools across 8 categories. 25 brokers and exchanges. Pay per call with OSR, SOL, USDC, USDT, or PYUSD.

| Category | Count | Highlights |
|---|---|---|
| [Core](#core-4-tools) | 4 | Position sizing, risk validation, performance evaluation |
| [Analysis](#analysis-18-tools) | 18 | Monte Carlo, Kelly criterion, drawdown, equity curves |
| [Intelligence](#intelligence-11-tools) | 11 | Regime detection, patterns, volatility surface, Greeks |
| [Planning](#planning-4-tools) | 4 | Options sizing, futures sizing, trade plan builders |
| [Data](#data-3-tools) | 3 | P&L calculation, expected value, compliance |
| [System](#system-5-tools) | 5 | Signal scoring, margin, scanner evaluation |
| [Compound](#compound-2-tools) | 2 | Pre-trade gate, full system assessment |
| [Journal](#journal-1-tool) | 1 | Trade journaling with R-multiples |
| [Memory and ML](#memory-and-ml-7-tools) | 7 | Persistent memory, behavioral analytics, ML prediction |

Connect to 25 brokers including IBKR, Schwab, Binance, Coinbase, Alpaca, Kraken, dYdX, Polymarket, and more.

---

## Tools

Every tool is callable via `client.call_tool("tool_name", **kwargs)`.

### Core (4 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `calculate_position_size` | $0.003 | G-formula position sizing. Returns shares, risk amount, notional value, and 1R dollar amount. |
| `check_trade_risk` | $0.004 | Iron Fist risk validation. Checks position limits, daily loss limits, correlation rules. Returns approval, score (0 to 100), errors, warnings. |
| `evaluate_performance` | $0.10 / $0.50 / $1.00 | G-score performance analysis in three tiers: basic (G metric + verdict), full (G + rolling G + System R Score), comprehensive (all metrics + impact analysis). |
| `get_pricing` | Free | Returns current prices for every operation on the platform. |

### Analysis (18 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `analyze_drawdown` | $0.004 | Drawdown profile analysis. Max drawdown, drawdown duration, recovery metrics. |
| `run_monte_carlo` | $0.006 | Monte Carlo simulation. 1,000 equity path projections with percentile bands. |
| `calculate_kelly` | $0.004 | Kelly criterion calculation. Optimal bet fraction, half-Kelly recommendation. |
| `find_variance_killers` | $0.004 | Identifies the specific trades dragging your G-metric down. |
| `analyze_win_loss` | $0.004 | Win/loss distribution. Win rate, average win R, average loss R, payoff ratio. |
| `run_what_if` | $0.004 | Scenario analysis. What happens to your G if you remove certain trades or change parameters. |
| `calculate_confidence` | $0.004 | Statistical confidence intervals for your edge estimate. |
| `analyze_consistency` | $0.004 | Rolling consistency metrics. Measures how stable your edge is over time. |
| `analyze_correlation` | $0.006 | Cross-trade correlation analysis. Detects clustering and serial dependency in outcomes. |
| `analyze_distribution` | $0.004 | R-multiple distribution analysis. Skew, kurtosis, normality tests. |
| `analyze_recovery` | $0.004 | Recovery analysis. Time to recover from drawdowns, recovery factor. |
| `calculate_risk_adjusted` | $0.004 | Risk-adjusted returns. Sharpe, Sortino, Calmar ratios from R-multiples. |
| `analyze_segmentation` | $0.006 | Segment performance by direction, asset, time of day, day of week. |
| `analyze_execution_quality` | $0.006 | Execution quality scoring. Slippage analysis, fill rate, MFE/MAE ratios. |
| `analyze_peak_valley` | $0.004 | Peak-to-valley analysis on the equity curve. |
| `calculate_rolling_g` | $0.004 | Rolling G-metric over sliding windows. Shows how your edge evolves. |
| `calculate_system_r_score` | $0.004 | System R Score: A/B/C/D/F grade based on composite G-metrics. |
| `calculate_equity_curve` | $0.004 | Equity curve from R-multiples. Total return, max drawdown, CAGR. |

### Intelligence (11 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `detect_regime` | $0.006 | Market regime detection. Identifies trending, ranging, volatile, or quiet regimes. |
| `detect_patterns` | $0.006 | Chart pattern recognition. Head-and-shoulders, double tops, triangles, flags. |
| `detect_structural_break` | $0.006 | Structural break detection in price series. Identifies regime transitions. |
| `analyze_trend_structure` | $0.006 | Trend structure analysis. Higher highs/lows, trend strength, pullback quality. |
| `calculate_indicators` | $0.004 | Technical indicator calculation. RSI, MACD, Bollinger, ATR, and more. |
| `analyze_price_structure` | $0.006 | Price structure analysis. Support/resistance levels, pivot points, price channels. |
| `analyze_correlations` | $0.006 | Multi-asset correlation matrix. Cross-asset relationships and divergences. |
| `analyze_liquidity` | $0.006 | Liquidity analysis. Bid-ask spreads, depth, volume profiles. |
| `analyze_greeks` | $0.006 | Options Greeks analysis. Delta, gamma, theta, vega for entire chains. |
| `analyze_iv_surface` | $0.008 | Implied volatility surface mapping. Skew, term structure, vol smile. |
| `analyze_futures_curve` | $0.006 | Futures curve analysis. Contango/backwardation, roll yield, basis. |

### Planning (4 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `calculate_options_size` | $0.004 | Options position sizing. Contract count based on premium risk and Greeks. |
| `calculate_futures_size` | $0.004 | Futures position sizing. Contract count based on margin and tick value. |
| `build_options_plan` | $0.008 | Options trade plan builder. Strategy selection, strike selection, risk/reward profile. |
| `build_futures_plan` | $0.008 | Futures trade plan builder. Entry, stop, target with margin requirements. |

### Data (3 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `calculate_pnl` | $0.003 | P&L calculation. Gross, net, fees, R-multiple from entry/exit/quantity. |
| `calculate_expected_value` | $0.003 | Expected value calculation from win rate and average win/loss. |
| `check_compliance` | $0.004 | Compliance check against configurable rule sets. Position limits, concentration, restricted lists. |

### System (5 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `calculate_equity_curve` | $0.004 | Build equity curve from R-multiples with a starting balance. |
| `score_signal` | $0.003 | Signal quality scoring. Confluence, regime alignment, volume confirmation. Returns confidence and quality score 0 to 100. |
| `analyze_trade_outcome` | $0.003 | Post-trade outcome classification. WIN/LOSS/BREAKEVEN, efficiency score, edge captured. |
| `calculate_margin` | $0.002 | Margin requirement calculation by asset class and direction. |
| `evaluate_scanner` | $0.005 | Evaluate a market scanner against multiple symbols and conditions. |

### Compound (2 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `pre_trade_gate` | $0.01 | The tool you call before every trade. Combines position sizing, risk validation, and system health into a single gate. Returns `gate_passed` (bool) so your agent can make a go/no-go decision in one call. |
| `assess_trading_system` | $2.00 | Comprehensive trading system assessment. Runs G-metrics, win/loss, Kelly criterion, Monte Carlo, drawdown analysis, and what-if scenarios. Returns a verdict: STRONG_SYSTEM, VIABLE_SYSTEM, MARGINAL_SYSTEM, or FAILING_SYSTEM. |

### Journal (1 tool)

| Tool | Price | Description |
|------|-------|-------------|
| `record_trade_outcome` | $0.003 | Record a completed trade to your agent's journal. Symbol, direction, entry, exit, stop, quantity, R-multiple, P&L, notes. Journal queries (trades, stats, R-multiples) are free REST endpoints. |

### Memory and ML (7 tools)

| Tool | Price | Description |
|------|-------|-------------|
| `store_memory` | $0.002 | Store a key-value memory entry for your agent. Persistent across sessions. |
| `search_memory` | $0.002 | Search stored memories by key or semantic query. |
| `get_trading_biases` | $0.004 | Detect behavioral biases from trade history: disposition effect, recency bias, overtrading, loss aversion. |
| `get_behavioral_fingerprint` | $0.006 | Generate a behavioral fingerprint for the agent. Risk appetite, decision speed, adaptability profile. |
| `predict_trajectory` | $0.008 | ML-based trajectory prediction. Projects future performance based on historical patterns. |
| `detect_anomalies` | $0.006 | Anomaly detection in trading behavior. Flags unusual position sizes, frequency spikes, style drift. |
| `cluster_trades` | $0.006 | Unsupervised clustering of trades by outcome, duration, asset, and strategy characteristics. |

---

## Brokers and Exchanges

25 brokers and exchanges across every major market.

### Traditional Brokers

| Broker | Markets | API |
|--------|---------|-----|
| Interactive Brokers (IBKR) | Stocks, Options, Futures, Forex | TWS / Client Portal |
| Charles Schwab | Stocks, Options, ETFs | Schwab API |
| Alpaca | Stocks, Crypto | Alpaca v2 |
| Tradier | Stocks, Options | Tradier REST |
| Tastytrade | Stocks, Options, Futures | Tastytrade API |
| TradeStation | Stocks, Options, Futures | TradeStation v3 |
| E*TRADE | Stocks, Options, ETFs | E*TRADE v1 |

### Forex

| Broker | Markets | API |
|--------|---------|-----|
| OANDA | Forex, CFDs | OANDA v20 |

### Crypto Exchanges

| Exchange | Markets | API |
|----------|---------|-----|
| Binance | Spot, Futures, Options | Binance REST/WS |
| Bybit | Spot, Perps, Options | Bybit v5 |
| OKX | Spot, Perps, Options, Futures | OKX v5 |
| Coinbase | Spot | Coinbase Advanced |
| Kraken | Spot, Futures | Kraken REST |
| Deribit | Options, Futures | Deribit v2 |
| KuCoin | Spot, Futures | KuCoin v2 |
| Gate.io | Spot, Futures | Gate.io v4 |
| Gemini | Spot | Gemini v1 |
| Bitfinex | Spot, Margin | Bitfinex v2 |
| Aster | Spot | Aster REST |

### DeFi Protocols

| Protocol | Markets | Chain |
|----------|---------|-------|
| Hyperliquid | Perps | Hyperliquid L1 |
| dYdX | Perps | dYdX Chain |
| Drift | Perps, Spot | Solana |

### Prediction Markets

| Platform | Markets | Type |
|----------|---------|------|
| Polymarket | Binary outcomes | Polygon |
| Kalshi | Binary outcomes, Events | Regulated exchange |

---

## Broker Connection Example

```python
import requests

headers = {"Authorization": "Bearer sr_agent_..."}
base = "https://agents.systemr.ai"

# Connect to Binance
resp = requests.post(f"{base}/v1/broker/connect", headers=headers, json={
    "broker": "binance",
    "credentials": {
        "api_key": "your_binance_api_key",
        "api_secret": "your_binance_api_secret",
    },
})
print(resp.json())  # {"status": "connected", "broker": "binance"}

# Check positions
resp = requests.get(f"{base}/v1/broker/positions", headers=headers)
positions = resp.json()
for pos in positions["positions"]:
    print(f"{pos['symbol']}: {pos['quantity']} @ {pos['avg_price']}")

# Place an order
resp = requests.post(f"{base}/v1/broker/order", headers=headers, json={
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "quantity": "0.01",
    "price": "65000.00",
})
print(resp.json())  # {"order_id": "...", "status": "NEW"}
```

---

## Workflows

### 1. Pre-Trade Gate (call before every trade)

One call, three checks: position sizing, risk validation, and system health.

```python
from systemr import SystemRClient

client = SystemRClient(api_key="sr_agent_...")

gate = client.pre_trade_gate(
    symbol="AAPL",
    direction="long",
    entry_price="185.50",
    stop_price="180.00",
    equity="100000",
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8", "0.8", "-0.3"],
)

if gate["gate_passed"]:
    shares = gate["sizing"]["shares"]
    risk = gate["sizing"]["risk_amount"]
    print(f"APPROVED: Buy {shares} shares, risking ${risk}")
    if gate.get("system_health"):
        print(f"System G: {gate['system_health']['g']}")
```

**Cost: $0.01**

### 2. Backtest Diagnostic (6-tool chain)

Feed your backtest R-multiples and get a complete system analysis: equity curve, grade, drawdown, Monte Carlo projection, variance killers, and win/loss distribution.

```python
diag = client.run_backtest_diagnostic(
    r_multiples=[
        "1.5", "-1.0", "2.0", "-0.5", "1.8",
        "0.8", "-0.3", "2.5", "-1.0", "1.2",
        "0.5", "-0.8", "1.1", "-0.2", "3.0",
    ],
    starting_equity="100000",
)

print(f"Grade: {diag['system_r_score']['grade']}")
print(f"Total return: {diag['equity_curve']['total_return']}")
print(f"Max drawdown: {diag['equity_curve']['max_drawdown_pct']}")
print(f"Monte Carlo median: ${diag['monte_carlo']['median_final_equity']}")
print(f"Variance killers: {len(diag['variance_killers'].get('killers', []))} trades")
print(f"Win rate: {diag['win_loss']['win_rate']}")
```

**Cost: ~$0.032**

### 3. Full System Assessment

Quarterly system review. Runs G-metrics, win/loss analysis, Kelly criterion, Monte Carlo, drawdown, and what-if scenarios in a single compound call.

```python
assessment = client.assess_system(
    r_multiples=[
        "1.5", "-1.0", "2.0", "-0.5", "1.8",
        "0.8", "-0.3", "2.5", "-1.0", "1.2",
        "0.5", "-0.8", "1.1", "-0.2", "3.0",
        "-1.0", "0.7", "1.5", "-0.6", "2.1",
    ],
    starting_equity="100000",
)

print(f"Verdict: {assessment['verdict']}")
# STRONG_SYSTEM, VIABLE_SYSTEM, MARGINAL_SYSTEM, or FAILING_SYSTEM

print(f"G metric: {assessment['g_metrics']['g']}")
print(f"Kelly fraction: {assessment['kelly']['kelly_fraction']}")
print(f"Half-Kelly: {assessment['kelly']['half_kelly']}")
print(f"Monte Carlo median: ${assessment['monte_carlo']['median_final_equity']}")
print(f"Max drawdown: {assessment['drawdown']['max_drawdown_pct']}")
```

**Cost: $2.00**

### 4. Market Intelligence Scan

Scan a watchlist for technical conditions, then score each matching signal for quality and confidence.

```python
scan = client.run_market_scan(
    symbols=["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"],
    conditions=["rsi_oversold", "volume_spike"],
    market_data={
        "AAPL": {
            "indicators": {"rsi_14": "28", "relative_volume": "2.1"},
            "current_price": "180.00", "regime": "RANGING", "atr": "3.50",
        },
        "MSFT": {
            "indicators": {"rsi_14": "55", "relative_volume": "0.8"},
            "current_price": "400.00", "regime": "TRENDING_UP", "atr": "5.00",
        },
        "GOOGL": {
            "indicators": {"rsi_14": "22", "relative_volume": "1.8"},
            "current_price": "155.00", "regime": "TRENDING_DOWN", "atr": "4.20",
        },
    },
)

for signal in scan["scored_signals"]:
    print(f"{signal['symbol']}: quality={signal['quality_score']}/100, "
          f"confidence={signal['signal_confidence']}")
```

**Cost: $0.005 + $0.003 per matching signal**

### 5. Memory-Assisted Trading

Agents can persist memories across sessions and use behavioral analytics to improve over time.

```python
# Store a trading insight
client.call_tool("store_memory",
    key="aapl_earnings_pattern",
    value="AAPL tends to gap down after earnings then recover within 3 days. "
          "Best entry is day 2 close if RSI < 35.",
)

# Later: recall it before an AAPL earnings trade
memories = client.call_tool("search_memory", query="aapl earnings")
print(memories)

# Check your behavioral biases
biases = client.call_tool("get_trading_biases",
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "0.3", "-2.0", "0.8"],
    trade_durations=["120", "30", "240", "15", "60", "180", "90"],
)
print(f"Detected biases: {biases['biases']}")

# Get your behavioral fingerprint
fingerprint = client.call_tool("get_behavioral_fingerprint",
    r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8"],
    trade_durations=["120", "30", "240", "15", "60"],
    position_sizes=["100", "50", "200", "75", "150"],
)
print(f"Risk appetite: {fingerprint['risk_appetite']}")
print(f"Adaptability: {fingerprint['adaptability']}")
```

**Cost: $0.002 to $0.006 per call**

---

## Payments

### Depositing compute credits

Every tool call deducts from your agent's balance. Deposit before you call. Pay per call.

Supported currencies:

| Currency | Endpoint | Notes |
|----------|----------|-------|
| OSR | `POST /v1/billing/deposit-osr` | System R's native token. Presale buyers receive a permanent 20% discount. |
| SOL | `POST /v1/billing/deposit-sol` | Solana native token. |
| USDC | `POST /v1/billing/deposit-usdc` | Circle USDC on Solana. |
| USDT | `POST /v1/billing/deposit-usdt` | Tether USDT on Solana. |
| PYUSD | `POST /v1/billing/deposit-pyusd` | PayPal USD on Solana. |

Each deposit endpoint requires a `tx_signature` (the Solana transaction signature) and `amount`.

### Wallet linking

```python
import requests

headers = {"Authorization": "Bearer sr_agent_..."}
base = "https://agents.systemr.ai"

# Link your Solana wallet
requests.post(f"{base}/v1/agents/link-wallet", headers=headers, json={
    "wallet_address": "YourSolanaPublicKey...",
})

# Deposit OSR tokens
requests.post(f"{base}/v1/billing/deposit-osr", headers=headers, json={
    "tx_signature": "your_solana_tx_signature",
    "amount": "10000",
})

# Check balance
resp = requests.get(f"{base}/v1/billing/balance", headers=headers)
print(resp.json())  # {"balance": "...", "currency": "USDC"}
```

### OSR presale discount

Agents whose linked wallet participated in the [OSR token presale](https://osrprotocol.com) receive a **permanent 20% discount** on every tool call. The discount is verified on-chain through the linked Solana wallet. The wallet is the identity.

---

## API Reference

All endpoints are prefixed with `https://agents.systemr.ai/v1`.

### Agent Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agents/register` | Register a new agent. Returns API key. |
| GET | `/agents/me` | Get current agent info. |
| GET | `/agents/list` | List all agents under your ownership. |
| PUT | `/agents/mode` | Change agent mode (sandbox, live, suspended, terminated). |
| POST | `/agents/link-wallet` | Link a Solana wallet to the agent. |

### Billing

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/billing/balance` | Current balance in USDC. |
| POST | `/billing/deposit` | Generic deposit. |
| POST | `/billing/deposit-osr` | Deposit OSR tokens for compute credits. |
| POST | `/billing/deposit-sol` | Deposit SOL for compute credits. |
| POST | `/billing/deposit-usdc` | Deposit USDC for compute credits. |
| POST | `/billing/deposit-usdt` | Deposit USDT for compute credits. |
| POST | `/billing/deposit-pyusd` | Deposit PYUSD for compute credits. |
| GET | `/billing/transactions` | Transaction history. |
| GET | `/billing/usage` | Usage summary grouped by operation. |
| GET | `/billing/pricing` | Current operation pricing. |

### Broker

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/broker/supported` | List supported brokers and exchanges. |
| POST | `/broker/connect` | Connect broker credentials. |
| POST | `/broker/disconnect` | Disconnect a broker. |
| GET | `/broker/account` | Broker account info and balances. |
| GET | `/broker/positions` | Current open positions. |
| POST | `/broker/order` | Submit an order. |
| POST | `/broker/cancel` | Cancel an open order. |
| GET | `/broker/orders` | List open and recent orders. |

### Tools

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tools/call` | Call any tool by name with arguments. |
| GET | `/tools/list` | List all available tools with schemas and pricing. |

### Support

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/support/feedback` | Submit general feedback. |
| POST | `/support/ticket` | Open a support ticket. |
| POST | `/support/suggestion` | Submit a feature suggestion. |
| POST | `/support/enterprise` | Enterprise inquiry. |
| POST | `/support/bug` | Report a bug. |
| GET | `/support/tickets` | List your support tickets. |
| GET | `/support/ticket/{id}` | Get a specific ticket. |

### Guardian

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/guardian/status` | Guardian system status for your agent. |
| GET | `/guardian/report` | Full Guardian risk report. |

### Trust

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/trust/trust-score` | Your agent's trust score. |
| GET | `/trust/tier-policies` | Trust tier requirements and policies. |
| GET | `/trust/access-policy` | Current access policy for your agent's trust tier. |

### Leaderboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/leaderboard` | Agent performance leaderboard. |

### Graduation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/graduation/check` | Check if your agent qualifies for tier promotion. |
| POST | `/graduation/apply` | Apply for tier promotion. |

### Audit

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/audit/trail` | Audit trail for your agent's actions. |
| GET | `/audit/compliance-check` | Run a compliance check. |

### Onboarding

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/onboarding/verify` | Verify agent registration. |
| GET | `/onboarding/quickstart` | Quickstart guide and next steps. |

---

## MCP

System R is available as an MCP (Model Context Protocol) server for direct integration with LLM clients like Cursor, Windsurf, and other MCP-compatible tools.

### Remote server (recommended)

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "systemr": {
      "transport": "sse",
      "url": "https://agents.systemr.ai/mcp/sse",
      "headers": {
        "X-API-Key": "sr_agent_..."
      }
    }
  }
}
```

### Local stdio server

Run a local proxy:

```bash
pip install systemr "mcp>=1.8.0"
SYSTEMR_API_KEY=sr_agent_... python -m systemr.mcp_server
```

Configuration for local stdio mode:

```json
{
  "mcpServers": {
    "systemr": {
      "command": "python",
      "args": ["-m", "systemr.mcp_server"],
      "env": {
        "SYSTEMR_API_KEY": "sr_agent_..."
      }
    }
  }
}
```

### Streamable HTTP

For clients that support the streamable HTTP transport:

```json
{
  "mcpServers": {
    "systemr": {
      "transport": "streamable-http",
      "url": "https://agents.systemr.ai/mcp/sse",
      "headers": {
        "X-API-Key": "sr_agent_..."
      }
    }
  }
}
```

All 55 tools are available through MCP with full input schemas, descriptions, and pricing metadata.

---

## Links

| | |
|---|---|
| **Agent Platform** | [agents.systemr.ai](https://agents.systemr.ai) |
| **OSR Protocol** | [osrprotocol.com](https://osrprotocol.com) |
| **System R AI** | [systemr.ai](https://www.systemr.ai) |
| **PyPI** | [pypi.org/project/systemr](https://pypi.org/project/systemr/) |
| **GitHub** | [github.com/System-R-AI/systemr-python](https://github.com/System-R-AI/systemr-python) |
| **X** | [@OsrProtocol](https://x.com/OsrProtocol) |

---

## License

MIT License. Copyright (c) 2026 System R AI. See [LICENSE](LICENSE) for details.

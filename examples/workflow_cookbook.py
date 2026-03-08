"""
System R Workflow Cookbook — 5 Complete Workflows

Runnable examples showing how the 47 tools chain together.
Each workflow is self-contained: copy-paste into your agent.

Usage:
    pip install systemr
    export SYSTEMR_API_KEY=sr_agent_...
    python workflow_cookbook.py

Cost breakdown per workflow:
    1. Pre-Trade Gate:       $0.01
    2. Backtest Diagnostic:  ~$0.032
    3. Post-Trade Analysis:  $0.006
    4. Market Scan:          $0.005 + $0.003/match
    5. System Assessment:    $2.00
"""

import os
from systemr import SystemRClient

API_KEY = os.environ.get("SYSTEMR_API_KEY", "sr_agent_demo")
client = SystemRClient(api_key=API_KEY)


# ============================================================================
# WORKFLOW 1: Pre-Trade Gate
# Use before EVERY trade. One call, three checks: sizing + risk + system health.
# Cost: $0.01
# ============================================================================

def workflow_pre_trade_gate():
    """
    The most important workflow. Call this before every trade entry.

    Input: symbol, direction, prices, equity
    Output: gate_passed (bool), position size, risk score, system health
    """
    print("\n=== WORKFLOW 1: Pre-Trade Gate ($0.01) ===\n")

    gate = client.pre_trade_gate(
        symbol="AAPL",
        direction="long",
        entry_price="185.50",
        stop_price="180.00",
        equity="100000",
        # Optional: feed R-multiples for system health check
        r_multiples=["1.5", "-1.0", "2.0", "-0.5", "1.8", "0.8", "-0.3"],
    )

    # Decision: trade or skip
    if gate["gate_passed"]:
        shares = gate["sizing"]["shares"]
        risk = gate["sizing"]["risk_amount"]
        print(f"  APPROVED: Buy {shares} shares of AAPL")
        print(f"  Risk: ${risk} ({gate['sizing']['risk_percent']})")
        print(f"  Risk score: {gate['risk']['score']}/100")
    else:
        print(f"  BLOCKED: {gate['risk']['errors']}")

    # System health (only present when r_multiples provided)
    if gate.get("system_health"):
        g = gate["system_health"]["g"]
        verdict = gate["system_health"]["verdict"]
        print(f"  System health: G={g} — {verdict}")

    return gate


# ============================================================================
# WORKFLOW 2: Backtest Diagnostic
# After a backtest, run this to understand your system's edge.
# Chains: equity_curve → system_r_score → drawdown → monte_carlo
#         → variance_killers → win_loss
# Cost: ~$0.032
# ============================================================================

def workflow_backtest_diagnostic():
    """
    Feed your backtest R-multiples. Get a complete system diagnostic.

    Input: R-multiples from backtest history
    Output: equity curve, grade, drawdown profile, Monte Carlo projection,
            variance killers, win/loss distribution
    """
    print("\n=== WORKFLOW 2: Backtest Diagnostic (~$0.032) ===\n")

    r_multiples = [
        "1.5", "-1.0", "2.0", "-0.5", "1.8",
        "0.8", "-0.3", "2.5", "-1.0", "1.2",
        "0.5", "-0.8", "1.1", "-0.2", "3.0",
        "-1.0", "0.7", "1.5", "-0.6", "2.1",
    ]

    diag = client.run_backtest_diagnostic(
        r_multiples=r_multiples,
        starting_equity="100000",
    )

    # System grade (A/B/C/D/F)
    grade = diag["system_r_score"]["grade"]
    score = diag["system_r_score"]["system_r_score"]
    print(f"  System R Grade: {grade} (score: {score})")

    # Equity curve
    total_return = diag["equity_curve"]["total_return"]
    max_dd = diag["equity_curve"]["max_drawdown_pct"]
    print(f"  Total return: {total_return}")
    print(f"  Max drawdown: {max_dd}")

    # Monte Carlo projection
    mc = diag["monte_carlo"]
    print(f"  Monte Carlo median: ${mc['median_final_equity']}")
    print(f"  Monte Carlo 5th pct: ${mc['percentile_5']}")

    # Variance killers (what's hurting your G metric)
    killers = diag["variance_killers"]
    if killers.get("killers"):
        print(f"  Variance killers: {len(killers['killers'])} trades dragging G down")
        for k in killers["killers"][:3]:
            print(f"    Trade #{k['index']}: R={k['r_multiple']}")
    else:
        print("  No variance killers found")

    # Win/loss distribution
    wl = diag["win_loss"]
    print(f"  Win rate: {wl['win_rate']}")
    print(f"  Avg win: {wl['average_win_r']}R  |  Avg loss: {wl['average_loss_r']}R")

    return diag


# ============================================================================
# WORKFLOW 3: Post-Trade Analysis
# After closing a trade, analyze how well you executed.
# Chains: calculate_pnl → analyze_trade_outcome
# Cost: $0.006
# ============================================================================

def workflow_post_trade_analysis():
    """
    After a trade closes, analyze execution quality.

    Input: entry/exit/stop prices, realized P&L, R-multiple, MFE
    Output: P&L breakdown, outcome classification, efficiency score
    """
    print("\n=== WORKFLOW 3: Post-Trade Analysis ($0.006) ===\n")

    post = client.run_post_trade_analysis(
        # Trade details
        entry_price="180.00",
        exit_price="186.50",
        quantity=100,
        direction="LONG",
        stop_price="175.00",
        # R-multiple tracking
        realized_pnl="650.00",
        realized_r="1.30",
        mfe="800.00",          # Maximum favorable excursion
        one_r_dollars="500.00", # Dollar value of 1R (risk per share * shares)
        expected_value_r="1.5", # What you expected
    )

    # P&L breakdown
    pnl = post["pnl"]
    print(f"  Gross P&L: ${pnl['gross_pnl']}")
    print(f"  Net P&L: ${pnl['net_pnl']}")

    # Outcome classification
    outcome = post["outcome"]
    print(f"  Outcome: {outcome['outcome']}")           # WIN / LOSS / BREAKEVEN
    print(f"  Efficiency: {outcome['efficiency_score']}") # How much R you captured
    print(f"  Edge captured: {outcome['edge_captured']}")
    if outcome.get("expectation_accuracy"):
        print(f"  Expectation accuracy: {outcome['expectation_accuracy']}")

    return post


# ============================================================================
# WORKFLOW 4: Market Scan + Signal Scoring
# Scan multiple symbols for technical conditions, then score each match.
# Chains: evaluate_scanner → score_signal (per match)
# Cost: $0.005 + $0.003 per match
# ============================================================================

def workflow_market_scan():
    """
    Scan your watchlist for setups, then score each signal's quality.

    Input: symbols, conditions, market data
    Output: matching symbols with confidence and quality scores
    """
    print("\n=== WORKFLOW 4: Market Scan ($0.005 + $0.003/match) ===\n")

    scan = client.run_market_scan(
        symbols=["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"],
        conditions=["rsi_oversold", "volume_spike"],
        market_data={
            "AAPL": {
                "indicators": {"rsi_14": "28", "relative_volume": "2.1"},
                "current_price": "180.00",
                "regime": "RANGING",
                "atr": "3.50",
            },
            "MSFT": {
                "indicators": {"rsi_14": "55", "relative_volume": "0.8"},
                "current_price": "400.00",
                "regime": "TRENDING_UP",
                "atr": "5.00",
            },
            "GOOGL": {
                "indicators": {"rsi_14": "22", "relative_volume": "1.8"},
                "current_price": "155.00",
                "regime": "TRENDING_DOWN",
                "atr": "4.20",
            },
            "NVDA": {
                "indicators": {"rsi_14": "65", "relative_volume": "1.1"},
                "current_price": "875.00",
                "regime": "TRENDING_UP",
                "atr": "15.00",
            },
            "TSLA": {
                "indicators": {"rsi_14": "30", "relative_volume": "2.5"},
                "current_price": "245.00",
                "regime": "RANGING",
                "atr": "8.00",
            },
        },
    )

    # Scan results
    matches = scan["scored_signals"]
    print(f"  Scanned 5 symbols, {len(matches)} matches found:\n")

    for sig in matches:
        print(f"  {sig['symbol']}:")
        print(f"    Direction: {sig['direction']}")
        print(f"    Signal confidence: {sig['signal_confidence']}")
        print(f"    Quality score: {sig['quality_score']}/100")
        print(f"    Entry: ${sig['suggested_entry']}  |  Stop: ${sig['suggested_stop']}")
        print()

    return scan


# ============================================================================
# WORKFLOW 5: Full System Assessment
# Comprehensive evaluation of your entire trading system.
# Compound endpoint: G-metrics, win/loss, Kelly, Monte Carlo, drawdown, what-if.
# Cost: $2.00
# ============================================================================

def workflow_system_assessment():
    """
    Quarterly system review. Are you still edge-positive?

    Input: full R-multiple history (minimum 10 trades, ideally 50+)
    Output: verdict, G-metrics, Kelly fraction, Monte Carlo, drawdown, scenarios
    """
    print("\n=== WORKFLOW 5: System Assessment ($2.00) ===\n")

    # Your full trade history in R-multiples
    r_multiples = [
        "1.5", "-1.0", "2.0", "-0.5", "1.8",
        "0.8", "-0.3", "2.5", "-1.0", "1.2",
        "0.5", "-0.8", "1.1", "-0.2", "3.0",
        "-1.0", "0.7", "1.5", "-0.6", "2.1",
        "1.0", "-0.4", "0.9", "1.7", "-0.3",
    ]

    assessment = client.assess_system(
        r_multiples=r_multiples,
        starting_equity="100000",
    )

    # Top-level verdict
    verdict = assessment["verdict"]
    print(f"  Verdict: {verdict}")
    # STRONG_SYSTEM, VIABLE_SYSTEM, MARGINAL_SYSTEM, FAILING_SYSTEM

    # G-metrics (the core edge metric)
    g = assessment["g_metrics"]
    print(f"  G metric: {g['g']}")
    print(f"  Expected R: {g['expected_r']}")
    print(f"  Trade count: {g['trade_count']}")

    # Kelly criterion (optimal bet size)
    kelly = assessment["kelly"]
    print(f"  Kelly fraction: {kelly['kelly_fraction']}")
    print(f"  Half-Kelly: {kelly['half_kelly']}")

    # Monte Carlo (forward projection)
    mc = assessment["monte_carlo"]
    print(f"  Monte Carlo median equity: ${mc['median_final_equity']}")

    # Drawdown risk
    dd = assessment["drawdown"]
    print(f"  Max drawdown: {dd['max_drawdown_pct']}")
    print(f"  Recovery trades: {dd['recovery_trades']}")

    return assessment


# ============================================================================
# BONUS: Combining Workflows
# The real power: chain workflows for complete agent loops.
# ============================================================================

def full_agent_loop():
    """
    Complete agent decision loop using all workflows.

    1. Scan market for opportunities
    2. Gate each candidate trade
    3. After trade closes, analyze outcome
    4. Periodically assess entire system
    """
    print("\n=== FULL AGENT LOOP ===\n")

    # Step 1: Find opportunities
    scan = client.run_market_scan(
        symbols=["AAPL", "MSFT"],
        conditions=["rsi_oversold"],
        market_data={
            "AAPL": {
                "indicators": {"rsi_14": "25"},
                "current_price": "180.00",
                "regime": "RANGING",
                "atr": "3.50",
            },
            "MSFT": {
                "indicators": {"rsi_14": "55"},
                "current_price": "400.00",
                "regime": "TRENDING_UP",
                "atr": "5.00",
            },
        },
    )

    # Step 2: Gate each match
    for sig in scan["scored_signals"]:
        gate = client.pre_trade_gate(
            symbol=sig["symbol"],
            direction=sig["direction"],
            entry_price=sig["suggested_entry"],
            stop_price=sig["suggested_stop"],
            equity="100000",
        )

        if gate["gate_passed"]:
            shares = gate["sizing"]["shares"]
            print(f"  TRADE: {sig['symbol']} — {shares} shares")
            # ... execute on your broker ...
        else:
            print(f"  SKIP: {sig['symbol']} — {gate['risk']['errors']}")

    # Step 3: After closing trades, analyze execution
    # (This would use real trade data from your broker)
    print("  [Post-trade analysis would run after position closes]")

    # Step 4: Monthly system check
    # (Run with your full R-multiple history)
    print("  [System assessment would run on schedule]")


# ============================================================================
# Run all workflows
# ============================================================================

if __name__ == "__main__":
    print("System R Workflow Cookbook")
    print("=" * 60)

    workflow_pre_trade_gate()
    workflow_backtest_diagnostic()
    workflow_post_trade_analysis()
    workflow_market_scan()
    workflow_system_assessment()
    full_agent_loop()

    client.close()
    print("\nDone. Total cost for all examples: ~$2.06 USDC")

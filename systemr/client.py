"""
System R Python SDK client.

A simple, ergonomic client for agents to call System R services.
48 tools accessible via call_tool() or named convenience methods.
Uses httpx for HTTP requests with proper error handling.

Usage:
    client = SystemRClient(api_key="sr_agent_...")

    # Named method
    result = client.pre_trade_gate(symbol="AAPL", ...)

    # Generic tool call (all 48 tools)
    result = client.call_tool("calculate_equity_curve", r_multiples=["1.5", "-1.0"], starting_equity="100000")

    # Workflow chain
    results = client.run_backtest_diagnostic(r_multiples=["1.5", "-1.0", "2.0", ...])
"""

import httpx
from typing import Any, Dict, List, Optional


class SystemRError(Exception):
    """Base exception for System R SDK errors."""

    def __init__(self, message: str, status_code: int = 0, detail: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail


class InsufficientBalanceError(SystemRError):
    """Raised when the agent's balance is too low for an operation."""
    pass


class AuthenticationError(SystemRError):
    """Raised when the API key is invalid or agent is inactive."""
    pass


class SystemRClient:
    """
    Python SDK client for agents.systemr.ai.

    48 tools available via:
    - call_tool(name, **kwargs) for any tool
    - Named methods for common operations
    - Workflow methods for multi-tool chains

    All methods return dicts with string values for financial amounts
    to preserve Decimal precision.
    """

    DEFAULT_BASE_URL = "https://agents.systemr.ai"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the System R client.

        Args:
            api_key: Agent API key (starts with 'sr_agent_').
            base_url: API base URL. Defaults to https://agents.systemr.ai.
            timeout: Request timeout in seconds.
        """
        self._base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={"X-API-Key": api_key},
            timeout=timeout,
        )

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make an API request with error handling."""
        resp = self._client.request(method, path, **kwargs)

        if resp.status_code == 401:
            raise AuthenticationError(
                "Authentication failed", status_code=401,
                detail=resp.json().get("detail", ""),
            )
        if resp.status_code == 402:
            raise InsufficientBalanceError(
                "Insufficient balance", status_code=402,
                detail=resp.json().get("detail", ""),
            )
        if resp.status_code == 403:
            raise AuthenticationError(
                "Agent is not active", status_code=403,
                detail=resp.json().get("detail", ""),
            )
        if resp.status_code >= 400:
            detail = resp.json().get("detail", resp.text)
            raise SystemRError(
                f"API error: {detail}",
                status_code=resp.status_code,
                detail=detail,
            )

        return resp.json()

    # === Generic Tool Call (access all 48 tools) ===

    def call_tool(self, tool_name: str, **arguments: Any) -> dict:
        """
        Call any System R tool by name.

        This is the universal method. All 48 tools are accessible:
        - Analysis: analyze_drawdown, run_monte_carlo, calculate_kelly, etc.
        - Intelligence: detect_regime, detect_patterns, analyze_greeks, etc.
        - Planning: build_options_plan, build_futures_plan, etc.
        - Data: calculate_pnl, calculate_expected_value, check_compliance, etc.
        - System: calculate_equity_curve, score_signal, evaluate_scanner, etc.

        Args:
            tool_name: Tool name (e.g. 'calculate_equity_curve').
            **arguments: Tool-specific arguments as keyword args.

        Returns:
            Dict with tool_name and result.

        Example:
            result = client.call_tool("calculate_equity_curve",
                r_multiples=["1.5", "-1.0", "2.0"],
                starting_equity="100000",
            )
            print(result["result"]["total_return"])
        """
        resp = self._request("POST", "/v1/tools/call", json={
            "tool_name": tool_name,
            "arguments": arguments,
        })
        return resp.get("result", resp)

    def list_tools(self) -> dict:
        """
        List all available tools with descriptions and pricing.

        No authentication required.

        Returns:
            Dict with tool_count and tools list.
        """
        return self._request("GET", "/v1/tools/list")

    # === Agent Management ===

    def get_info(self) -> dict:
        """Get current agent information."""
        return self._request("GET", "/v1/agents/me")

    def list_agents(self) -> dict:
        """List all agents owned by the same owner."""
        return self._request("GET", "/v1/agents/list")

    def update_mode(self, mode: str) -> dict:
        """Change agent mode (sandbox, live, suspended, terminated)."""
        return self._request("PUT", "/v1/agents/mode", json={"mode": mode})

    # === Billing ===

    def get_balance(self) -> dict:
        """Get current USDC balance."""
        return self._request("GET", "/v1/billing/balance")

    def deposit(
        self,
        amount: str,
        funding_path: str = "direct_transfer",
        on_chain_tx_hash: Optional[str] = None,
    ) -> dict:
        """Record a USDC deposit."""
        payload: Dict[str, str] = {
            "amount": amount,
            "funding_path": funding_path,
        }
        if on_chain_tx_hash:
            payload["on_chain_tx_hash"] = on_chain_tx_hash
        return self._request("POST", "/v1/billing/deposit", json=payload)

    def get_transactions(self, limit: int = 100) -> dict:
        """Get recent billing transactions."""
        return self._request("GET", f"/v1/billing/transactions?limit={limit}")

    def get_usage(self) -> dict:
        """Get usage summary grouped by operation."""
        return self._request("GET", "/v1/billing/usage")

    def get_pricing(self) -> dict:
        """Get current operation pricing (no auth required)."""
        return self._request("GET", "/v1/billing/pricing")

    # === Position Sizing ===

    def calculate_position_size(
        self,
        equity: str,
        entry_price: str,
        stop_price: str,
        direction: str,
        risk_percent: Optional[str] = None,
        instrument: Optional[str] = None,
    ) -> dict:
        """
        Calculate optimal position size using G-formula.

        Cost: $0.003 USDC.

        Args:
            equity: Account equity in USD.
            entry_price: Planned entry price.
            stop_price: Stop loss price.
            direction: 'long' or 'short'.
            risk_percent: Risk as decimal (e.g. '0.02'). Optional.
            instrument: Instrument symbol. Optional.

        Returns:
            Dict with shares, risk_amount, risk_percent, notional, one_r_dollars.
        """
        payload: Dict[str, str] = {
            "equity": equity,
            "entry_price": entry_price,
            "stop_price": stop_price,
            "direction": direction,
        }
        if risk_percent:
            payload["risk_percent"] = risk_percent
        if instrument:
            payload["instrument"] = instrument
        return self._request("POST", "/v1/sizing/calculate", json=payload)

    # === Risk Check ===

    def check_risk(
        self,
        symbol: str,
        direction: str,
        entry_price: str,
        stop_price: str,
        quantity: str,
        equity: str,
        daily_pnl: str = "0",
    ) -> dict:
        """
        Validate trade risk using Iron Fist rules.

        Cost: $0.004 USDC.

        Returns:
            Dict with approved (bool), score (0-100), errors, warnings.
        """
        return self._request("POST", "/v1/risk/check", json={
            "symbol": symbol,
            "direction": direction,
            "entry_price": entry_price,
            "stop_price": stop_price,
            "quantity": quantity,
            "equity": equity,
            "daily_pnl": daily_pnl,
        })

    # === Evaluation ===

    def basic_eval(self, r_multiples: List[str]) -> dict:
        """
        Basic evaluation -- G metric and verdict.

        Cost: $0.10 USDC.
        """
        return self._request("POST", "/v1/eval/basic", json={
            "r_multiples": r_multiples,
        })

    def full_eval(
        self, r_multiples: List[str], window_size: int = 10
    ) -> dict:
        """
        Full evaluation -- G + rolling G + System R Score.

        Cost: $0.50 USDC.
        """
        return self._request("POST", "/v1/eval/full", json={
            "r_multiples": r_multiples,
            "window_size": window_size,
        })

    def comprehensive_eval(
        self, r_multiples: List[str], window_size: int = 10
    ) -> dict:
        """
        Comprehensive evaluation -- all metrics + impact analysis.

        Cost: $1.00 USDC.
        """
        return self._request("POST", "/v1/eval/comprehensive", json={
            "r_multiples": r_multiples,
            "window_size": window_size,
        })

    # === Compound Operations ===

    def pre_trade_gate(
        self,
        symbol: str,
        direction: str,
        entry_price: str,
        stop_price: str,
        equity: str,
        daily_pnl: str = "0",
        risk_percent: Optional[str] = None,
        r_multiples: Optional[List[str]] = None,
    ) -> dict:
        """
        Pre-trade validation gate: sizing + risk + system health in one call.

        Use this before every trade. Returns gate_passed (bool), sizing,
        risk assessment, and optional system health check.

        Cost: $0.01 USDC.

        Args:
            symbol: Instrument symbol (e.g. 'AAPL').
            direction: 'long' or 'short'.
            entry_price: Planned entry price.
            stop_price: Stop loss price.
            equity: Account equity in USD.
            daily_pnl: Today's P&L so far. Default '0'.
            risk_percent: Risk as decimal (e.g. '0.02'). Optional.
            r_multiples: Recent R-multiples for system health. Optional.

        Returns:
            Dict with gate_passed, sizing, risk, system_health.
        """
        payload: Dict[str, Any] = {
            "symbol": symbol,
            "direction": direction,
            "entry_price": entry_price,
            "stop_price": stop_price,
            "equity": equity,
            "daily_pnl": daily_pnl,
        }
        if risk_percent:
            payload["risk_percent"] = risk_percent
        if r_multiples:
            payload["r_multiples"] = r_multiples
        return self._request("POST", "/v1/compound/pre-trade-gate", json=payload)

    def assess_system(
        self,
        r_multiples: List[str],
        starting_equity: str = "100000",
        pnl_values: Optional[List[str]] = None,
    ) -> dict:
        """
        Full trading system assessment: G-metrics, win/loss, Kelly,
        Monte Carlo, drawdown, and what-if analysis.

        Cost: $2.00 USDC.

        Args:
            r_multiples: R-multiples from trade history (min 5).
            starting_equity: Starting equity for simulations.
            pnl_values: Absolute P&L values. Optional.

        Returns:
            Dict with verdict, g_metrics, win_loss, kelly, monte_carlo,
            drawdown, what_if.
        """
        payload: Dict[str, Any] = {
            "r_multiples": r_multiples,
            "starting_equity": starting_equity,
        }
        if pnl_values:
            payload["pnl_values"] = pnl_values
        return self._request("POST", "/v1/compound/assess-system", json=payload)

    # === Trade Journal ===

    def record_trade(
        self,
        symbol: str,
        direction: str,
        entry_price: str,
        exit_price: str,
        stop_price: str,
        quantity: str,
        r_multiple: Optional[str] = None,
        pnl: Optional[str] = None,
        trade_date: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """
        Record a completed trade to the journal.

        Goes through MCP billing (cost per call).

        Args:
            symbol: Instrument symbol (e.g. 'AAPL').
            direction: 'long' or 'short'.
            entry_price: Entry price.
            exit_price: Exit price.
            stop_price: Stop loss price.
            quantity: Number of shares/contracts.
            r_multiple: Realized R-multiple. Optional.
            pnl: Realized P&L in dollars. Optional.
            trade_date: Trade date as ISO string (e.g. '2026-03-09'). Optional.
            notes: Free-text notes about the trade. Optional.

        Returns:
            Dict with recorded trade details.
        """
        args: Dict[str, Any] = {
            "symbol": symbol,
            "direction": direction,
            "entry_price": entry_price,
            "exit_price": exit_price,
            "stop_price": stop_price,
            "quantity": quantity,
        }
        if r_multiple is not None:
            args["r_multiple"] = r_multiple
        if pnl is not None:
            args["pnl"] = pnl
        if trade_date is not None:
            args["trade_date"] = trade_date
        if notes is not None:
            args["notes"] = notes
        return self.call_tool("record_trade_outcome", **args)

    def get_journal_trades(self, limit: int = 50) -> dict:
        """
        Get recent trades from the journal.

        Free REST endpoint (no billing charge).

        Args:
            limit: Maximum number of trades to return. Default 50.

        Returns:
            Dict with list of journal trades.
        """
        return self._request("GET", f"/v1/journal/trades?limit={limit}")

    def get_journal_stats(self) -> dict:
        """
        Get aggregate journal statistics (win rate, avg R, P&L, etc.).

        Free REST endpoint (no billing charge).

        Returns:
            Dict with journal statistics.
        """
        return self._request("GET", "/v1/journal/stats")

    def get_journal_r_multiples(self, limit: int = 50) -> dict:
        """
        Get R-multiples from journal trades.

        Free REST endpoint (no billing charge).

        Args:
            limit: Maximum number of R-multiples to return. Default 50.

        Returns:
            Dict with list of R-multiples from journal trades.
        """
        return self._request("GET", f"/v1/journal/r-multiples?limit={limit}")

    # === Workflow Methods (multi-tool chains) ===

    def run_backtest_diagnostic(
        self,
        r_multiples: List[str],
        starting_equity: str = "100000",
    ) -> dict:
        """
        Run a complete backtest diagnostic chain (6 tools).

        Flow: equity_curve → system_r_score → drawdown → monte_carlo
              → variance_killers → win_loss
        Total cost: ~$0.032 USDC.

        Args:
            r_multiples: R-multiples from backtest.
            starting_equity: Starting equity.

        Returns:
            Dict with equity_curve, system_r_score, drawdown,
            monte_carlo, variance_killers, win_loss results.
        """
        results: Dict[str, Any] = {}

        results["equity_curve"] = self.call_tool(
            "calculate_equity_curve",
            r_multiples=r_multiples,
            starting_equity=starting_equity,
        )

        results["system_r_score"] = self.call_tool(
            "calculate_system_r_score",
            r_multiples=r_multiples,
        )

        results["drawdown"] = self.call_tool(
            "analyze_drawdown",
            r_multiples=r_multiples,
            starting_equity=starting_equity,
        )

        results["monte_carlo"] = self.call_tool(
            "run_monte_carlo",
            r_multiples=r_multiples,
            starting_equity=starting_equity,
        )

        results["variance_killers"] = self.call_tool(
            "find_variance_killers",
            r_multiples=r_multiples,
        )

        results["win_loss"] = self.call_tool(
            "analyze_win_loss",
            r_multiples=r_multiples,
        )

        return results

    def run_post_trade_analysis(
        self,
        realized_pnl: str,
        realized_r: str,
        mfe: str,
        one_r_dollars: str,
        entry_price: str,
        exit_price: str,
        quantity: int,
        direction: str,
        expected_value_r: Optional[str] = None,
        stop_price: Optional[str] = None,
    ) -> dict:
        """
        Run post-trade analysis chain (2 tools).

        Flow: calculate_pnl → analyze_trade_outcome
        Total cost: $0.006 USDC.

        Args:
            realized_pnl: Net P&L in dollars.
            realized_r: Actual R-multiple.
            mfe: Maximum favorable excursion in dollars.
            one_r_dollars: Dollar value of 1R.
            entry_price: Entry price.
            exit_price: Exit price.
            quantity: Position quantity.
            direction: 'LONG' or 'SHORT'.
            expected_value_r: Expected value in R. Optional.
            stop_price: Stop loss price. Optional.

        Returns:
            Dict with pnl and outcome results.
        """
        pnl_args: Dict[str, Any] = {
            "entry_price": entry_price,
            "exit_price": exit_price,
            "quantity": quantity,
            "direction": direction,
        }
        if stop_price:
            pnl_args["stop_price"] = stop_price

        results: Dict[str, Any] = {}
        results["pnl"] = self.call_tool("calculate_pnl", **pnl_args)

        outcome_args: Dict[str, Any] = {
            "realized_pnl": realized_pnl,
            "realized_r": realized_r,
            "mfe": mfe,
            "one_r_dollars": one_r_dollars,
        }
        if expected_value_r:
            outcome_args["expected_value_r"] = expected_value_r

        results["outcome"] = self.call_tool("analyze_trade_outcome", **outcome_args)

        return results

    def run_market_scan(
        self,
        symbols: List[str],
        conditions: List[str],
        market_data: Dict[str, Dict[str, Any]],
        scanner_name: str = "sdk_scan",
    ) -> dict:
        """
        Run a market scan and score matching signals (2 tools).

        Flow: evaluate_scanner → score_signal (for each match)
        Total cost: $0.005 + $0.003 per match.

        Args:
            symbols: Symbols to scan.
            conditions: Technical conditions (e.g. ['rsi_oversold', 'volume_spike']).
            market_data: Market data dict keyed by symbol.
            scanner_name: Name for this scan.

        Returns:
            Dict with scan_results and scored_signals.
        """
        scan = self.call_tool(
            "evaluate_scanner",
            scanner_config={
                "scanner_id": "sdk-scan-1",
                "name": scanner_name,
                "scanner_type": "TECHNICAL",
                "symbols": symbols,
                "timeframes": ["1h"],
                "conditions": conditions,
            },
            market_data=market_data,
        )

        scored = []
        for r in scan.get("results", []):
            conditions_met = len(r.get("conditions_met", []))
            total_conditions = len(conditions)
            score = self.call_tool(
                "score_signal",
                conditions_met=conditions_met,
                total_conditions=total_conditions,
                regime_aligned=r.get("regime", "") in ("TRENDING_UP", "TRENDING_DOWN"),
                indicator_confluence=conditions_met,
                volume_confirmed="volume_spike" in r.get("conditions_met", []),
                risk_reward_ratio="2.0",
            )
            scored.append({
                "symbol": r["symbol"],
                "direction": r["direction"],
                "scan_confidence": r["confidence"],
                "signal_confidence": score["confidence"],
                "quality_score": score["quality_score"],
                "suggested_entry": r["suggested_entry"],
                "suggested_stop": r["suggested_stop"],
            })

        return {
            "scan_results": scan,
            "scored_signals": scored,
        }

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

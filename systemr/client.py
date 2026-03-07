"""
System R Python SDK client.

A simple, ergonomic client for agents to call System R services.
Uses httpx for HTTP requests with proper error handling.

Usage:
    client = SystemRClient(api_key="sr_agent_...")
    result = client.calculate_position_size(...)
"""

import httpx
from typing import Dict, List, Optional


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

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

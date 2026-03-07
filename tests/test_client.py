"""Tests for SystemRClient."""

import json
import pytest
import httpx
from unittest.mock import patch, MagicMock

from systemr import (
    SystemRClient,
    SystemRError,
    AuthenticationError,
    InsufficientBalanceError,
)


def _mock_response(status_code: int, data: dict) -> httpx.Response:
    """Create a mock httpx response."""
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = data
    resp.text = json.dumps(data)
    return resp


class TestSystemRClient:
    """Tests for client initialization."""

    def test_default_base_url(self):
        client = SystemRClient(api_key="sr_agent_test")
        assert client._base_url == "https://agents.systemr.ai"
        client.close()

    def test_custom_base_url(self):
        client = SystemRClient(api_key="sr_agent_test", base_url="http://localhost:8000")
        assert client._base_url == "http://localhost:8000"
        client.close()

    def test_trailing_slash_stripped(self):
        client = SystemRClient(api_key="sr_agent_test", base_url="http://localhost:8000/")
        assert client._base_url == "http://localhost:8000"
        client.close()

    def test_context_manager(self):
        with SystemRClient(api_key="sr_agent_test") as client:
            assert client is not None


class TestErrorHandling:
    """Tests for error handling."""

    def test_authentication_error_on_401(self):
        client = SystemRClient(api_key="sr_agent_bad")
        with patch.object(client._client, "request", return_value=_mock_response(401, {"detail": "Invalid API key"})):
            with pytest.raises(AuthenticationError) as exc_info:
                client.get_info()
            assert exc_info.value.status_code == 401
        client.close()

    def test_insufficient_balance_on_402(self):
        client = SystemRClient(api_key="sr_agent_test")
        with patch.object(client._client, "request", return_value=_mock_response(402, {"detail": "Insufficient balance"})):
            with pytest.raises(InsufficientBalanceError) as exc_info:
                client.calculate_position_size("100000", "185", "180", "long")
            assert exc_info.value.status_code == 402
        client.close()

    def test_inactive_agent_on_403(self):
        client = SystemRClient(api_key="sr_agent_test")
        with patch.object(client._client, "request", return_value=_mock_response(403, {"detail": "Agent is suspended"})):
            with pytest.raises(AuthenticationError) as exc_info:
                client.get_info()
            assert exc_info.value.status_code == 403
        client.close()

    def test_generic_error(self):
        client = SystemRClient(api_key="sr_agent_test")
        with patch.object(client._client, "request", return_value=_mock_response(500, {"detail": "Internal error"})):
            with pytest.raises(SystemRError) as exc_info:
                client.get_info()
            assert exc_info.value.status_code == 500
        client.close()


class TestAgentMethods:
    """Tests for agent management methods."""

    def test_get_info(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"agent_id": "agent-123", "agent_name": "test", "mode": "sandbox"}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.get_info()
        assert result == expected
        client.close()

    def test_list_agents(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"agents": [], "count": 0}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.list_agents()
        assert result["count"] == 0
        client.close()

    def test_update_mode(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"agent_id": "agent-123", "mode": "live"}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)) as mock_req:
            result = client.update_mode("live")
            mock_req.assert_called_once_with("PUT", "/v1/agents/mode", json={"mode": "live"})
        assert result["mode"] == "live"
        client.close()


class TestPositionSizing:
    """Tests for position sizing."""

    def test_calculate_position_size(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"shares": "181", "risk_amount": "995.50"}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)) as mock_req:
            result = client.calculate_position_size("100000", "185.50", "180.00", "long")
            mock_req.assert_called_once_with(
                "POST", "/v1/sizing/calculate",
                json={"equity": "100000", "entry_price": "185.50", "stop_price": "180.00", "direction": "long"},
            )
        assert result["shares"] == "181"
        client.close()

    def test_calculate_with_optional_params(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"shares": "100"}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)) as mock_req:
            client.calculate_position_size("100000", "185", "180", "long", risk_percent="0.02", instrument="AAPL")
            call_kwargs = mock_req.call_args
            payload = call_kwargs.kwargs["json"]
            assert payload["risk_percent"] == "0.02"
            assert payload["instrument"] == "AAPL"
        client.close()


class TestRiskCheck:
    """Tests for risk validation."""

    def test_check_risk(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"approved": True, "score": 85}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.check_risk("AAPL", "long", "185.50", "180.00", "100", "100000")
        assert result["approved"] is True
        client.close()


class TestEvaluation:
    """Tests for evaluation methods."""

    def test_basic_eval(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"g_score": "0.15", "verdict": "positive_edge"}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.basic_eval(["1.5", "-1.0", "2.3"])
        assert result["verdict"] == "positive_edge"
        client.close()

    def test_full_eval(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"g_score": "0.15", "system_r_score": "72"}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)) as mock_req:
            result = client.full_eval(["1.5", "-1.0"], window_size=5)
            payload = mock_req.call_args.kwargs["json"]
            assert payload["window_size"] == 5
        assert "system_r_score" in result
        client.close()

    def test_comprehensive_eval(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"g_score": "0.15", "impact": {}}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.comprehensive_eval(["1.5", "-1.0"])
        assert "impact" in result
        client.close()


class TestBilling:
    """Tests for billing methods."""

    def test_get_balance(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"balance": "10.50", "is_low": False}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.get_balance()
        assert result["balance"] == "10.50"
        client.close()

    def test_get_pricing_no_auth(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"prices": {"position_sizing": "0.003"}}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.get_pricing()
        assert "prices" in result
        client.close()

    def test_deposit(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"balance_after": "25.00"}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)) as mock_req:
            result = client.deposit("25.00", on_chain_tx_hash="0xabc")
            payload = mock_req.call_args.kwargs["json"]
            assert payload["amount"] == "25.00"
            assert payload["on_chain_tx_hash"] == "0xabc"
        client.close()

    def test_get_transactions(self):
        client = SystemRClient(api_key="sr_agent_test")
        expected = {"transactions": []}
        with patch.object(client._client, "request", return_value=_mock_response(200, expected)):
            result = client.get_transactions(limit=10)
        assert result["transactions"] == []
        client.close()

"""
System R CLI — command-line interface for agents.systemr.ai.

Usage:
    systemr register --owner-id my-id --name my-agent --type trading
    systemr info
    systemr balance
    systemr size --equity 100000 --entry 185.50 --stop 180.00 --direction long
    systemr risk --symbol AAPL --direction long --entry 185.50 --stop 180.00 --qty 100 --equity 100000
    systemr eval 1.5 -1.0 2.3 -0.5 1.8
    systemr pricing
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

import click
import httpx

from systemr import __version__

CONFIG_DIR = Path.home() / ".systemr"
CONFIG_FILE = CONFIG_DIR / "config.json"

BANNER = r"""
   ___           __               ___
  / __| _  _ ___| |_ ___ _ __   | _ \
  \__ \| || (_-<|  _/ -_) '  \  |   /
  |___/ \_, /__/ \__\___|_|_|_| |_|_\
        |__/
"""


def _load_config() -> dict:
    """Load saved config."""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def _save_config(config: dict) -> None:
    """Save config to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def _get_api_key() -> str:
    """Get API key from env or config."""
    key = os.environ.get("SYSTEMR_API_KEY")
    if key:
        return key
    config = _load_config()
    key = config.get("api_key")
    if key:
        return key
    click.echo(click.style("Error: ", fg="red", bold=True) + "No API key found.")
    click.echo("Set via: systemr auth <api-key>")
    click.echo("Or env:  export SYSTEMR_API_KEY=sr_agent_...")
    sys.exit(1)


def _get_base_url() -> str:
    """Get base URL from env or config."""
    url = os.environ.get("SYSTEMR_BASE_URL")
    if url:
        return url
    config = _load_config()
    return config.get("base_url", "https://agents.systemr.ai")


def _request(method: str, path: str, auth: bool = True, **kwargs) -> dict:
    """Make an API request."""
    base_url = _get_base_url()
    headers = {}
    if auth:
        headers["X-API-Key"] = _get_api_key()

    try:
        resp = httpx.request(method, f"{base_url}{path}", headers=headers, timeout=30.0, **kwargs)
    except httpx.ConnectError:
        click.echo(click.style("Error: ", fg="red", bold=True) + f"Cannot connect to {base_url}")
        sys.exit(1)

    if resp.status_code == 401:
        click.echo(click.style("Error: ", fg="red", bold=True) + "Invalid API key.")
        sys.exit(1)
    if resp.status_code == 402:
        click.echo(click.style("Error: ", fg="red", bold=True) + "Insufficient balance. Deposit USDC to continue.")
        sys.exit(1)
    if resp.status_code == 403:
        click.echo(click.style("Error: ", fg="red", bold=True) + "Agent is not active.")
        sys.exit(1)
    if resp.status_code >= 400:
        detail = resp.json().get("detail", resp.text) if resp.headers.get("content-type", "").startswith("application/json") else resp.text
        click.echo(click.style("Error: ", fg="red", bold=True) + str(detail))
        sys.exit(1)

    return resp.json()


def _kv(label: str, value: str, label_width: int = 16) -> None:
    """Print a key-value pair."""
    click.echo(f"  {click.style(label.ljust(label_width), fg='cyan')}{value}")


def _table(headers: list, rows: list) -> None:
    """Print a simple table."""
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    header_line = "  ".join(click.style(h.ljust(widths[i]), fg="cyan", bold=True) for i, h in enumerate(headers))
    sep_line = "  ".join("─" * widths[i] for i in range(len(headers)))
    click.echo(f"  {header_line}")
    click.echo(f"  {sep_line}")
    for row in rows:
        line = "  ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
        click.echo(f"  {line}")


# ─── CLI Group ──────────────────────────────────────────────

@click.group()
@click.version_option(__version__, prog_name="systemr")
def cli():
    """System R — AI-native risk intelligence for trading agents."""
    pass


# ─── Auth ───────────────────────────────────────────────────

@cli.command()
@click.argument("api_key")
def auth(api_key: str):
    """Save your API key locally."""
    config = _load_config()
    config["api_key"] = api_key
    _save_config(config)
    masked = api_key[:12] + "..." + api_key[-4:]
    click.echo(click.style("✓ ", fg="green", bold=True) + f"API key saved: {masked}")
    click.echo(f"  Config: {CONFIG_FILE}")


# ─── Register ──────────────────────────────────────────────

@cli.command()
@click.option("--owner-id", required=True, help="Your owner/user ID.")
@click.option("--name", required=True, help="Agent display name.")
@click.option("--type", "agent_type", type=click.Choice(["trading", "analysis", "risk", "composite"]), default="trading", help="Agent type.")
@click.option("--description", default=None, help="Optional description.")
def register(owner_id: str, name: str, agent_type: str, description: Optional[str]):
    """Register a new agent and get an API key."""
    payload = {
        "owner_id": owner_id,
        "agent_name": name,
        "agent_type": agent_type,
    }
    if description:
        payload["description"] = description

    data = _request("POST", "/v1/agents/register", auth=False, json=payload)

    click.echo()
    click.echo(click.style("  Agent registered", fg="green", bold=True))
    click.echo()
    _kv("Agent ID", data["agent_id"])
    _kv("Name", data["agent_name"])
    _kv("Type", data["agent_type"])
    _kv("Mode", data["mode"])
    _kv("Created", data["created_at"])
    click.echo()
    click.echo(click.style("  API Key", fg="yellow", bold=True))
    click.echo(f"  {data['api_key']}")
    click.echo()
    click.echo(click.style("  ⚠ Save this key — it won't be shown again.", fg="yellow"))
    click.echo()

    # Offer to save
    if click.confirm("  Save this key to ~/.systemr/config.json?", default=True):
        config = _load_config()
        config["api_key"] = data["api_key"]
        _save_config(config)
        click.echo(click.style("  ✓ ", fg="green") + "Saved.")


# ─── Info ──────────────────────────────────────────────────

@cli.command()
def info():
    """Show current agent info."""
    data = _request("GET", "/v1/agents/me")

    click.echo()
    _kv("Agent ID", data["agent_id"])
    _kv("Owner", data["owner_id"])
    _kv("Name", data["agent_name"])
    _kv("Type", data["agent_type"])
    _kv("Mode", click.style(data["mode"], fg="green" if data["mode"] in ("sandbox", "live") else "red"))
    _kv("Active", click.style("yes", fg="green") if data.get("is_active") else click.style("no", fg="red"))
    _kv("Created", data["created_at"])
    if data.get("description"):
        _kv("Description", data["description"])
    click.echo()


# ─── Balance ──────────────────────────────────────────────

@cli.command()
def balance():
    """Show current USDC balance."""
    data = _request("GET", "/v1/billing/balance")

    bal = data["balance"]
    color = "red" if data.get("is_low") else "green"
    click.echo()
    click.echo(f"  Balance: {click.style(f'${bal} USDC', fg=color, bold=True)}")
    if data.get("is_low"):
        click.echo(click.style("  ⚠ Low balance — deposit to continue using paid endpoints.", fg="yellow"))
    click.echo()


# ─── Pricing ──────────────────────────────────────────────

@cli.command()
def pricing():
    """Show operation pricing."""
    data = _request("GET", "/v1/billing/pricing", auth=False)

    click.echo()
    click.echo(click.style("  Pricing (USDC per call)", bold=True))
    click.echo()

    rows = []
    for op, price in data.get("prices", {}).items():
        label = op.replace("_", " ").title()
        rows.append([label, f"${price}"])

    _table(["Operation", "Cost"], rows)
    click.echo()


# ─── Transactions ──────────────────────────────────────────

@cli.command()
@click.option("--limit", default=20, help="Number of transactions to show.")
def transactions(limit: int):
    """Show recent billing transactions."""
    data = _request("GET", f"/v1/billing/transactions?limit={limit}")

    txns = data.get("transactions", [])
    if not txns:
        click.echo("  No transactions yet.")
        return

    click.echo()
    rows = []
    for tx in txns:
        rows.append([
            tx.get("created_at", "")[:19],
            tx.get("type", ""),
            f"${tx.get('amount', '0')}",
            f"${tx.get('balance_after', '0')}",
            tx.get("operation", "") or "",
        ])

    _table(["Time", "Type", "Amount", "Balance", "Operation"], rows)
    click.echo()


# ─── Usage ─────────────────────────────────────────────────

@cli.command()
def usage():
    """Show usage summary."""
    data = _request("GET", "/v1/billing/usage")

    summary = data.get("usage", data.get("summary", []))
    if not summary:
        click.echo("  No usage recorded yet.")
        return

    click.echo()
    if isinstance(summary, list):
        rows = [[s.get("operation", ""), str(s.get("count", 0)), f"${s.get('total_cost', '0')}"] for s in summary]
        _table(["Operation", "Count", "Total Cost"], rows)
    else:
        for k, v in summary.items():
            _kv(k, str(v))
    click.echo()


# ─── Position Sizing ──────────────────────────────────────

@cli.command()
@click.option("--equity", required=True, help="Account equity in USD.")
@click.option("--entry", required=True, help="Entry price.")
@click.option("--stop", required=True, help="Stop loss price.")
@click.option("--direction", required=True, type=click.Choice(["long", "short"]), help="Trade direction.")
@click.option("--risk-pct", default=None, help="Risk percent as decimal (e.g. 0.02).")
@click.option("--instrument", default=None, help="Instrument symbol.")
def size(equity: str, entry: str, stop: str, direction: str, risk_pct: Optional[str], instrument: Optional[str]):
    """Calculate optimal position size (G-formula). $0.003"""
    payload = {
        "equity": equity,
        "entry_price": entry,
        "stop_price": stop,
        "direction": direction,
    }
    if risk_pct:
        payload["risk_percent"] = risk_pct
    if instrument:
        payload["instrument"] = instrument

    data = _request("POST", "/v1/sizing/calculate", json=payload)

    click.echo()
    click.echo(click.style("  Position Size", bold=True))
    click.echo()
    _kv("Shares", click.style(str(data.get("shares", "")), fg="green", bold=True))
    _kv("Risk Amount", f"${data.get('risk_amount', '')}")
    _kv("Risk Percent", data.get("risk_percent", ""))
    _kv("Notional", f"${data.get('notional', '')}")
    _kv("1R Dollars", f"${data.get('one_r_dollars', '')}")
    click.echo()


# ─── Risk Check ────────────────────────────────────────────

@cli.command()
@click.option("--symbol", required=True, help="Instrument symbol.")
@click.option("--direction", required=True, type=click.Choice(["long", "short"]), help="Trade direction.")
@click.option("--entry", required=True, help="Entry price.")
@click.option("--stop", required=True, help="Stop loss price.")
@click.option("--qty", required=True, help="Number of shares/contracts.")
@click.option("--equity", required=True, help="Account equity.")
@click.option("--daily-pnl", default="0", help="Daily P&L so far.")
def risk(symbol: str, direction: str, entry: str, stop: str, qty: str, equity: str, daily_pnl: str):
    """Validate trade risk (Iron Fist). $0.004"""
    data = _request("POST", "/v1/risk/check", json={
        "symbol": symbol,
        "direction": direction,
        "entry_price": entry,
        "stop_price": stop,
        "quantity": qty,
        "equity": equity,
        "daily_pnl": daily_pnl,
    })

    click.echo()
    approved = data.get("approved", False)
    if approved:
        click.echo(click.style("  ✓ APPROVED", fg="green", bold=True))
    else:
        click.echo(click.style("  ✗ REJECTED", fg="red", bold=True))

    click.echo()
    _kv("Score", str(data.get("score", "")))

    errors = data.get("errors", [])
    if errors:
        click.echo()
        click.echo(click.style("  Errors:", fg="red"))
        for e in errors:
            click.echo(f"    • {e}")

    warnings = data.get("warnings", [])
    if warnings:
        click.echo()
        click.echo(click.style("  Warnings:", fg="yellow"))
        for w in warnings:
            click.echo(f"    • {w}")

    click.echo()


# ─── Eval ──────────────────────────────────────────────────

@cli.command(name="eval")
@click.argument("r_multiples", nargs=-1, required=True)
@click.option("--tier", type=click.Choice(["basic", "full", "comprehensive"]), default="basic", help="Evaluation tier.")
@click.option("--window", default=10, help="Rolling window size (full/comprehensive).")
def evaluate(r_multiples: tuple, tier: str, window: int):
    """Evaluate strategy from R-multiples. $0.10-$1.00

    Pass R-multiples as arguments: systemr eval 1.5 -1.0 2.3 -0.5 1.8
    """
    r_list = list(r_multiples)

    endpoints = {
        "basic": "/v1/eval/basic",
        "full": "/v1/eval/full",
        "comprehensive": "/v1/eval/comprehensive",
    }
    costs = {"basic": "$0.10", "full": "$0.50", "comprehensive": "$1.00"}

    payload = {"r_multiples": r_list}
    if tier in ("full", "comprehensive"):
        payload["window_size"] = window

    data = _request("POST", endpoints[tier], json=payload)

    click.echo()
    click.echo(click.style(f"  {tier.title()} Evaluation", bold=True) + f"  ({costs[tier]})")
    click.echo()

    _kv("G Score", click.style(str(data.get("g_score", "")), fg="green", bold=True))
    if "verdict" in data:
        _kv("Verdict", data["verdict"])
    if "system_r_score" in data:
        _kv("System R Score", str(data["system_r_score"]))
    if "trade_count" in data:
        _kv("Trades", str(data["trade_count"]))
    if "win_rate" in data:
        _kv("Win Rate", data["win_rate"])
    if "expectancy" in data:
        _kv("Expectancy", data["expectancy"])
    if "rolling_g" in data:
        click.echo()
        click.echo(click.style("  Rolling G:", fg="cyan"))
        for i, g in enumerate(data["rolling_g"]):
            click.echo(f"    [{i+1}] {g}")

    click.echo()


# ─── Whoami ────────────────────────────────────────────────

@cli.command()
def whoami():
    """Show saved config and connection status."""
    config = _load_config()
    click.echo()
    click.echo(click.style("  Config", bold=True))
    click.echo(f"  File: {CONFIG_FILE}")
    click.echo()

    key = config.get("api_key", os.environ.get("SYSTEMR_API_KEY", ""))
    if key:
        source = "config" if config.get("api_key") else "env"
        masked = key[:12] + "..." + key[-4:]
        _kv("API Key", f"{masked} ({source})")
    else:
        _kv("API Key", click.style("not set", fg="red"))

    base_url = config.get("base_url", os.environ.get("SYSTEMR_BASE_URL", "https://agents.systemr.ai"))
    _kv("Base URL", base_url)

    # Test connection
    try:
        resp = httpx.get(f"{base_url}/v1/health", timeout=5.0)
        if resp.status_code == 200:
            _kv("Status", click.style("connected", fg="green"))
        else:
            _kv("Status", click.style(f"error ({resp.status_code})", fg="red"))
    except Exception:
        _kv("Status", click.style("unreachable", fg="red"))

    click.echo()


if __name__ == "__main__":
    cli()

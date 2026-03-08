# Changelog

## 2.0.0 (2026-03-09)

- **47 tools** accessible via `call_tool(name, **kwargs)` — universal method for all tools
- 3 workflow chain methods:
  - `run_backtest_diagnostic()` — 6-tool chain (~$0.032)
  - `run_post_trade_analysis()` — 2-tool chain ($0.006)
  - `run_market_scan()` — scanner + signal scoring ($0.005+)
- Compound operation methods:
  - `pre_trade_gate()` — sizing + risk + system health ($0.01)
  - `assess_system()` — full system assessment ($2.00)
- `list_tools()` — discover all available tools with pricing
- Workflow cookbook: `examples/workflow_cookbook.py`
- Updated README with complete 47-tool documentation

## 1.0.0 (2026-03-08)

- Initial release
- `SystemRClient` with position sizing, risk validation, and evaluation endpoints
- Agent registration, authentication, and billing management
- Error classes: `SystemRError`, `AuthenticationError`, `InsufficientBalanceError`
- Context manager support

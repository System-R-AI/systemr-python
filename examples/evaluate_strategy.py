"""
Strategy evaluation example — compute G metric from R-multiples.
"""

from systemr import SystemRClient

client = SystemRClient(api_key="sr_agent_YOUR_KEY_HERE")

# R-multiples from recent trades
r_multiples = ["1.5", "-1.0", "2.3", "-0.5", "1.8", "-1.0", "3.2", "0.8"]

# Basic eval ($0.10)
basic = client.basic_eval(r_multiples=r_multiples)
print(f"G Score: {basic['g_score']}")
print(f"Verdict: {basic['verdict']}")

# Full eval ($0.50) — includes rolling G and System R Score
full = client.full_eval(r_multiples=r_multiples, window_size=5)
print(f"System R Score: {full['system_r_score']}")

client.close()

FROM python:3.11-slim

RUN pip install --no-cache-dir systemr "mcp>=1.8.0"

ENTRYPOINT ["python", "-m", "systemr.mcp_server"]

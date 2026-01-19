#!/bin/bash
# Run the Baltimore Permit MCP Server with Python 3.11

cd "$(dirname "$0")"
exec python3.11 server.py

#!/bin/bash
set -a
source .env
set +a
uv run src/receipt_scanner/agent/main.py

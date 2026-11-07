#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

python3 src/main.py
python3 -m http.server 8888 --directory docs

#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller
pyinstaller --noconfirm prompter.spec

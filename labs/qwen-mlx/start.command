#!/bin/zsh
set -eu
cd "${0:A:h}"
source ./offline-env.sh
exec /usr/bin/sandbox-exec -f offline.sb .venv/bin/python -u app/project/app.py

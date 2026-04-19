#!/usr/bin/env bash
# Remove generated artifacts from all presentation directories.
# Run from repo root: ./clean.sh
# Use --venv to also remove .venv directories.

set -euo pipefail

REMOVE_VENV=false
for arg in "$@"; do
  [[ "$arg" == "--venv" ]] && REMOVE_VENV=true
done

find . -not -path './.git/*' \( \
  -name '*.png' -o \
  -name '*.pptx' -o \
  -name '*.docx' -o \
  -name '__pycache__' -o \
  -name '*.pyc' -o \
  -name '*.pyo' \
\) -print -delete

if $REMOVE_VENV; then
  find . -not -path './.git/*' -name '.venv' -type d -print -exec rm -rf {} +
fi

echo "Clean complete."

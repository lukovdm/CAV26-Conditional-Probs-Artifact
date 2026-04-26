#!/usr/bin/env bash
# Run this on the server from the project directory.
# Creates project_backup.tar.gz, excluding .dockerignore entries except docker-image.tar.
set -euo pipefail

ARCHIVE="project_backup.tar.gz"

tar -c \
    --exclude='.vscode' \
    --exclude='.venv' \
    --exclude='out' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='project_backup.tar.gz' \
    . | pv -s 19g | gzip > "$ARCHIVE"

echo "Created $ARCHIVE ($(du -sh "$ARCHIVE" | cut -f1))"
echo "Download with:"
echo "  scp \$SERVER:\$(pwd)/$ARCHIVE ."

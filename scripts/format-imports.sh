#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort main.py core.py config.py test.py API MySQL --force-single-line-imports
sh ./scripts/format.sh
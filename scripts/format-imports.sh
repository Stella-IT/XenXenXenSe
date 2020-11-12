#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort main.py test.py app API --force-single-line-imports
sh ./scripts/format.sh
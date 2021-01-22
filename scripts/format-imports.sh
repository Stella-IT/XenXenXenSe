#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort main.py test.py app API --force-single-line-imports

# And now merge it.
isort main.py test.py app API

sh ./scripts/format.sh
#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place main.py test.py app API --exclude=__init__.py
black main.py test.py app API
isort main.py test.py app API

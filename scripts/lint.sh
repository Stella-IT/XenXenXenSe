#!/usr/bin/env bash

set -e
set -x

mypy app API
flake8 main.py test.py app API
black main.py  test.py app API --check
isort main.py test.py app API --check-only

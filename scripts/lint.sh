#!/usr/bin/env bash

set -e
set -x

mypy app API MySQL
flake8 main.py test.py app API MySQL
black main.py  test.py app API MySQL --check
isort main.py test.py app API MySQL --check-only

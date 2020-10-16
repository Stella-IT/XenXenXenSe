#!/usr/bin/env bash

set -e
set -x

mypy config.py API MySQL
flake8 main.py core.py config.py test.py API MySQL
black main.py core.py config.py test.py API MySQL --check
isort main.py core.py config.py test.py API MySQL --check-only
#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place main.py core.py config.py test.py API MySQL --exclude=__init__.py
black main.py core.py config.py test.py API MySQL
isort main.py core.py config.py test.py API MySQL

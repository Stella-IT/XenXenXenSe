#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place main.py test.py app API MySQL --exclude=__init__.py
black main.py test.py app API MySQL
isort main.py test.py app API MySQL

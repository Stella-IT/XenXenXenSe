#!/usr/bin/env bash

set -e
set -x

isort main.py test.py app API --check-only

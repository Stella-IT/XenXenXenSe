#!/usr/bin/env bash

set -e
set -x

flake8 main.py test.py app API

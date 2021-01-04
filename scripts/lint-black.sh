#!/usr/bin/env bash

set -e
set -x

black main.py  test.py app API --check

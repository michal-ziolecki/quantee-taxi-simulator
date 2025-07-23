#!/bin/bash

TEST_PATH="."

if [ -n "$1" ]
  then
    TEST_PATH="$1"
fi

echo "checking path: ${TEST_PATH}"

echo "=== black ==="
black --version
black "$TEST_PATH"

echo "=== isort ==="
isort --version
isort "$TEST_PATH"

echo "=== flake8 ==="
flake8 --version
flake8 "$TEST_PATH"

echo "=== mypy ==="
python -m mypy --version
python -m mypy .

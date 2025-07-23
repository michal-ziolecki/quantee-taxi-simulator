#!/bin/bash

result=0
TEST_PATH="."

if [ -n "$1" ]
  then
    TEST_PATH="$1"
fi

echo "checking path: ${TEST_PATH}"

echo "=== black ==="
python black --version
python black --diff --check "$TEST_PATH"
result=$(($result + $?))

echo "=== isort ==="
python isort --version
python isort -c --diff "$TEST_PATH"
result=$(($result + $?))

echo "=== flake8 ==="
python flake8 --version
python flake8 "$TEST_PATH"
result=$(($result + $?))

echo "=== mypy ==="
python mypy --version
python mypy .
result=$(($result + $?))

echo "static-analysis result: ${result}"
exit $result

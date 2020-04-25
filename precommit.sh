#!/bin/bash

source .env/bin/activate

echo ""
echo "Running tests"
echo ""

python -m pytest tests/ -v

echo ""
echo "Running flake8"
echo ""
flake8 src --max-line-length=160

echo ""
echo "Running mypy"
echo ""
mypy --ignore-missing-imports src

#!/bin/bash

TARGETS="."

# Exit with a non-zero code if Ruff finds any issues.
FAIL_ON_ERROR=true

echo "Starting Ruff checks on: $TARGETS"

ruff check $TARGETS

echo "Applying Ruff fixes..."
ruff check $TARGETS --fix

echo "Formatting code with Ruff..."
ruff format .

echo "Ruff checks completed."


echo "Starting isort on: $TARGETS"

isort $TARGETS

echo "Checking if its all sorted..."

if isort --check "$TARGETS"; then
  echo "isort check passed. Imports are correctly sorted."
else
  echo "isort check failed. Running isort again to apply necessary modifications..."
  isort "$TARGETS"
  if isort --check "$TARGETS"; then
    echo "isort ran again and the check now passes."
  else
    echo "ERROR: isort check still failed after running the formatter again. Please investigate."
    exit 1 # Exit with an error code
  fi
fi


echo "Starting MyPy type checking on $TARGETS"
if mypy "$TARGETS"; then
  echo "MyPy checks passed. No type errors found."
else
  echo "ERROR: MyPy found type errors. Please review the output above and fix the issues."
  exit 1
fi

exit 0

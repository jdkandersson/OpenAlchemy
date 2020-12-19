#!/bin/bash

# Copy application files
cp ../../../examples/app/app.py ../../../examples/app/api.yaml ../../../examples/app/api.py ../../../examples/app/database.py ./

# Copy test files
mkdir -p tests
touch tests/__init__.py
cp ../../examples/app/test_app.py ../conftest.py tests/

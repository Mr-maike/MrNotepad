#!/bin/bash
# Configura ambiente para testes

export PYTHONPATH=$PYTHONPATH:$(pwd)
echo "PYTHONPATH set to: $PYTHONPATH"
echo "Running tests..."
python -m pytest tests/ -v
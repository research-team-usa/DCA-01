#!/bin/bash
set -e
echo "Setting up DCA-01 repo..."
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi redis pydantic jsonschema prometheus_client pytest
 echo "Done. Run make up"

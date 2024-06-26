#!/bin/bash

# Activate virtual environment
source ../venv/bin/activate

# Install dependencies
pip install -r ../api/requirements.txt

# Run Flask app
cd ../api
flask run

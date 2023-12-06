#!/bin/bash

# Navigate to directory where the script is located
# Allows running from cron directly
cd "$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 main.py

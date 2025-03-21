#!/bin/sh

DIR=$(dirname "$(readlink -f "$0")")
cd "${DIR}/script"

[ -d "venv" ] \
  && echo "Virtual environment already exists." \
  || (echo "Creating virtual environment..." && python3 -m venv venv)

echo "Activating virtual environment..."
. venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt


echo "Running main.py..."
cd "${DIR}/script"
python3 main.py

echo ""
echo "Press Enter to run tests..."
read -r _

echo "Running tests..."
python3 -m pytest -v test_main.py

deactivate # virtual environment


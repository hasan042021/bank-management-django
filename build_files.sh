#!/bin/bash
# Install dependencies
pip install -r requirements.txt
# Collect static files
python manage.py collectstatic --noinput

if ! command -v pip &> /dev/null; then
    echo "Python and pip are not installed. Installing now..."
    apt-get update
    apt-get install -y python3 python3-pip
fi
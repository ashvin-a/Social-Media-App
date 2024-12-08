#!/bin/bash
echo "Vercel Build Begins!!!!!!!!"
echo "Installing requirements......"
pip install -r requirements.txt
echo "Requirements installed successfully!"

python3.9 project/manage.py collectstatic
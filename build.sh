#!/bin/bash
set -e  
echo "Vercel Build Begins!!!!!!!!"
echo "Current user: $(whoami)"
echo "Installing requirements......"
pip install -r requirements.txt
echo "Requirements installed successfully!"
ls -la
chmod -R u+w project/

python3 project/manage.py collectstatic
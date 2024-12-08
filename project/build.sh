# /bin/bash
set -e  
echo "Vercel Build Begins!!!!!!!!"
echo "Current user: $(whoami)"
echo "Installing requirements......"
pip install setuptools
pip install -r requirements.txt
echo "Requirements installed successfully!"


python3 manage.py wait_for_db 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
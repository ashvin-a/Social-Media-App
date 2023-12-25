# Social-Media-App
A social media app build with Django.

This is a social media application that is build using Django. This application features session authentication, user profile creation,email notification while user creation,
updation, admin-user accounts with authorization systems, forget passwords etc.

How to use this
 1. create a virtual environment
      python3 -m venv env
 2. Use the virtual environment created
      source env/bin/activate
 3. Install dependencies
      pip install -r requiements.txt

Now you have all the dependencies for running the application. Before starting the server,
make sure to connect the database. In my case, I have used Postgres so make sure you setup your database before running migrations.

python manage.py migrate
python manage.py runserver

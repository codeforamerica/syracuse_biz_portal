# Syracuse Biz Portal


## Install Instructions for Developing with the Sample Project


Requires Postgres and Django be installed.  This project is developed and *only* works with Python 3.5 and Django 1.9 (and probably higher but untested).

```bash
pip install -r requirements/app.txt
```

Copy the local_settings file and update the settings to fit your machine.


  cp local_settings.py.example local_settings.py

Create a database for the application by first logging into postgres (`psql`) then running:

  CREATE DATABASE syracuse_biz_portal;

Test that Django is working and pointed at your database(migrations not yet created).

  ./manage.py migrate

Create a user to log in to and manage the application.

  ./manage.py createsuperuser


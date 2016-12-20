# Syracuse Biz Portal

[![Build Status](https://travis-ci.org/codeforamerica/syracuse_biz_portal.svg?branch=master)](https://travis-ci.org/codeforamerica/syracuse_biz_portal)

## Install Instructions for Developing with the Sample Project


Requires Postgres and Django be installed.  This project is developed and *only* works with Python 3.5 and Django 1.9 (and probably higher but untested).

Use [virtualenv](https://virtualenv.pypa.io/en/stable/) to specify python3.5:
```
virtualenv -p python3 venv
```

Activate virtualenv:
```
source venv/bin/activate
```

Install requirements:
```bash
pip install -r requirements/app.txt
```

Copy the local_settings file and update the settings to fit your machine.
```
cp local_settings.py.example local_settings.py
```

Create a database for the application by first logging into postgres (`psql`) then running:
```
CREATE DATABASE syracuse_biz_portal;
```

Test that Django is working and pointed at your database(migrations not yet created).
```
./manage.py migrate
```

Create a user to log in to and manage the application.
```
./manage.py createsuperuser
```

Start your app:
```
python manage.py runserver
```

Go to [http://localhost:8080/admin](http://localhost:8080/admin) and enter the credentials that you used when running `./manage.py createsuperuser`.

## For Contributors

First thank you for helping its much appreciated.  This project is currently has to major functions to host a bizport CMS with Wagtail and to offer a resource search tool using [wealthmap](https://github.com/codeforamerica/wealthmap) which is configured in the matcher app in this project.

You might end up wanting to make changes to the wealthmap application as well.  If so fork and clone the app to your desktop environment and then install from source like so.

```
pip install -e .
```

This will allow you to work on both repositories and without having to push and upgrade from this project.


### Pushing Up Changes

The best way to help us is to look through existing issues or create new issues. Once its triaged then just fork this code(if not on the team) and make a branch labeled feature/thing_changed.

Once you've made your proposed changes, if the tests pass locally and the pep8 linter doesn't complain (see `.pep8` file) you're ready to file a push your changes up to a branch.  If you are a member of the team Travis-CI will start running tests and will verify all the tests are passing.  If all is well you are ready to file a PR(pull request).

When a PR is filed out on Github the description should include the issue it fixes, if there is no issue then explain what has changed.  Heroku will automatically build a review app for manual testing and travis-ci will run and include the results on the PR page in the review section.  Review apps are setup to create a admin user and example content.  Whenever frontend changes are made please include a before and after screenshot of the relevant areas and manually test that content creation works.

Doing this will mean your changes are highly likely to make it into the main repository and keep runtime errors out of production.  Once a PR is accepted it will be immediately deployed to the staging server and can have further manual testing done and/or evaulated by stakeholders.  If that is successful we can then promote those changes to the production server from the pipeline page in the heroku admin.

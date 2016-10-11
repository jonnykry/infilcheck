# se329-project2
TODO:  Write a pretty intro.

# Heroku Deployment


# Dev Set-up Instructions

MacOS Guide:

Env Set-up:
```
$ export FLASK_APP=app/server.py
$ export DATABASE_URL="postgresql://localhost/infilcheck_dev"
```

Local Database Set-up:
```
$ psql
# create database infilcheck_dev;
CREATE DATABASE
# \q

$ python app/manage.py db init
$ python app/manage.py db migrate
$ python app/manage.py db upgrade
```

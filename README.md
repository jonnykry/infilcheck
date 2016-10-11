# InfilcheckM8

InfilcheckM8 is a cheap and efficient home security product to notify you when your living quarters have been infiltrated.  The software is dependent upon a Raspberry Pi (TODO: version/link to Pi needed) and a PiCam(TODO:  version/link needed).  This repository offers software for:

- A web application (located in the `app` directory, sample [here](https://agile-lake-39375.herokuapp.com)) to manage any infiltrations or check on the status of your room.
- Live tracking (located in the `pi` directory) of a room for any activity

In addition, we've created a prototype for (TODO:  Greg) to physically track when the Raspberry Pi is recording, among other things.

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


Windows Guide:

Env Set-up:
```
$ set FLASK_APP=app/server.py
$ set DATABASE_URL=postgresql://postgres:@localhost/infilcheck_dev
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
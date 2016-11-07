# InfilcheckM8

InfilcheckM8 is a cheap and efficient home security product to notify you when your living quarters have been infiltrated.  The software is dependent upon a Raspberry Pi (TODO: version/link to Pi needed) and a PiCam(TODO:  version/link needed).  This repository offers software for:

- A web application (located in the `app` directory, sample [here](https://agile-lake-39375.herokuapp.com)) to manage any infiltrations or check on the status of your room.
- Live tracking (located in the `pi` directory) of a room for any activity

In addition, we've created a prototype for (TODO:  Greg) to physically track when the Raspberry Pi is recording, among other things.

# Dev Set-up Instructions

Local Database Set-up:
```
$ python
>>> from app import db
>>> db.create_all()
```

Set Environment Variables (optional:  store in  `.bash_vars` and `source` for working on this project):

```
export DATABASE_URL="postgres:///YOUR_DATABASE"
export FLASK_APP="YOUR_PATH_TO/app/app.py"
export FLASK_USERNAME="YOUR_USERNAME"
export FLASK_PASSWORD="YOUR_PASSWORD"
export FLASK_SECRET_KEY="YOUR_KEY"
export FLASK_DEBUG=1
export S3_HEAD_BUCKET="YOUR_AMAZON_S3_HEAD_BUCKET"
```

# Infilcheck

Infilcheck is a cheap and efficient home security product that notifies you when your living quarters have been infiltrated.  The software is dependent upon a Raspberry Pi (early models will be exponentially slower) and a PiCam [amazon link](https://www.amazon.com/gp/product/B00E1GGE40/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00E1GGE40&linkCode=as2&tag=trndingcom-20&linkId=XF5KMO3TGBUENU5T).  This repository offers software for:

- A web application (located in the `app` directory, to manage any infiltrations or check on the status of your room
- Live tracking (located in the `pi` directory) on a Raspberry Pi using a webcam

In addition, we created a prototype with GPIO to visually track when the Raspberry Pi is recording, when videos are sent, and the status of uploads.

# Installation Guide
The Infilcheck Installation guide comes in two parts.
  1. Complete the web Installation and configure the appropriate services.
  2. Install our software on a Raspberry Pi. This process is detailed for you below.
  
  
To follow our complete installation guide and learn more about our Heroku configurations please check out [INSTALL.md](INSTALL.md)

# Local Development Set-up

Create a new `virtualenv`, `activate` it and run:
```
$ pip install -r requirements.txt
```

* Install and run a [local PostgreSQL Database Server](https://www.postgresql.org/download/)
* Set local environment variables (optional:  store in  `.bash_vars` and `source` that file when working on this project):
```
export DATABASE_URL="postgres:///YOUR_DATABASE"
export FLASK_APP="YOUR_PATH_TO/app/app.py"
export FLASK_USERNAME="YOUR_USERNAME"
export FLASK_PASSWORD="YOUR_PASSWORD"
export FLASK_SECRET_KEY="YOUR_KEY"
export FLASK_DEBUG=1
export S3_HEAD_BUCKET="YOUR_AMAZON_S3_HEAD_BUCKET"
export TWILIO_ACCOUNT_SID="YOUR_TWILIO_ACCOUNT_SID"
export TWILIO_AUTH_TOKEN="YOUR_TWILIO_AUTH_TOKEN"
export TWILIO_CALLER_ID="YOUR_TWILIO_CALLER_ID"
export TWILIO_ALERTS="YOUR_TWILIO_ALERTS"
```

* Set up local AWS credentials for Boto 3 access (https://boto3.readthedocs.io/en/latest/guide/configuration.html)
* Generate an empty SQL database:
```
$ python
>>> from app import db
>>> db.create_all()
```

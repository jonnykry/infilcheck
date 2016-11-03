# Infilcheck

Infilcheck is a cheap and efficient home security product to notify you when your living quarters have been infiltrated.  The software is dependent upon a Raspberry Pi (TODO: version/link to Pi needed) and a PiCam(TODO:  version/link needed).  This repository offers software for:

- A web application (located in the `app` directory, sample [here](https://agile-lake-39375.herokuapp.com)) to manage any infiltrations or check on the status of your room.
- Live tracking (located in the `pi` directory) of a room for any activity

In addition, we've created a prototype for (TODO:  Greg) to physically track when the Raspberry Pi is recording, among other things.

#Installation Guide
To install Infilcheck you must sign up for a number of free services.
## Web Services
### Heroku
We will be using Heroku a cloud platform to host Infilcheck. The Heroku plan we will be using provides a postgres database and hosting for free.

Sign up for Heroku by following this link. [sign-up](https://signup.heroku.com)

After you have signed up you are ready to deploy Infilcheck by clicking the "Deploy to Heroku" button below. You will need to sign up for the following services to get text alerts when an intruder is detected and store video from your Pi.
### Twilio
Twilio is a texting service which will allow our application to alert you whenever there is an intruder.

Create an account with Twilio by following this link. [sign-up](https://www.twilio.com/try-twilio)

You can expect to follow these steps creating your account.

1. Verify that you are not a robot by entering your mobile phone number and inputting a code sent to the phone's number you entered.

2. Get your first Twilio number by following the tutorial.

  * Save this number for later and input it the "TWILIO_CALLER_ID" Config variable when deploying your Heroku application.

3. Completing the rest of the tutorial is not necessary, you may if you wish.

4. Select the pound sign on the far right side (looks like this #).

5. Select Verified Caller IDs.

  * Here you must add every phone number you wish to be able to be texted by your Heroku application. You should see the number you verified you humanity with already listed.

### Amazon Web Services




## Heroku Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jonnykry/infilcheck/)


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

Example `.bash_vars` Environment Variables:

```
export DATABASE_URL="postgres:///YOUR_DATABASE"
export FLASK_APP="YOUR_PATH_TO/app/app.py"
export FLASK_USERNAME="YOUR_USERNAME"
export FLASK_PASSWORD="YOUR_PASSWORD"
export FLASK_SECRET_KEY="YOUR_KEY"
export FLASK_DEBUG=1
export S3_HEAD_BUCKET="YOUR_AMAZON_S3_HEAD_BUCKET"
```


Windows Guide:

Env Set-up:
```
set FLASK_APP=app/server.py
set DATABASE_URL=postgresql://postgres:@localhost/infilcheck_dev
```

Local Database Set-up:
```
Open SQL Shell
Sign in with database password only
# create database infilcheck_dev;
CREATE DATABASE
# \q

$ python app/manage.py db init
$ python app/manage.py db migrate
$ python app/manage.py db upgrade
```

```
set DATABASE_URL=postgresql://postgres:@localhost/infilcheck_dev
set FLASK_APP=YOUR_PATH_TO/app/app.py
set FLASK_USERNAME=YOUR_USERNAME
set FLASK_PASSWORD=YOUR_PASSWORD
set FLASK_SECRET_KEY="YOUR_KEY"
set FLASK_DEBUG=1
set S3_HEAD_BUCKET=YOUR_AMAZON_S3_HEAD_BUCKET
```

# Infilcheck

Infilcheck is a cheap and efficient home security product to notify you when your living quarters have been infiltrated.  The software is dependent upon a Raspberry Pi (TODO: version/link to Pi needed) and a PiCam(TODO:  version/link needed).  This repository offers software for:

- A web application (located in the `app` directory, sample [here](https://agile-lake-39375.herokuapp.com)) to manage any infiltrations or check on the status of your room.
- Live tracking (located in the `pi` directory) of a room for any activity

In addition, we've created a prototype for (TODO:  Greg) to physically track when the Raspberry Pi is recording, among other things.

#Installation Guide
The Infilcheck Installation guide comes in two parts. First you must complete the web Installation and configure the appropriate services.
Second you must install our software on a Raspberry Pi. The process is detailed for you below.
## Web Installation
To install Infilcheck you must sign up for a number of free services
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

  * Save this number for later and input it as "TWILIO_CALLER_ID" Config variable when deploying your Heroku application.

3. Completing the rest of the Twilio tutorial is not necessary, you may if you wish.

4. Select the pound sign on the far right side (looks like this #).

5. Select Verified Caller IDs.

  * Here you must add every phone number you wish to be able to be texted by your Heroku application. You should see the number you verified you humanity with already listed.

### Amazon Web Services
TODO @jonnykry




## Heroku Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jonnykry/infilcheck/)

Click the above link to deploy the repository to your Heroku account.

You will be taken to a "Create New App" page where you will follow these steps to complete the InfilCheck deploy.

1. Enter in the first box the name of your App. This is totally optional but a cool name is completely necessary.

2. Runtime Selection - choose for the appropriate region you wish to run your InfilCheck deploy in.

3. Enter the following Config Variables

### Twilio Configurations

  1. **TWILIO_ACCOUNT_SID** (ACCOUNT SID) may be found under Account Summary at [https://www.twilio.com/user/account](https://www.twilio.com/user/account)

  2. **TWILIO_AUTH_TOKEN** (AUTH TOKEN) may be found below Account Summary. You will need to click on the eye icon to reveal the token.

  3. **TWILIO_CALLER_ID** is the active number you wish Twilio to send text alerts from and may be found here. [https://www.twilio.com/user/account/phone-numbers/incoming](https://www.twilio.com/user/account/phone-numbers/incoming)

  4. **TWILIO_ALERTS** Twilio is not a completely free service and if you do not wish to get text alerts to your phone enter 0, otherwise 1

### Amazon Web Services Configurations

  5. **AWS_ACCESS_KEY_ID** The Amazon webservice key found in your AWS dashboard found here [TODO PROVIDE LINK]()

  6. **AWS_SECRET_ACCESS_KEY** An Amazon webservice key found in your AWS dashboard found here [TODO PROVIDE LINK]()

  7. **S3_HEAD_BUCKET** The name of the bucket you created in S3 for all of your video files.

### Flask Configurations

  8. **FLASK_DEBUG** Set to 0 for no logged errors or 1. This is more of a development configuration if you have no clue set it to 1

  9. **FLASK_PASSWORD** to be removed in a future dev cycle keep as is

  10. **FLASK_SECRET_KEY** to be removed in a future dev cycle keep as is

  11. **FLASK_USERNAME**  to be removed in a future dev cycle keep as is

4. Click on the deploy button and you are off the races!

  * Once Heroku completes installing your application you may begin creating user accounts and logins.

  * Note* phone numbers must include country code to work with Twilio.

## Raspberry Pi InfilCheck Installation guide.
TODO @samjxn





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

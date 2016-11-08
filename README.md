# Infilcheck

Infilcheck is a cheap and efficient home security product that notifies you when your living quarters have been infiltrated.  The software is dependent upon a Raspberry Pi (early models will be exponentially slower) and a PiCam [amazon link]{https://www.amazon.com/gp/product/B00E1GGE40/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00E1GGE40&linkCode=as2&tag=trndingcom-20&linkId=XF5KMO3TGBUENU5T}.  This repository offers software for:

- A web application (located in the `app` directory, to manage any infiltrations or check on the status of your room
- Live tracking (located in the `pi` directory) on a Raspberry Pi using a webcam

In addition, we created a prototype for GPIO to physically track when the Raspberry Pi is recording, when videos are sent, and the status of uploads.

# Installation Guide
The Infilcheck Installation guide comes in two parts.
  1. Complete the web Installation and configure the appropriate services.
  2. Install our software on a Raspberry Pi. This process is detailed for you below.

## Web Installation
To install Infilcheck, you must sign up for a number of free services:

### Heroku
We use Heroku (a cloud platform) to host Infilcheck. The Heroku plan we use provides a PostgreSQL database and hosting for free.

[Sign Up for Heroku](https://signup.heroku.com).

After you have signed up and are ready to deploy Infilcheck, click the "Deploy to Heroku" button below.

### Twilio
Twilio is an SMS API/service which allows our application to alert you whenever there is an intruder.

[Sign Up for Twilio](https://www.twilio.com/try-twilio).

You can expect to follow these steps to create your account:
1. Verify that you are not a robot by entering your mobile phone number and inputting a code sent to the phone's number you entered.
2. Get your first Twilio number by following the tutorial.
  * Save this number for later and input it as "TWILIO_CALLER_ID" Config variable when deploying your Heroku application.
3. Completing the rest of the Twilio tutorial is not necessary, you may if you wish.
4. Select the pound sign on the far right side (looks like this #).
5. Select Verified Caller IDs.
  * Here you must add every phone number you wish to be able to be texted by your Heroku application. You should see the number you verified you humanity with already listed.

### Amazon Web Services
Amazon Web Services is used for S3 storage to store and serve the `.avi`/`.gif` files.

[Sign Up for AWS](https://aws.amazon.com/s3/).

Once you've signed up, you need to:

1. Authenticate your account using the Boto 3 credential configuration described [here](https://boto3.readthedocs.io/en/latest/guide/configuration.html)
2. Create a head bucket to store all of your gifs/videos and set desired permissions on the bucket for web application access (required for viewing on the web application)
3. Store the head bucket name as the `S3_HEAD_BUCKET` environment variable in Infilcheck

## Heroku Deploy [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jonnykry/infilcheck/)

Click the above "Deploy to Heroku" button to deploy the repository to your Heroku account.

You will be taken to a "Create New App" page where you will follow these steps to complete the InfilCheck deploy.

1. Enter in the first box the name of your App. This is totally optional but a cool name is completely necessary.
2. Runtime Selection - choose for the appropriate region you wish to run your InfilCheck deploy in.
3. Enter the following Config Variables:

### Twilio Configurations

  1. **TWILIO_ACCOUNT_SID** (ACCOUNT SID) may be found under Account Summary at [https://www.twilio.com/user/account](https://www.twilio.com/user/account)
  2. **TWILIO_AUTH_TOKEN** (AUTH TOKEN) may be found below Account Summary. You will need to click on the eye icon to reveal the token.
  3. **TWILIO_CALLER_ID** is the active number you wish Twilio to send text alerts from and may be found here. [https://www.twilio.com/user/account/phone-numbers/incoming](https://www.twilio.com/user/account/phone-numbers/incoming)
  4. **TWILIO_ALERTS** Twilio is not a completely free service and if you do not wish to get text alerts to your phone enter 0, otherwise 1

### Amazon Web Services Configurations

The following must be set from your [AWS Credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html):
  5. **AWS_ACCESS_KEY_ID** Your Access Key ID from your AWS Security Console
  6. **AWS_SECRET_ACCESS_KEY** Your Secret Access Key from your AWS Security Console
  7. **S3_HEAD_BUCKET** The name of the bucket you created in S3 for all of your video files

### Flask Configurations

  8. **FLASK_DEBUG** Set to 0 for no logged errors or 1. This is used for local development.
  9. **FLASK_PASSWORD** to be removed in a future dev cycle (keep default config value)
  10. **FLASK_SECRET_KEY** to be removed in a future dev cycle (keep default config value)
  11. **FLASK_USERNAME**  to be removed in a future dev cycle (keep default config value)

4. Click on the deploy button and you are off the races!
  * Once Heroku completes installing your application you may begin creating user accounts and logins.
  * Note: phone numbers must include country code to work with Twilio.

## Raspberry Pi
[source]{http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/}
The following steps are taken from a mixture of two tutorials by pyimagesearch found at the link. Depending on which version Raspberry Pi you own these steps may take up to 10 hrs to complete.

Make sure your Pi is up to date!
```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo rpi-update
```
Install Dev tools
```
$ sudo apt-get install build-essential cmake pkg-config
```
Install media packages
```
$ sudo apt-get install libjpeg8-dev libtiff4-dev libjasper-dev libpng12-dev
```
Required for highgui
```
sudo apt-get install libgtk2.0-dev
```
Video I/O packages
```
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
```
Optimization Libraries for OpenCV
```
$ sudo apt-get install libatlas-base-dev gfortran
```
Install pip
```
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py
```
Install  virtualenv  and virtualenvwrapper
```
$ sudo pip install virtualenv virtualenvwrapper
$ sudo rm -rf ~/.cache/pip
```
Update your bash ~/.profile by using your favorite text editor and adding the following lines.
```
# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```
Reload your ~./profile
```
$ source ~/.profile
```
create a virtual enviroment
```
$ mkvirtualenv cv
```
Install Python 2.7 development tools
```
$ sudo apt-get install python2.7-dev
```

Install Numpy
```
$ pip install numpy
```
Download OpenCV and upack it
* Note: If you get an error redownload OpenCV as sourceforge may have corrupted it
```
$ wget -O opencv-2.4.10.zip http://sourceforge.net/projects/opencvlibrary/files/opencv-unix/2.4.10/opencv-2.4.10.zip/download
$ unzip opencv-2.4.10.zip
$ cd opencv-2.4.10
```
Setup build
```
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_NEW_PYTHON_SUPPORT=ON -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON  -D BUILD_EXAMPLES=ON ..
```
Compile
* Note: If for any reason make fails or is interupted you may rerun the command and it will pick up where it left off
* Time: Raspberry Pi B+: ~9.5 hours     Raspberry Pi 2: ~3 hours
```
$ make
```
Install OpenCV
```
$ sudo make install
$ sudo ldconfig
```
Check that OpenCV is installed in 
```
/usr/local/lib/python2.7/site-packages
```
Setup OpenCV for work in our virtual enviroment
```
$ cd ~/.virtualenvs/cv/lib/python2.7/site-packages/
$ ln -s /usr/local/lib/python2.7/site-packages/cv2.so cv2.so
$ ln -s /usr/local/lib/python2.7/site-packages/cv.py cv.py
```

```
```

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

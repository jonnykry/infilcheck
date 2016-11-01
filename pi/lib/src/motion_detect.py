from picamera.array import PiRGBArray
from picamera import PiCamera

import json
import sys
import requests
import imutils
import datetime
import time
import cv2
import thread
import os
sys.path.insert(0, '../../gpio/')
from light_sensor import *
from led import *


PI_ID = ""

# Tracks the list of files to upload
TO_UPLOAD = []

# Tracks whether or not we are currently capturing a video
IS_CAPTURING = False

# The video writer
OUT = None

# The path of the file currently being captured
CURRENT_CAPTURE = None

# Whether or not to attempt to upload files
LOCAL = False

# Whether or not the app is in verbose mode
VERBOSE = False

SETTINGS = {};

## LED1 While recording
## LED2 While occupied
## LED3 While upload
## LED4 Wait for cam
## LED5 LOW Light

def log(msg, verbose_only=False):
    if (verbose_only and not VERBOSE):
        return
    
    with open("log.txt", "a") as myfile:
        info = str(datetime.datetime.now())[:-7] + " :: " + msg
        print info
        myfile.write(info +'\n')

def polling_thread():
    last_poll = datetime.datetime.now()
    while True:
        while (datetime.datetime.now() - last_poll).seconds < 3:
            pass
        last_poll = datetime.datetime.now()
        
        log("polling...", True)


        r = requests.get('https://agile-lake-39375.herokuapp.com/poll', data={'piid': PI_ID})
    
        if r.ok:
            log("polling response OK", True)
#           data = json.loads(r.text())
        else:
            log("polling response BAD", True)
        
        
def upload_thread():    
    while True:    
        while not TO_UPLOAD:
            pass
        blink_led3()
        filepath = TO_UPLOAD.pop(0)
        if not LOCAL:
            log("UPLOAD_STARTING:  " + filepath)
            try :
                r = requests.post('https://agile-lake-39375.herokuapp.com/upload',
                                  data={'piid': PI_ID}, files={filepath.split('\\')[-1]: open(filepath, 'rb')})        

                if r.ok:
                    os.remove(filepath)
                    log("UPLOAD DONE :  " + filepath)           
                    led4_off()
                    
                else:
                    log('POST failed')
                    log('INTERPRETED FILENAME:  ' + filepath.split('\\')[-1])
                    log('FILEPATH:  ' + filepath)
                    led4_off()
            except:
                led4_on()
            finally:
                blink_led3_stop()
        else:
            log("Not uploading " + filepath)
            time.sleep(3.0)
            blink_led3_stop()

def add_status_and_timestamps(frame, text, timestamp):
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Room: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    cv2.putText(frame, "Light:  {}".format(light_sense()), (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
    
def wait_for_cam(max):
    led4_on()
    time.sleep(max)
    led4_off()

def init_video_writer(fourcc):
    global IS_CAPTURING
    global OUT
    global CURRENT_CAPTURE
    
    path = './avi/'
    
    if not os.path.exists(path):
        os.makedirs(path)


    log('STARTING CAPTURE')
    filename = str(datetime.datetime.now()).replace(" ", "_").replace(":","_")[:-7] + ".avi"
    OUT = cv2.VideoWriter(path + filename, fourcc, 10.0, (500, 375))
    CURRENT_CAPTURE = path + filename
    IS_CAPTURING = True

    
def stop_recording():
    global IS_CAPTURING
    global OUT
    global CURRENT_CAPTURE
    
    log("DONE CAPTURING")
    IS_CAPTURING = False
    TO_UPLOAD.append(CURRENT_CAPTURE)
    CURRENT_CAPTURE = None
    OUT.release()
    OUT = None
    recordedFrames = 0


def read_settings_file():
    global SETTINGS

    try:
        with open('settings.json', 'r') as fp:
            SETTINGS = json.load(fp)
    except:
        return None

    needs_saving = False

    if not SETTINGS['room_name']:
        SETTINGS['room_name'] = "Room"
        needs_saving = True

    if not SETTINGS['capture_fr']:
        SETTINGS['capture_fr'] = 32
        needs_saving = True

    if not SETTINGS['threshold_frame_count']:
        SETTINGS['threshold_frame_count'] = 5
        needs_saving = True

    if not SETTINGS['output_fr']:
        SETTINGS['output_fr'] = 10,
        needs_saving = True
        
    if (not SETTINGS['pi_id']) and (not sys.environ['PI_ID']):
        print "Pi ID must either be set as 'pi_id' in settings.json or as PI_ID env var"
        return None

    return SETTINGS
    
def main():
    global TO_UPLOAD

    global OUT
    global CURRENT_CAPTURE
    global LOCAL
    
    global PI_ID
    
    if not read_settings_file():
        print("Error loading settings file")
        return 1


    if SETTINGS['pi_id']:
        PI_ID = SETTINGS['pi_id']
    else:
        PI_ID = os.environ['PI_ID']
        
    WINDOWED = '-w' in sys.argv
    LOCAL = '--local' in sys.argv
    VERBOSE = '-v' in sys.argv
    
    # The video codec for cv2's VideoWriter
    FOURCC = cv2.VideoWriter_fourcc(*'MJPG')
    
    # TODO:  move to conf file
    CAPTURE_RESOLUTION = (640, 480)

    cam = PiCamera()
    cam.resolution = CAPTURE_RESOLUTION
    cam.framerate = 32

    rawCapture = PiRGBArray(cam, size=CAPTURE_RESOLUTION)

    # wait for camera to warm up
    wait_for_cam(2.0)

    avg = None
    lastUploaded = datetime.datetime.now()
    motionCounter = 0

    recordedFrames = 0

    thread.start_new_thread(upload_thread, ())

    if not LOCAL:
        thread.start_new_thread(polling_thread, ())
    
    occupied = False
    text = ""

    log("UP AND RUNNING")
    for f in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        led1_on() 
        frame = f.array
        timestamp = datetime.datetime.now()
        occupied = False
        text = "Unoccupied"

        #resize / convert the frame to grayscale
        frame = imutils.resize(frame, width=500)
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #apply gaussian blur
        grayscale_frame = cv2.GaussianBlur(grayscale_frame, (21, 21), 0)

        # if this is the first capture, we have to init average
        if avg is None:
            avg = grayscale_frame.copy().astype("float")
            rawCapture.truncate(0)
            continue

        # accumulate weighted average between current frame and previous frames
        cv2.accumulateWeighted(grayscale_frame, avg, 0.83)
        frameDelta = cv2.absdiff(grayscale_frame, cv2.convertScaleAbs(avg))

        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, 2, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (__, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) >= 500:
                occupied = True
                break
            
        text = "Occupied" if occupied else "Unoccupied"

        add_status_and_timestamps(frame, text, timestamp)
        
        if occupied:
            led2_on()  
            motionCounter += 1

            # wait for X frames of motion to be sure
            if motionCounter > 5 and OUT is None :               
                init_video_writer(FOURCC)


            if IS_CAPTURING and OUT is not None and recordedFrames < 300:
                recordedFrames += 1                         
                OUT.write(frame)

            elif IS_CAPTURING and OUT and recordedFrames >= 300:
                recordedFrames = 0
                stop_recording()
                led2_off()
                       
        else:
            led2_off()
            motionCounter = 0

            if IS_CAPTURING:
                recordedFrames = 0
                stop_recording()

            if WINDOWED:
                cv2.imshow("Feed", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

        rawCapture.truncate(0)

    return



if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


from picamera.array import PiRGBArray
from picamera import PiCamera



import sys
import requests
import imutils
import datetime
import time
import cv2
import thread
import os
sys.path.insert(0, '../gpio/')
from led import *


PI_ID = 'e51b6577-85ca-4360-bcef-0c83452e24f2'

# Tracks the list of files to upload
TO_UPLOAD = []

# Tracks whether or not we are currently capturing a video
IS_CAPTURING = False

# The video writer
OUT = None

# The path of the file currently being captured
CURRENT_CAPTURE = None

# List of strings to print when exiting normally
LOG = []


def upload_thread():
    
    while True:
        while not TO_UPLOAD:
            pass
        filepath = TO_UPLOAD.pop(0)
        print("UPLOAD STARTING:  " + filepath)
        LOG.append("UPLOAD_STARTING:  " + filepath)
        
        r = requests.post('https://agile-lake-39375.herokuapp.com/upload', data={'piid': PI_ID}, files={filepath.split('\\')[-1]: open(filepath, 'rb')})        

        if r.ok:
            os.remove(filepath)
            print("UPLOAD DONE :  " + filepath)
            LOG.append("UPLOAD DONE :  " + filepath)

        else:
            print 'POST failed'
            print 'INTERPRETED FILENAME:  ' + filepath.split('\\')[-1]
            print 'FILEPATH:  ' + filepath

            
def add_status_and_timestamps(frame, text, timestamp):
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Room: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    
def wait_for_cam(max):
    ## TODO:  smart polling so we don't have to wait the whole time
    time.sleep(max)


def init_video_writer(fourcc):
    global IS_CAPTURING
    global OUT
    global CURRENT_CAPTURE
    
    path = "./" # TODO:  SET DYNAMICALLY
    filename = str(datetime.datetime.now()).replace(" ", "_").replace(":","_")[:-7] + ".avi"
    OUT = cv2.VideoWriter(path + filename, fourcc, 10.0, (500, 375))
    CURRENT_CAPTURE = path + filename
    IS_CAPTURING = True

    
def stop_recording():
    global IS_CAPTURING
    global OUT
    global CURRENT_CAPTURE
    
    print "DONE CAPTURING"
    IS_CAPTURING = False
    TO_UPLOAD.append(CURRENT_CAPTURE)
    CURRENT_CAPTURE = None
    OUT.release()
    OUT = None
    recordedFrames = 0


def main():
    global TO_UPLOAD
    global IS_CAPTURING
    global OUT
    global CURRENT_CAPTURE

    # The video codec for cv2's VideoWriter
    FOURCC = cv2.VideoWriter_fourcc(*'MJPG')
    
    # TODO:  move to conf file
    CAPTURE_RESOLUTION = (640, 480)

    cam = PiCamera()
    cam.resolution = CAPTURE_RESOLUTION
    cam.framerate = 32

    rawCapture = PiRGBArray(cam, size=CAPTURE_RESOLUTION)

    # wait for camera to warm up
    wait_for_cam(0.1)

    avg = None
    lastUploaded = datetime.datetime.now()
    motionCounter = 0

    recordedFrames = 0

    thread.start_new_thread(upload_thread, ())

    occupied = False
    text = ""
    
    for f in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
 
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
            blink_led5()
            motionCounter += 1

            # wait for X frames of motion to be sure
            if motionCounter > 5 and OUT is None :
                blink_led4()
                print "STARTING CAPTURE"
                IS_CAPTURING = True
                init_video_writer(FOURCC)


            if IS_CAPTURING and OUT is not None and recordedFrames < 300:
                recordedFrames += 1
                print "WRITING FRAME " + str(recordedFrames)            
                OUT.write(frame)

            elif IS_CAPTURING and OUT and recordedFrames >= 300:
                recordedFrames = 0
                stop_recording()
                       
        else:
            motionCounter = 0

            if IS_CAPTURING:
                recordedFrames = 0
                stop_recording()

        cv2.imshow("Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print "To upload:  " + str(TO_UPLOAD)
            print ""
            print ""
            print "LOG:"
            for l in LOG:
                print l
            
            break

        rawCapture.truncate(0)
        
    return



if __name__ == '__main__':
    main()

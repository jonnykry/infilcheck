from picamera.array import PiRGBArray
from picamera import PiCamera

import sys
import imutils
import datetime
import time
import cv2

DEBUG = 0



"""

THE FOLLOWING METHOD resize IS FROM jrosebr1's IMUTILS PACKAGE

THE CODE CAN BE FOUND HERE:
https://github.com/jrosebr1/imutils/blob/f28d4cd5e14910fa283f67db47e1a721b660fdfd/imutils/convenience.py

"""

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    
    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)
    
    # return the resized image
    return resized


def add_status_and_timestamps(frame, text, timestamp):
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Room: {}".format(text), (10, 20), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_PLAIN, 0.35, (0, 0, 255), 1)

    
def debug_print(msg):
    if DEBUG:
        print(msg)

        
def parse_args(argv):

    video = None
    area = 500

    global DEBUG

    if '-d' in argv:
        DEBUG = 1

    if '-ns' in argv:
        NOSCREEN = 1
    
    if '-v' in argv:
        idx = argv.index('-v')
        if idx + 1 != len(argv):
            debug_print("Setting FILE to {}".format(argv[idx + 1]))
            video = argv[idx + 1]
    if '-a' in argv:
        idx = argv.index('-a')
        if idx + 1 != len(argv):
            debug_print("Setting AREA to {}".format(argv[idx + 1]))
            area = int(argv[idx + 1])

    return {'vid': video, 'area': area}


def wait_for_cam(max):
    ## TODO:  smart polling so we don't have to wait the whole time
    time.sleep(max)

def main():

    IS_CAPTURING = 0
    CAPTURED = 0
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output.avi',fourcc, 1.0, (500, 375))

    
    
    args = parse_args(sys.argv)

    # TODO:  move to conf file
    CAPTURE_RESOLUTION = (640, 480)

    cam = PiCamera()
    cam.resolution = CAPTURE_RESOLUTION
    cam.framerate = 32

    rawCapture = PiRGBArray(cam, size=CAPTURE_RESOLUTION)

    # wait for camera to warm up
    time.sleep(0.1)

    avg = None
    lastUploaded = datetime.datetime.now()
    motionCounter = 0

    for f in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        frame = f.array
        timestamp = datetime.datetime.now()
        text = "Unoccupied"

        #resize / convert the frame to grayscale
        frame = resize(frame, width=500)
        print frame.shape[:2]
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
        thresh = cv2.dilate(thresh, None, iterations=6)
        (__, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            if cv2.contourArea(c) < 500:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"


        if text == "Occupied":
            motionCounter += 1
            if motionCounter > 10 and not CAPTURED:
                print "STARTING CAPTURE, FOOLS"
                CAPTURED = 1
                IS_CAPTURING = 1
                print "Is open:  {}".format(out.isOpened())
            if IS_CAPTURING:
                print "WRITING."
                out.write(frame)

                       
        else:
            motionCounter = 0
            if IS_CAPTURING:
                print "DONE CAPTURING, FOOLS"
                IS_CAPTURING = 0
                out.release()
                

        add_status_and_timestamps(frame, text, timestamp)
            
        cv2.imshow("Feed", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        rawCapture.truncate(0)
        
    return



if __name__ == '__main__':
    main()

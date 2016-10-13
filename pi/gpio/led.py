import RPi.GPIO as GPIO ## Import GPIO library
import time		## Import Time Library for sleep
import thread		## Import Thread for blinking
from multiprocessing import Process
import os


## Debug Mode
if __debug__:
        print 'Debug ON'
        GPIO.setwarnings(False)

else:
        print 'Debug OFF'
        GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
## Variable LED for PIN
global LED1
global LED2
global LED3
global LED4
global LED5

LED1 = 11
LED2 = 13
LED3 = 15
LED4 = 12
LED5 = 16

## Bool variables for blink continous func
   
global blink_led1
global blink_led2
global blink_led3
global blink_led4
global blink_led5

## Blink Speed
blink_speed = 0.5

## Setup LEDs
GPIO.setup(LED1, GPIO.OUT) ## Setup GPIO Pin 11 to OUT
GPIO.setup(LED2, GPIO.OUT) ## Setup GPIO Pin 13 to OUT
GPIO.setup(LED3, GPIO.OUT) ## Setup GPIO Pin 15 to OUT
GPIO.setup(LED4, GPIO.OUT) ## Setup GPIO Pin 12 to OUT
GPIO.setup(LED5, GPIO.OUT) ## Setup GPIO Pin 16 to OUT


## Turn LED 1-5 on
def led_1_on():
	GPIO.output(LED1,True) ## Turn on GPIO pin 11 

def led_2_on():
	GPIO.output(LED2,True) ## Turn on GPIO pin 13 

def led_3_on():
	GPIO.output(LED3,True) ## Turn on GPIO pin 15 

def led_4_on():
	GPIO.output(LED4,True) ## Turn on GPIO pin 12 

def led_5_on():
	GPIO.output(LED5,True) ## Turn on GPIO pin 16 

## Turn LED 1-5 off
def led_1_off():
        GPIO.output(LED1,False) ## Turn off GPIO pin 11 

def led_2_off():
	GPIO.output(LED2,False) ## Turn off GPIO pin 13 

def led_3_off():
        GPIO.output(LED3,False) ## Turn off GPIO pin 15 

def led_4_off():
	GPIO.output(LED4,False) ## Turn off GPIO pin 12

def led_5_off():
	GPIO.output(LED5,False) ## Turn off GPIO pin 16

## Blink LED 1-5
def Blink(numTimes,speed,LED_NUM):
	for i in range(0,numTimes):## Run loop numTimes
		GPIO.output(LED_NUM,True)## Switch on LED_Num
		time.sleep(speed)## Wait
		GPIO.output(LED_NUM,False)## Switch off LED_NUM
		time.sleep(speed)## Wait

def blink_thread(numTimes, speed, LED_NUM):
	try:
		thread.start_new_thread(Blink,(numTimes, speed,LED_NUM))
	except:
		print "Error: unable to start thread"

def blink_led1_start():
	while(1):
		GPIO.output(LED1,True)## Switch on LED_NUM
        time.sleep(blink_speed)## Wait
        GPIO.output(LED1,False)## Switch off LED_NUM
        time.sleep(blink_speed)## Wait

def blink_led1_start_process():
	global blink_led1
	blink_led1 = Process(target=blink_led1_start, args=())
	blink_led1.start()

def blink_led1_stop_process():
	global blink_led1
	blink_led1.terminate()

def blink_led2_start():
	while(1):
		GPIO.output(LED2,True)## Switch on LED_NUM
        time.sleep(blink_speed)## Wait
        GPIO.output(LED2,False)## Switch off LED_NUM
        time.sleep(blink_speed)## Wait

def blink_led2_start_process():
	global blink_led2
	blink_led2 = Process(target=blink_led2_start, args=())
	blink_led2.start()

def blink_led2_stop_process():
	global blink_led2
	blink_led2.terminate()

def blink_led3_start():
	while(1):
		GPIO.output(LED3,True)## Switch on LED_NUM
        time.sleep(blink_speed)## Wait
        GPIO.output(LED3,False)## Switch off LED_NUM
        time.sleep(blink_speed)## Wait

def blink_led3_start_process():
	global blink_led3
	blink_led3 = Process(target=blink_led3_start, args=())
	blink_led3.start()

def blink_led3_stop_process():
	global blink_led3
	blink_led3.terminate()

def blink_led4_start():
	while(1):
		GPIO.output(LED4,True)## Switch on LED_NUM
        time.sleep(blink_speed)## Wait
        GPIO.output(LED4,False)## Switch off LED_NUM
        time.sleep(blink_speed)## Wait

def blink_led4_start_process():
	global blink_led4
	blink_led4 = Process(target=blink_led4_start, args=())
	blink_led4.start()

def blink_led4_stop_process():
	global blink_led4
	blink_led4.terminate()

def blink_led5_start():
	while(1):
		GPIO.output(LED5,True)## Switch on LED_NUM
        time.sleep(blink_speed)## Wait
        GPIO.output(LED5,False)## Switch off LED_NUM
        time.sleep(blink_speed)## Wait

def blink_led5_start_process():
	global blink_led5
	blink_led5 = Process(target=blink_led5_start, args=())
	blink_led5.start()

def blink_led5_stop_process():
	global blink_led5
	blink_led5.terminate()

## Cleanup
def cleanup_gpio():
	    GPIO.cleanup()


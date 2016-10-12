import RPi.GPIO as GPIO ## Import GPIO library
import time		## Import Time Library for sleep
import thread		## Import Thread for blinking


## Debug Mode
if __debug__:
        print 'Debug ON'
        GPIO.setwarnings(True)

else:
        print 'Debug OFF'
        GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
## Variable LED for PIN
LED1 = 11
LED2 = 13
LED3 = 15
LED4 = 12
LED5 = 16

## Bool variables for blink continous func
global blink_led1
blink_led1 = False
blink_led2 = False
blink_led3 = False
blink_led4 = False
blink_led5 = False

## Blink Speed
blink_speed = 0.05

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
	blink_led1 = True 
	while(blink_led1):
		GPIO.output(LED1,True)## Switch on LED_NUM
                time.sleep(blink_speed)## Wait
                GPIO.output(LED1,False)## Switch off LED_NUM
                time.sleep(blink_speed)## Wait

def blink_led1_start_thread():
	try:
                thread.start_new_thread(blink_led1_start,())
	except:
                print "Error: unable to start thread"

def blink_led1_stop():
	blink_led1 = False



#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from led import *


GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 7

def light_sense():
    
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    if (count > 2000):
        led5_on()
        return "Dark"
    else:
        led5_off()
        return "Light"




def cleanup():
    GPIO.cleanup()

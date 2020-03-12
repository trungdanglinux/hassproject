#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from lcd import lcd_i2c

#Define the port for sensor and devices
MOTION_SENSOR = 14
SMOKE_SENSOR = 17
FLAME_SENSOR = 15
DHT11 = 4
LED1 = 18
RELAY = 27

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR,GPIO.IN)
GPIO.setup(SMOKE_SENSOR,GPIO.IN)
GPIO.setup(FLAME_SENSOR,GPIO.IN)
GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(RELAY,GPIO.IN)

workingStove = GPIO.input(RELAY)
smoke = GPIO.input(SMOKE_SENSOR)
flame = GPIO.input(FLAME_SENSOR)
motion = GPIO.input(MOTION_SENSOR)
light = GPIO.output(LED1)
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11)

def offStove():
    while workingStove:
        if motion == False:
            if smoke == False or flame == True: #smoke is off when it's deteced 
                GPIO.output(RELAY,GPIO.LOW)
                print("The stove is off due to burning")
        else:
            if flame == True:
                GPIO.output(RELAY,GPIO.LOW)
                print("Stove is off due to flame!")
        if temperature >= 50: 
            GPIO.output(RELAY,GPIO.LOW)
            print("The stove is off due to leaving a stove on when not using!")
            print("The temperature at the moment is %{0:0,1f}*C".format(temperature))
    else:
        if smoke == False or flame == True: #smoke is off when it's deteced 
            GPIO.output(RELAY,GPIO.LOW)
            print("Stove is off!")        

def kitchenLight():
    if motion == False and light == True :
        time.sleep(90)
        GPIO.output(LED1,GPIO.LOW)
        print("The light is off!")
    elif motion == True and light == False :
        GPIO.output(LED1,GPIO.HIGH)
        print("the light is on!")

try:
    offStove()
    kitchenLight()
    lcd_i2c.lcd_string('Temp={0:0.1f}*C'.format(temperature),LCD_LINE_1)
    lcd_i2c.lcd_string('Humidity={0:0.1f}%'.format(humidity),LCD_LINE_2)
except:
    print("There is somethig wrong!")
    
        



    


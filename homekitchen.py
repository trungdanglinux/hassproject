#!/usr/bin/python
import sys
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
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR,GPIO.IN)
GPIO.setup(SMOKE_SENSOR,GPIO.IN)
GPIO.setup(FLAME_SENSOR,GPIO.IN)
GPIO.setup(LED1,GPIO.OUT, initial = 0)
GPIO.setup(RELAY,GPIO.OUT, initial =0)


humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11)

high = GPIO.HIGH
low = GPIO.LOW
def tem():
  if temperature >= 60: 
      GPIO.output(RELAY,HIGH)
      print("The stove is off due to leaving a stove on when not using!")
      print("The temperature at the moment is %{0:0.1f}*C".format(temperature))

def offStove():

    while GPIO.input(RELAY) == high:
        tem()
        if GPIO.input(MOTION_SENSOR) == low:
            if GPIO.input(SMOKE_SENSOR) == low or GPIO.input(FLAME_SENSOR) == low: #smoke sensor and flame are off when it's deteced 
                GPIO.output(RELAY,low)
                print("The stove is off due to burning")
        else:
            if GPIO.input(FLAME_SENSOR) == low:
                GPIO.output(RELAY,low)
                print("Stove is off due to flame!")
    else:
        if GPIO.input(SMOKE_SENSOR) == low or GPIO.input(FLAME_SENSOR) == low:
            GPIO.output(RELAY,low)
            print("Stove is off!")
def kitchenLight():
    while GPIO.input(MOTION_SENSOR) == low :
         if GPIO.input(LED1) == high :
            time.sleep(20)
            print("The light is off!")
            GPIO.output(LED1,low)
    else:
        if GPIO.input(MOTION_SENSOR) == high and GPIO.input(LED1) == low:
            print("the light is on!")
            GPIO.output(LED1,high)

try:
   while True:  
     offStove()
     kitchenLight()
  lcd_i2c.lcd_string('Temp={0:0.1f}*C'.format(temperature),LCD_LINE_1)
  lcd_i2c.lcd_string('Humidity={0:0.1f}%'.format(humidity),LCD_LINE_2)
except KeyboardInterrupt:
  print("The program stopped!")


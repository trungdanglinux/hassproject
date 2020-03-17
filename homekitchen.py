#!/usr/bin/python
import sys
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import picamera
from datetime import datetime
from lcd import lcd_i2c

#Define the port for sensor and devices
MOTION_SENSOR = 14
SMOKE_SENSOR = 17
FLAME_SENSOR = 15
DHT11 = 4
LED1 = 18
RELAY = 27
BUZZER= 22
camera = picamera.PiCamera()

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR,GPIO.IN)
GPIO.setup(SMOKE_SENSOR,GPIO.IN)
GPIO.setup(FLAME_SENSOR,GPIO.IN)
GPIO.setup(LED1,GPIO.OUT, initial = 0)
GPIO.setup(RELAY,GPIO.OUT, initial =0)
GPIO.setup(BUZZER,GPIO.OUT, initial = 0)

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11)

high = GPIO.HIGH
low = GPIO.LOW
#take a photo of stove to check the state of kitchen  
def capture():
    GPIO.output(LED1,high) #turn on the light to have a clear photo
    time.sleep(1)
    now = datetime.now() 
    filename = now.strftime("%d-%m-%Y-%H-%M-%S")
    camera.resolution = (800,600)
    camera.capture("/home/pi/Documents/kitchen/{}.jpg".format(filename))
    GPIO.output(LED1,low)
#turn off the stove in case of leaving working stove while not using it
def tem(): 
  if temperature >= 60: 
      GPIO.output(RELAY,low)
      capture()
      print("The stove is off due to leaving a stove on when not using!")
      print("The temperature at the moment is %{0:0.1f}*C".format(temperature))
#making an alarm
def buzz():
    GPIO.output(BUZZER,high)
    time.sleep(20)
    GPIO.output(BUZZER,low)

def offStove():
    while GPIO.input(RELAY) == high:
        tem()  
        if GPIO.input(MOTION_SENSOR) == low:
            if GPIO.input(SMOKE_SENSOR) == low or GPIO.input(FLAME_SENSOR) == low: #smoke sensor and flame are off when it's deteced 
                GPIO.output(RELAY,low)
                capture()
                print("The stove is off due to burning")
                buzz()
        else:
            if GPIO.input(FLAME_SENSOR) == low:
                GPIO.output(RELAY,low)
                capture()
                print("Stove is off due to flame!")
                buzz()
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



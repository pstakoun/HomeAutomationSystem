import RPi.GPIO as GPIO
import thread
import picamera
import os, os.path
import time
import datetime
import tzlocal

OFF_LED_PIN = 12
ON_LED_PIN = 11
SENSOR_PIN = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(OFF_LED_PIN, GPIO.OUT)
GPIO.setup(ON_LED_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN)
GPIO.output(OFF_LED_PIN, True)
GPIO.output(ON_LED_PIN, False)

running = False

captures = []

def updateCaptures():
    global captures
    captures = sorted(os.listdir('/home/pi/HSS-captures'))

updateCaptures()

def detectMotion():
    motionDetected = False
    time.sleep(10)
    while running:
        time.sleep(0.5)
        current = GPIO.input(SENSOR_PIN)
        if current and not motionDetected:
            print("Motion detected")
            motionDetected = True
            loc = tzlocal.get_localzone().localize(datetime.datetime.now()).strftime("/home/pi/HSS-captures/%Y%m%d%H%M%S")
            with picamera.PiCamera(resolution=(640,360)) as camera:
                for i in range(3):
                    camera.capture(loc+str(i)+'.jpg')
                    time.sleep(1)
            updateCaptures()
            print("Images captured")
        elif motionDetected and not current:
            print("Motion no longer detected")
            motionDetected = False
            time.sleep(10)

def start():
    if not running:
        global running
        running = True
        GPIO.output(OFF_LED_PIN, False)
        GPIO.output(ON_LED_PIN, True)
        print("Starting motion detection")
        thread.start_new_thread(detectMotion, ())

def stop():
    if running:
        global running
        running = False
        GPIO.output(OFF_LED_PIN, True)
        GPIO.output(ON_LED_PIN, False)

def isRunning():
    return running

def countCaptures():
    updateCaptures()
    return len(captures)

def getCapture(n):
    return captures[n]

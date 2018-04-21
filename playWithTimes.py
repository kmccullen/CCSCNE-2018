import vlc
import Adafruit_PCA9685
import time
import random
import sys

#
# For the keyfob
#
import RPi.GPIO as GPIO

#
# For the sounds
#
import subprocess

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Set BOARD as number scheme
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

# Assign GPIO pins to Keyfob buttons
D0 = 5
D1 = 6
D2 = 13
D3 = 19
D4 = 26
D5 = 21
D6 = 20
D7 = 16

# Configure GPIO pins as input with pull down register enabled
GPIO.setup(D0, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(D1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(D2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(D3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(D4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(D5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(D6, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(D7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

pwm.set_pwm_freq(60)

def playSoundClip(clip):
    v = vlc.Instance()
    player = v.media_player_new()
    media = v.media_new(clip)
    media.parse()
    duration = media.get_duration() / 1500.0
    player.set_media(media)
    player.play()
    time.sleep(duration + 1.5)
    
def moveServoRange(rate, start, stop, servo):
    midPoint = int((start + stop)/2)
    for i in range(midPoint, stop):
       servoVal  = stop + i*2
       pwm.set_pwm(servo, 0, servoVal)
       time.sleep(rate)
    for i in range(stop, start, -1):
       servoVal  = stop + i*2
       pwm.set_pwm(servo, 0, servoVal)
       time.sleep(rate)
    for i in range(start, midPoint):
       servoVal  = stop + i*2
       pwm.set_pwm(servo, 0, servoVal)
       time.sleep(rate)

def movePair(rate, start1, stop1, servo1, start2, stop2, servo2):
    oneRange = stop1 - start1
    twoRange = stop2 - start2
    rangeRatio = float(oneRange) / float(twoRange)
    maxRange = max(oneRange, twoRange)
    if oneRange < 0:
        inc = -1
    else:
        inc = 1
    print(oneRange, twoRange, rangeRatio, inc)
    if maxRange == oneRange:
       for i in range(start1, stop1, inc):
          servo1Val = stop1 + i*2
          servo2Val = stop2 + int(i*2 / rangeRatio)
          pwm.set_pwm(servo1, 0, servo1Val)
          pwm.set_pwm(servo2, 0, servo2Val)
          time.sleep(rate)
    else:
       for i in range(start2, stop2, inc):
          servo2Val = stop2 + i*2
          servo1Val = stop1 + int(i*2 / rangeRatio)
          pwm.set_pwm(servo1, 0, servo1Val)
          pwm.set_pwm(servo2, 0, servo2Val)
          time.sleep(rate)

def moveServo(rate):
    servoZeroLow = 50
    servoZeroHigh = 225
    servoZeroMid = 150
    servoOneMid = 150
    servoOneLow = -50
    servoOneHigh = 250
    for i in range(servoOneMid, servoOneHigh):
       servoOne  = 150 + i*2
       pwm.set_pwm(1, 0, servoOne)
       time.sleep(rate)
    for i in range(servoZeroLow, servoZeroMid):
       servoZero = 150 + i*2
       pwm.set_pwm(0, 0, servoZero)
       time.sleep(rate)
    for i in range(servoZeroMid, servoZeroLow, -1):
       servoZero = 150 + i*2
       pwm.set_pwm(0, 0, servoZero)
       time.sleep(rate)
    for i in range(servoOneHigh, servoOneLow, -1):
       servoOne  = 150 + i*2
       pwm.set_pwm(1, 0, servoOne)
       time.sleep(rate)
    for i in range(servoZeroLow, servoZeroMid):
       servoZero = 150 + i*2
       pwm.set_pwm(0, 0, servoZero)
       time.sleep(rate)
    for i in range(servoZeroMid, servoZeroLow, -1):
       servoZero = 150 + i*2
       pwm.set_pwm(0, 0, servoZero)
       time.sleep(rate)
    for i in range(servoOneLow, servoOneMid):
       servoOne  = 150 + i*2
       pwm.set_pwm(1, 0, servoOne)
       time.sleep(rate)

#moveServoRange(0.02, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
#movePair(0.02, 150, 225, 1, 75, 160, 0)
#movePair(0.02, 225, -25, 1, 160, 75, 0)
#exit()

# Create callback function for GPIO pin 21
def button0(channel):
	print("Button 1 pressed! 0.005")
#	playSoundClip("/home/pi/Audio/Slitherine.mp3")
	moveServo(0.005)

# Create callback function for GPIO pin 22
def button1(channel):
	print("Button 2 pressed! 0.01")
#	playSoundClip("/home/pi/Audio/Hufflepuff.mp3")
	moveServo(0.01)

# Create callback function for GPIO pin 23
def button2(channel):
	print("Button 3 pressed! 0.02")
#	playSoundClip("/home/pi/Audio/Ravenclaw.mp3")
	moveServo(0.02)

# Create callback function for GPIO pin 24
def button3(channel):
	print("Button 4 pressed! 0.05")
#	playSoundClip("/home/pi/Audio/GriffindorII.mp3")
	moveServo(0.05)

# Create callback function for GPIO pin 25
def button4(channel):
	print("Button 5 pressed! 0.10")
	moveServo(0.1)

# Create callback function for GPIO pin 29
def button5(channel):
	print("Button 6 pressed!")
	
# Create callback function for GPIO pin 28
def button6(channel):
	print("Button 7 pressed!")

# Create callback function for GPIO pin 27
def button7(channel):
	print("Button 8 pressed!")

# Create event listeners for Respective GPIO pins
# No edge detection for 300 ms, with bouncetime = 300 ms
GPIO.add_event_detect(D0, GPIO.RISING, callback = button0, bouncetime = 300)
GPIO.add_event_detect(D1, GPIO.RISING, callback = button1, bouncetime = 300)
GPIO.add_event_detect(D2, GPIO.RISING, callback = button2, bouncetime = 300)
GPIO.add_event_detect(D3, GPIO.RISING, callback = button3, bouncetime = 300)
GPIO.add_event_detect(D4, GPIO.RISING, callback = button4, bouncetime = 300)
GPIO.add_event_detect(D5, GPIO.RISING, callback = button5, bouncetime = 300)
GPIO.add_event_detect(D6, GPIO.RISING, callback = button6, bouncetime = 300)
GPIO.add_event_detect(D7, GPIO.RISING, callback = button7, bouncetime = 300)

#playSoundClip("/home/pi/Downloads/TimeToStart.wav")

while True :
	try :
		time.sleep(0.5)
	except KeyboardInterrupt :	
		# Clean up GPIO on CTRL+C exit
		GPIO.cleanup()

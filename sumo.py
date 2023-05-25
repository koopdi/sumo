"""
This program uses the Sparkfun TB6612FNG motor driver
and the TCRT5000 line sensing module.
A two wheeled vehicle with differential drive is
controlled to stay within a white border.
"""

from machine import Pin , PWM
from utime import sleep
from utime import sleep_ms
from sys import exit

# The led on the pico-w board.
led = Pin("LED", Pin.OUT)

# The led on the pico-classic board.
# led = Pin(25, Pin.OUT)

# the start match button
btn_start = Pin(1, Pin.IN, Pin.PULL_UP)

# motor a control pins
ina1 = Pin(18, Pin.OUT)
ina2 = Pin(17, Pin.OUT)

# motor b control pins
inb1 = Pin(19, Pin.OUT)
inb2 = Pin(20, Pin.OUT)

# speed control pins
pwma = PWM(Pin(16)) # motor a
pwmb = PWM(Pin(21)) # motor b

# set pwm frequency
pwma.freq(10000)
pwmb.freq(10000)

# infrared line sensor
ir = Pin(22, Pin.IN)

# duty sets the speed, duty = 0 ~ 100%
# motor = 'a' or 'b'
def RotateCW(duty, motor):
    duty_16 = int((duty*65536)/100)
    if motor == 'a':        
        ina1.value(1)
        ina2.value(0)
        pwma.duty_u16(duty_16)
    elif motor == 'b':
        inb1.value(0)
        inb2.value(1)
        pwmb.duty_u16(duty_16)

def RotateCCW(duty, motor):
    duty_16 = int((duty*65536)/100)
    if motor == 'a':        
        ina1.value(0)
        ina2.value(1)
        pwma.duty_u16(duty_16)
    elif motor == 'b':
        inb1.value(1)
        inb2.value(0)
        pwmb.duty_u16(duty_16)

# basic control functions
def StopMotor(motor):
    if motor == 'a':
        ina1.value(0)
        ina2.value(0)
        pwma.duty_u16(0)
    elif motor == 'b':
        inb1.value(0)
        inb2.value(0)
        pwmb.duty_u16(0)

# duration doesn't do anything yet
def forward(duty, duration = -1):
    RotateCW(duty, 'a')
    RotateCW(duty, 'b')
    
def reverse(duty, duration = -1):
    RotateCCW(duty, 'a')
    RotateCCW(duty, 'b')
    
def stop():
    StopMotor('a')
    StopMotor('b')

# it only turns left for now
def turn(duty = 50, direction = 'left'):
    RotateCW(duty, 'a')
    RotateCCW(duty, 'b')

drive_speed = 15

def run():
    print('running')
    while True:
        if btn_start.value() == 0:
            stop()
            print("Exiting sumo code")
            exit()
        elif ir.value() == True: # no line detected, drive forward
#             print("true", ir, ir.value())
            forward(drive_speed)
        else: # line deteted, drive backward then turn
#             print("false", ir, ir.value())
            reverse(drive_speed)
            sleep(2/drive_speed) # drive backward for 1 second
            turn(drive_speed)
            sleep(1/drive_speed) # turn for one second
        sleep(1) # wait 0.1 seconds in either case

# wait for button press, then start countdown
def wait_to_run():
    print("Press Start to Begin")
    while True:
        if btn_start.value() == 0:
            for i in range(0,5):
                led.value(1)
                sleep(0.5)
                led.value(0)
                sleep(0.5)
            run()
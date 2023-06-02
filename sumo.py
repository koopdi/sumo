"""
This program uses the Sparkfun TB6612FNG motor driver
and the TCRT5000 line sensing module.
A two wheeled vehicle with differential drive is
controlled to stay within a white border.
"""
from machine import Pin
from time import sleep

from differential_drive import drive, test

# The led on the pico-w board.
led = Pin("LED", Pin.OUT)

# the start match button
btn_start = Pin(1, Pin.IN, Pin.PULL_UP)

# infrared line sensor
ir = Pin(22, Pin.IN)

def run():
    print('running')
    while True:
        if btn_start.value() == 0:
            drive.stop()
            print("Exiting sumo code")
            sleep(0.5)
            return
        elif ir.value() == True: # no line detected, drive forward
            drive.forward(time = 0.1)
        else: # line deteted, drive backward then turn
            drive.reverse(time = 0.5)
            drive.left(time = 0.75)

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
#             test()
#             return # end program, remove to keep waiting after run


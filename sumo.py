"""
This program uses the Sparkfun TB6612FNG motor driver
and the TCRT5000 line sensing module.
A two wheeled vehicle with differential drive is
controlled to stay within a white border.
"""
from machine import Pin, ADC
from time import sleep

import logger
import differential_drive
from differential_drive import drive, test, gyro_test

# differential_drive.DEFAULT_SPEED = 10

log = logger.init("sumo")
log.info("initializing sumo")

# The led on the pico-w board.
# led = Pin("LED", Pin.OUT)

# The led on the esp32 devkit v1
led = Pin(2, Pin.OUT)

# the start match button
btn_start = Pin(12, Pin.IN, Pin.PULL_DOWN)

# bump switch
left_bump = Pin(17, Pin.IN, Pin.PULL_DOWN)
right_bump = Pin(15, Pin.IN, Pin.PULL_DOWN)

# infrared line sensor
ir_digital = Pin(16, Pin.IN)
ir_analog = ADC(Pin(4))

def run():
    print('running')
    while True:
        if btn_start.value():
            drive.stop()
            print("Exiting sumo code")
            sleep(0.5)
            return
        elif ir_digital.value() == 0 or ir_analog.read_u16() < 50000: # line detected, drive backward then turn
            drive.reverse(time = 0.4)
#             turn(90)
            try:
                drive.seek()
            except Exception as e:
                log.critical(f"{str(e)}")
                logger.flush()
                raise
        elif left_bump.value() and right_bump.value():
            log.info("duo bumps")
            logger.flush()
            drive.forward(speed=100, time=0.1)
        elif left_bump.value(): # left bumper pressed
            drive.left(speed=100,time = 0.02)
            drive.forward(speed=100, time = 0.04)
        elif right_bump.value(): # right bumper pressed
            drive.right(speed=100, time = 0.02)
            drive.forward(speed=100, time = 0.04)
        else:
            drive.forward()

# wait for button press, then start countdown
def wait_to_run():
    print("Press Start to Begin")
    while True:
        if btn_start.value():
            for i in range(0,5):
                led.value(1)
                sleep(0.5)
                led.value(0)
                sleep(0.5)
            run()
#             test()
#             gyro_test()
#             return # end program, remove to keep waiting after run


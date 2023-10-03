# Sumo robot control logic.

import logger
log = logger.init("sumo")
log.info("Starting sumo code.")
logger.flush()

import drive
drive.stop()

from machine import Pin, ADC
# The led on the esp32 devkit v1
led = Pin(2, Pin.OUT)

# the start match button
btn_start = Pin(12, Pin.IN, Pin.PULL_DOWN)

# infrared line sensor
ir_digital = Pin(16, Pin.IN)
ir_analog = ADC(Pin(4))

# bump switch
left_bump = Pin(17, Pin.IN, Pin.PULL_DOWN)
right_bump = Pin(15, Pin.IN, Pin.PULL_DOWN)

from time import sleep

import buzzer

def run():
    log.info("Let's Go!")
    while True:
        if btn_start.value():
            drive.stop()
            log.info("Exiting sumo code")
            sleep(0.5)
            return
        elif ir_analog.read_u16() < 50000: # line detected
            drive.reverse(time = 0.4)
            drive.turn(course = 30)
            try:
                drive.seek(course = 90)
            except Exception as e:
                log.critical(f"{str(e)}")
                logger.flush()
        elif left_bump.value() and right_bump.value():
            drive.forward(speed=100, time=0.1)
        elif left_bump.value(): # left bumper pressed
            drive.left(speed=100, time = 0.02)
            drive.forward(speed=100, time = 0.04)
        elif right_bump.value(): # right bumper pressed
            drive.right(speed=100, time = 0.02)
            drive.forward(speed=100, time = 0.04)
        else:
            drive.forward()

# wait for button press, then start countdown
def wait_to_run():
    log.info("Press Start to Begin")
    while True:
        if btn_start.value():
            for i in range(0,4):
                led.value(1)
                buzzer.buzz(200, 5)
                sleep(0.5)
                led.value(0)
                buzzer.buzz(200,0)
                sleep(0.5)
                
            led.value(1)
            buzzer.buzz(440, 5)
            sleep(0.5)
            led.value(0)
            buzzer.buzz(200,0)
            sleep(0.5)
            
            run()
            log.info("Press Start to Begin")

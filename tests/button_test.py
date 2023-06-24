from machine import Pin
from time import sleep

# the start match button
btn_start = Pin(12, Pin.IN, Pin.PULL_DOWN)

# bump switch
left_bump = Pin(17, Pin.IN, Pin.PULL_DOWN)
right_bump = Pin(15, Pin.IN, Pin.PULL_DOWN)

while True:
    print(f"lbump: {left_bump.value()}, rbump: {right_bump.value()}, start, {btn_start.value()}")
    sleep(0.1)
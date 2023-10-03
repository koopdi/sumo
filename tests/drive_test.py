from time import sleep

import drive
from blink_pwm import led
led.duty_u16(0)

SPEED = 20

drive.right(speed=SPEED, time=0.2)
sleep(0.5)
drive.left(speed=SPEED, time=0.2)
sleep(0.5)

drive.head(720 - 90)
print("heading on course")
sleep(3)
drive.head(-45)

# drive.turn(angle = -45)
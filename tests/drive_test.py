from time import sleep

import drive

SPEED = 20

drive.right(speed=SPEED, time=0.2)
sleep(0.5)
drive.left(speed=SPEED, time=0.2)
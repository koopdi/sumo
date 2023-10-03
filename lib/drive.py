
from machine import Pin, PWM, I2C, ADC
from utime import sleep, ticks_us, ticks_diff

import motor
from laser import tof
from motion import mpu
import logger

DEFAULT_SPEED = 60

def speed(speed):
    DEFAULT_SPEED = speed

log = logger.init("drive")
log.info("initializing drive system")

# motor a control pins
pwma = PWM(Pin(23))
ina2 = Pin(22, Pin.OUT)
ina1 = Pin(21, Pin.OUT)

# motor b control pins
inb1 = Pin(19, Pin.OUT)
inb2 = Pin(18, Pin.OUT)
pwmb = PWM(Pin(5))

# set pwm frequency
pwma.freq(20000)
pwmb.freq(20000)

# set pwm duty to 0 at startup
pwma.duty_u16(0)
pwmb.duty_u16(0)

bridge = motor.TB66(ina1, ina2, pwma, inb1, inb2, pwmb)

def percent_to_duty(speed):
    return int((speed*65535)/100)
     
def forward(speed = DEFAULT_SPEED, time = None):
    bridge.a.duty(percent_to_duty(speed))
    bridge.b.duty(percent_to_duty(speed))
    bridge.a.high_low()
    bridge.b.low_high()
    
    if time != None:
        sleep(time)
        stop()
    
def reverse(speed = DEFAULT_SPEED, time = None):
    bridge.a.duty(percent_to_duty(speed))
    bridge.b.duty(percent_to_duty(speed))
    bridge.a.low_high()
    bridge.b.high_low()
    
    if time != None:
        sleep(time)
        stop()
        
def left(speed = DEFAULT_SPEED, time = None):    
    duty = percent_to_duty(speed)
    bridge.a.duty(duty)
    bridge.b.duty(duty)
    bridge.a.high_low()
    bridge.b.high_low()
    
    if time != None:
        sleep(time)
        stop()
        
def right(speed = DEFAULT_SPEED, time = None):
    bridge.a.duty(percent_to_duty(speed))
    bridge.b.duty(percent_to_duty(speed))
    bridge.a.low_high()
    bridge.b.low_high()
    
    if time != None:
        sleep(time)
        stop()
    
def stop():
    bridge.a.duty(0)
    bridge.b.duty(0)
    bridge.a.high_high()
    bridge.b.high_high()
    
def coast():
    bridge.a.duty(0)
    bridge.b.duty(0)
    bridge.a.low_low()
    bridge.b.low_low()

# remap angle to the range (-180, 180]
def untwist(angle):
    angle = angle % 360
        
    if angle > 180:
        angle -= 360
    elif angle <= -180:
        angle += 360
        
    return angle

TICK_REV = 360*1000000 # Number of micro degrees per revolution
TRIM_LEFT = -2500000000
GYRO_DRIFT_X = -3.432
PER_TICK = 360 / TICK_REV
TICKS_PER = TICK_REV / 360
MAX_GYRO_RATE = 8000 # 8,000 samples/second (8kHz)

U16_MAX       = 65535
MAX_SPEED     = 40
MIN_SPEED     = 10
MARGIN        = 2  # minimum course bearing to trigger drive (degrees)

# Turn until on course or a target has been acquired.
def seek(speed = DEFAULT_SPEED, course = 180):
    gyro_heading  = 0  # the current direction (micro degrees)
    heading       = 0  # the current direction (degrees)
    course        = untwist(course)  # the target direction (degrees)
    last_us = ticks_us()
    while abs(heading - course) > MARGIN:
        x = mpu.gyro.x - GYRO_DRIFT_X               # get angular velocity
        us = ticks_us()                             # start timer
        gyro_heading += x * ticks_diff(us, last_us) # update direction (micro degrees)
        heading = gyro_heading // 1000000           # update direction (degrees)
        heading = untwist(heading)
        # drive
        if tof.ping() < 500:
            forward()
            return
        elif heading < course-MARGIN:
            right(speed = speed)
        elif heading > course+MARGIN:
            left(speed = speed)
        else:
            stop()
        last_us = us                                # end timer
    
    stop()

def turn(speed = DEFAULT_SPEED, course = 180):
    gyro_heading  = 0  # the current direction (micro degrees)
    heading       = 0  # the current direction (degrees)
    course        = untwist(course)  # the target direction (degrees)
    last_us = ticks_us()
    while abs(heading - course) > MARGIN:
        x = mpu.gyro.x - GYRO_DRIFT_X               # get angular velocity
        us = ticks_us()                             # start timer
        gyro_heading += x * ticks_diff(us, last_us) # update direction (micro degrees)
        heading = gyro_heading // 1000000           # update direction (degrees)
        heading = untwist(heading)
        # drive
        if heading < course-MARGIN:
            right(speed = speed)
        elif heading > course+MARGIN:
            left(speed = speed)
        else:
            stop()
        last_us = us       # end timer
    
    stop()

def head(course):
    gyro_heading  = 0  # the current direction (micro degrees)
    heading       = 0  # the current direction (degrees)
    course        = untwist(course)  # the target direction (degrees)
    last_us = ticks_us()
    while abs(heading - course) > MARGIN:
        x = mpu.gyro.x - GYRO_DRIFT_X               # get angular velocity
        us = ticks_us()                             # start timer
        gyro_heading += x * ticks_diff(us, last_us) # update direction (micro degrees)
        heading = gyro_heading // 1000000           # update direction (degrees)
        heading = untwist(heading)
        # drive
        speed = abs(heading)/180*MAX_SPEED
        if speed < MIN_SPEED: speed = MIN_SPEED
        if heading < course-MARGIN:
            right(speed = speed)
        elif heading > course+MARGIN:
            left(speed = speed)
        else:
            stop()
        last_us = us       # end timer
    
    stop()
        

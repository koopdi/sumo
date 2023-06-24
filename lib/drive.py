
from machine import Pin, PWM, I2C, ADC
from utime import sleep, ticks_us, ticks_diff

import motor
# from laser import tof
# from motion import mpu
import logger

DEFAULT_SPEED = 20

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

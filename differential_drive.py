import motor_driver
from machine import Pin ,PWM
from utime import sleep

DEFAULT_SPEED = 30

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
pwma.freq(20000)
pwmb.freq(20000)

# set pwm duty to 0 at startup
pwma.duty_u16(0)
pwmb.duty_u16(0)

def percent_to_duty(speed):
    return int((speed*65536)/100)

class Diff_Drive():
    def __init__(self, bridge):
        self.bridge = bridge
        
    def forward(self, speed = DEFAULT_SPEED, time = None):

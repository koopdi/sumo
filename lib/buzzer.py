from machine import Pin, PWM
from time import sleep
buzzer = PWM(Pin(32))
buzzer.duty_u16(0)

def percent_to_duty(volume):
    return int((volume*65535)/100)

def buzz(freq, volume):
    buzzer.freq(freq)
    buzzer.duty_u16(percent_to_duty(volume))
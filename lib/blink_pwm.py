# Use PWM to rapidly blink the LED on the pico/esp32 board.
# Does not work on pico-w.
from machine import Pin, PWM
from time import sleep

U16_MAX = 65535

def BlinkPWM(freq=8, duty=U16_MAX//2, led_pin=2):
    led = PWM(Pin(led_pin))
    led.freq(freq)
    led.duty_u16(duty)
    return led

led = BlinkPWM()
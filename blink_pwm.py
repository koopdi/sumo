# Use PWM to rapidly blink the LED on the pico board.

from machine import Pin, PWM
from time import sleep

def BlinkPWM(freq=8, duty=2048, led_pin=Pin(25)):
    led = PWM(Pin(0))
    led.freq(freq) # minimum freq = 8
    led.duty_u16(duty)

BlinkPWM()
sleep(1)
# led2 = Pin(25, Pin.OUT)
# led2.value

from machine import Pin
led = Pin("LED", Pin.OUT)
led.value(1)  // a method instead of setting the value
sleep(1)
led.value(0) // turn it off again.



# TypeError: function doesn't take keyword arguments
# led = PWM(Pin(25), freq=5, duty=128)
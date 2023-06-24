def info():
    from os import uname
    print(uname())
    
def blink():
    from machine import Pin
    from time import sleep
    led = Pin(2, Pin.OUT)
    print('Blinking LED on', led)
    for i in range(10):
        led.value(1)
        sleep(0.1)
        led.value(0)
        sleep(0.1)

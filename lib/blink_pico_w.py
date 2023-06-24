import machine
import utime

led_onboard = machine.Pin("LED", machine.Pin.OUT)

for i in range(0,10):
    led_onboard.toggle()
    utime.sleep(0.1)
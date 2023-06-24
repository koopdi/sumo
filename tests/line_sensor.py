from machine import Pin, PWM, ADC
from time import sleep
ao1 = ADC(Pin(4))
do1 = Pin(16, Pin.IN)
# ao2 = ADC(Pin(27))
# do2 = Pin(22, Pin.IN)
while True:
    print(f"ao1: {ao1.read_u16()}, do1: {35000*do1.value()}")
#     print(f"ao1: {ao1.read_u16()}, do1: {4000*do1.value()}, ao2: {ao2.read_u16()}, do2: {4000*do2.value()}")
    sleep(0.1)
#     print(f"{ao.read()}")
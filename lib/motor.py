"This program uses the Sparkfun TB6612FNG motor driver"

from machine import Pin, PWM

class Motor():
    def __init__(self, in1 = None, in2 = None, inpwm = None):
        self.pin_1 = in1
        self.pin_2 = in2
        self.pwm_pin = inpwm
        
    def __str__(self):
        str = "Motor Object Stats:\n"
        str += "pin_1: " + repr(self.pin_1) + '\n'
        str += "pin_2: " + repr(self.pin_2) + '\n'
        str += "pwm_pin: " + repr(self.pwm_pin) + '\n'
        return str

    def high_low(self):
        self.pin_1.value(1)
        self.pin_2.value(0)

    def low_high(self):
        self.pin_1.value(0)
        self.pin_2.value(1)

    def high_high(self):
        self.pin_1.value(1)
        self.pin_2.value(1)

    def low_low(self):
        self.pin_1.value(0)
        self.pin_2.value(0)
    
    def pwm(self, duty = None, freq = None):
        if duty != None:
            self.pwm_pin.duty_u16(duty)
        if freq != None:
            self.pwm_pin.freq(freq)
        return self.pwm_pin
    
    def duty(self, duty):
        self.pwm_pin.duty_u16(duty)

class TB66:
    def __init__(self, ina1 = None, ina2 = None, pwma = None,
                       inb1 = None, inb2 = None, pwmb = None):
        self.a = Motor(ina1, ina2, pwma)
        self.b = Motor(inb1, inb2, pwmb)
        
    def __str__(self):
        str = "Motor A:\n"
        str += a
        str += "Motor B:\n"
        str += b
        return str
        

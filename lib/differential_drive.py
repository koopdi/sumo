import motor_driver
from machine import Pin ,PWM, I2C, ADC
from utime import sleep, ticks_ms, ticks_cpu, ticks_diff
from imu import MPU6050
import logger
from blink_pwm import led
from laser import tof
# import traceback

DEFAULT_SPEED = 15

TICK_REV = 39400000000 # Number of gyro ticks per revolution
TRIM_LEFT = -2500000000
GYRO_DRIFT_X = -3.570254
PER_TICK = 360 / TICK_REV
TICKS_PER = TICK_REV / 360

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

# initialize gyroscope
log.info("initializing gyroscope")
bus = 0
sda = Pin(14)
scl = Pin(13)
freq = 400000
log.debug(f"i2c bus: {bus}, serial data: {str(sda)}, serial clock: {str(scl)}")
i2c = I2C(bus, sda=sda, scl=scl, freq=freq)
mpu = MPU6050(i2c)
mpu.gyro_range = 3
log.debug(f"gyro_range: {mpu.gyro_range}")

led.duty_u16(0)

def to_ticks(angle):
    return angle*TICKS_PER

def to_angle(ticks):
    return ticks*PER_TICK

def percent_to_duty(speed):
    return int((speed*65535)/100)

class Diff_Drive():
    def __init__(self, bridge):
        self.bridge = bridge
        
    def forward(self, speed = DEFAULT_SPEED, time = None):
        self.bridge.a.duty(percent_to_duty(speed))
        self.bridge.b.duty(percent_to_duty(speed))
        self.bridge.a.high_low()
        self.bridge.b.low_high()
        
        if time != None:
            sleep(time)
            self.stop()
        
    def reverse(self, speed = DEFAULT_SPEED, time = None):
        self.bridge.a.duty(percent_to_duty(speed))
        self.bridge.b.duty(percent_to_duty(speed))
        self.bridge.a.low_high()
        self.bridge.b.high_low()
        
        if time != None:
            sleep(time)
            self.stop()
            
    def left(self, speed = DEFAULT_SPEED, time = None):
        duty = percent_to_duty(speed)
        self.bridge.a.duty(duty)
        self.bridge.b.duty(duty)
        self.bridge.a.high_low()
        self.bridge.b.high_low()
        if time != None:
            sleep(time)
            self.stop()
            
    def right(self, speed = DEFAULT_SPEED, time = None):
        self.bridge.a.duty(percent_to_duty(speed))
        self.bridge.b.duty(percent_to_duty(speed))
        self.bridge.a.low_high()
        self.bridge.b.low_high()
        
        if time != None:
            sleep(time)
            self.stop()
        
    def stop(self):
        self.bridge.a.duty(0)
        self.bridge.b.duty(0)
        self.bridge.a.high_high()
        self.bridge.b.high_high()
        
    def coast(self):
        self.bridge.a.duty(0)
        self.bridge.b.duty(0)
        self.bridge.a.low_low()
        self.bridge.b.low_low()
        
    def turn(self, speed = DEFAULT_SPEED, angle = 180):
        DELAY = 0.01
        ATK_DIST = 350
        try: # catch exceptions
            angle = to_ticks(angle)
            curr_angle = 0
            if(angle < 0):
                angle += TRIM_LEFT
                drive.left(speed)
                while curr_angle > angle:
                    start = ticks_cpu()
#                     sleep(DELAY)
#                     if tof.ping() < ATK_DIST:
#                         drive.forward(speed=100)
#                         break
                    delta = ticks_diff(ticks_cpu(), start)
                    curr_angle += mpu.gyro.x*(delta - GYRO_DRIFT_X)
#                     if start % 10 == 0:
#                         log.debug(f"curr_angle {curr_angle}, angle {angle}")
            else:
                drive.right(speed)
                while curr_angle < angle:
                    start = ticks_cpu()
#                     sleep(DELAY)
#                     if tof.ping() < ATK_DIST:
#                         drive.forward(speed=100)
#                         break
                    delta = ticks_diff(ticks_cpu(), start)
                    curr_angle += mpu.gyro.x*(delta - GYRO_DRIFT_X)
#                     if start % 10 == 0:
#                         log.debug(f"curr_angle {to_angle(curr_angle)}, angle {to_angle(angle)}")
                        
            self.stop()
            
        except OSError as e:
            self.stop()
#             log.error(f"OSError: {str(e)}")
            logger.flush()
        except Exception as e:
            self.stop()
            log.critical(f"unknown exception: {str(e)}")
#             traceback.print_stack()
#             stack_trace_info = traceback.format_stack()
            logger.flush()

    def seek(self, speed = DEFAULT_SPEED, angle = 360):
        angle += 25
        angle = to_ticks(angle)
        
        DELAY = 0.01
        
        min_dist = 10000
        dist = min_dist
        
        min_angle = 0
        curr_angle = min_angle
        
        drive.right(speed)
        
        while curr_angle < angle:
            start = ticks_cpu()
#             sleep(DELAY)
            dist = tof.ping()
            if dist < 500:
                drive.forward()
                return
            elif dist < min_dist:
                min_dist = dist
                min_angle = curr_angle
            delta = ticks_diff(ticks_cpu(), start)
            curr_angle += mpu.gyro.x*(delta - GYRO_DRIFT_X)
            if start % 3 == 0:
                log.debug(f"curr_angle {to_angle(curr_angle)}, angle {to_angle(angle)}, min_dist, {min_dist}, dist {dist}")
                
        drive.stop()
#         min_angle = to_angle(min_angle)
        min_angle = to_angle(min_angle) - 25
        if min_angle < 0: min_angle = 0
        print(min_angle)
#         sleep(0.1)
        drive.turn(angle = min_angle)
                
bridge = motor_driver.TB66(ina1, ina2, pwma, inb1, inb2, pwmb)
drive = Diff_Drive(bridge)

def test():
    bridge = motor_driver.TB66(ina1, ina2, pwma, inb1, inb2, pwmb)
    drive = Diff_Drive(bridge)
    for speed in range(0,101,1):
        drive.left(speed = speed, time = 0.1)
        drive.right(speed = speed, time = 0.1)
    for speed in range(0,101,1):
        drive.forward(speed = speed, time = 0.1)
        drive.reverse(speed = speed, time = 0.1)
    drive.coast()
    
def gyro_test():
    log.info("gyro_test")
    
    for i in range(0,5):
        log.debug(f"right {i}")
        logger.flush()
        drive.turn(angle = 360)
        sleep(3)
        log.debug(f"left {i}")
        logger.flush()
        drive.turn(angle = -360)
        sleep(3)

    log.info("gyro_test complete")   
    logger.flush()
    
def laser_test():
    log.info("laser test")
    
    start = ticks_ms()
    delta = 0
    while delta < 120*1000:
        range = tof.ping() - 150
        log.debug(f"range: {range} mm")
        if range < 800 and range > 300:
            drive.forward()
        elif range < 200:
            drive.reverse()
        else:
            drive.coast()
        sleep(0.1)
        delta = ticks_diff(ticks_ms(), start)
    drive.coast()
from imu import MPU6050
from machine import I2C, Pin
from time import sleep, ticks_cpu, ticks_us, ticks_ms, ticks_diff
import logger

log = logger.init("imu_test")
log.info("initializing imu")

bus = 0
sda = Pin(14)
scl = Pin(13)
freq = 400000
log.debug(f"i2c bus: {bus}, serial data: {str(sda)}, serial clock: {str(scl)}")
i2c = I2C(bus, sda=sda, scl=scl, freq=freq)
mpu = MPU6050(i2c)
mpu.gyro_range = 3 # max speed 2000 deg/sec
log.debug(f"gyro_range: {mpu.gyro_range}")

# calculate the average sensor drift (deg/sec)
def calc_drift(samples):
    sum = 0
    for i in range(0, samples):
        sum += mpu.gyro.x
        sleep(0.01)
    return sum / samples

drift = -3.570254
# drift = calc_drift(10000) # avg drift, -3.570254
# print (f"drift, {drift}")

TICK_REV = 5000000 # Number of gyro ticks per revolution
GYRO_DRIFT_X = -3.432
PER_TICK = 360 / TICK_REV
TICKS_PER = TICK_REV / 360

def to_ticks(angle):
    return angle*TICKS_PER

def to_angle(ticks):
    return ticks*PER_TICK

gyro_heading = 0
heading      = 0

# while True:
#     start = ticks_cpu()                               # start timer
#     heading = to_angle(gyro_heading)
#     print(f"heading {to_angle(heading)}, speed {mpu.gyro.x-GYRO_DRIFT_X}")
#     sleep(0.1)
#     delta = ticks_diff(ticks_cpu(), start)            # end timer
#     gyro_heading += (mpu.gyro.x - GYRO_DRIFT_X)*delta # update heading
    
gyro_heading = 0   # this is in microdegrees
# last_x = mpu.gyro.x
last_us = ticks_us()
while True:
  x = mpu.gyro.x - GYRO_DRIFT_X
  us = ticks_us()
  gyro_heading += x * ticks_diff(us, last_us)
  gyro_heading %= 360 * 1000000
  sleep(0.5)
  heading = gyro_heading // 1000000 # this is in degrees
  print(heading)
#   last_x = x
  last_us = us

# while True:
#     try:
#         start = ticks_cpu()
#         sleep(0.01)
#         delta = ticks_diff(ticks_cpu(), start)
#         gyro = mpu.gyro.x
#         pos += (gyro - drift)*delta
#         
#         if start%5 == 0 :
#             print("pos - drift", pos // 160000000)
#             
#     except OSError as e:
#             log.error(f"OSError: {str(e)}")
#             logger.flush()
#             
#     except Exception as e:
#             log.critical(f"unknown exception: {str(e)}")
#             logger.flush()

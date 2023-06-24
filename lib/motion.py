# Setup the mpu-6050 inertial measurement unit

from machine import Pin, PWM, I2C, ADC
from imu import MPU6050

import logger
log = logger.init("motion")

TICK_REV = 360*1000000 # Number of micro degrees per revolution
TRIM_LEFT = -2500000000
GYRO_DRIFT_X = -3.432
PER_TICK = 360 / TICK_REV
TICKS_PER = TICK_REV / 360
MAX_GYRO_RATE = 8000 # 8,000 samples/second (8kHz)

# initialize gyroscope
log.info("initializing gyroscope")

# pins
bus = 0
sda = Pin(14)
scl = Pin(13)
freq = 400000

log.debug(f"i2c bus: {bus}, serial data: {str(sda)}, serial clock: {str(scl)}")
logger.flush()

# i2c
i2c = I2C(bus, sda=sda, scl=scl, freq=freq)
# mpu object
mpu = MPU6050(i2c)
mpu.gyro_range = 3 # set to max range: +/- 2,000 degrees/second


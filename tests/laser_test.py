# import time
from machine import Pin, I2C
from vl53l0x import VL53L0X
from time import sleep
import logger
log = logger.init("laser_test")

bus = 1
sda = 26
scl = 27
freq = 400000
log.debug(f"i2c bus: {bus}, serial data: {str(sda)}, serial clock: {str(scl)}")
i2c = I2C(bus, sda=Pin(sda), scl=Pin(scl), freq=freq)

# Create a VL53L0X object
tof = VL53L0X(i2c)

# check interference from other i2c device
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# from imu import MPU6050
# log.info("initializing imu")
# bus = 0
# sda = Pin(14)
# scl = Pin(13)
# freq = 400000
# log.debug(f"i2c bus: {bus}, serial data: {str(sda)}, serial clock: {str(scl)}")
# i2c = I2C(bus, sda=sda, scl=scl, freq=freq)
# mpu = MPU6050(i2c)
# mpu.gyro_range = 3
# log.debug(f"gyro_range: {mpu.gyro_range}")

# print(i2c.scan())

# the measuting_timing_budget is a value in ms, the longer the budget, the more accurate the reading. 
# budget = tof.measurement_timing_budget_us
# print("Budget was:", budget)
# tof.set_measurement_timing_budget(0)

# Sets the VCSEL (vertical cavity surface emitting laser) pulse period for the 
# given period type (VL53L0X::VcselPeriodPreRange or VL53L0X::VcselPeriodFinalRange) 
# to the given value (in PCLKs). Longer periods increase the potential range of the sensor. 
# Valid values are (even numbers only):

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 2)
# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12) # VL53L0X::VcselPeriodPreRange

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 32768)
# tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8) # VL53L0X::VcselPeriodFinalRange

while True:
# Start ranging
    dist = tof.ping()
    if(dist < 3000):
        print(f"dist: {dist} mm")
    sleep(0.1)
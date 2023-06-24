from machine import Pin, I2C
from vl53l0x import VL53L0X
import logger
log = logger.init("laser")

# initialize laser
log.info("initializing laser")
bus = 1
sda = Pin(26)
scl = Pin(27)
freq = 400000
log.debug(f"i2c bus: {bus}, serial data: {str(sda)}, serial clock: {str(scl)}")
i2c = I2C(bus, sda=sda, scl=scl, freq=freq)
# Create a VL53L0X object
tof = VL53L0X(i2c)

tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 2)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 32768)
# This file is executed on every boot (including wake-boot from deepsleep)

import logger
log = logger.init("boot")
log.info(" ---------------- system online -------------------")
logger.flush()

# begin blinking onboard led rapidly
from blink_pwm import led
led.freq(20)

#---------------setup webrepl---------------------------#
# import network
# 
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='bobby_drop_tables', password='smith')
# 
# import webrepl
# webrepl.start(password="1234")

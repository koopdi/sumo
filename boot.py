# This file is executed on every boot (including wake-boot from deepsleep)

# doesn't seem to do anythin
# import esp
# esp.osdebug(esp.LOG_VERBOSE) #os debug on
# esp.osdebug(None) #os debug off

# copy log from previous boot then clear it
# import os
# os.rename("log.txt", "log.old.txt")

import logger
log = logger.init("boot")
log.info(" ---------------- system online -------------------")
logger.flush()

#---------------setup webrepl---------------------------#
# import network
# 
# ap = network.WLAN(network.AP_IF)
# ap.active(True)
# ap.config(essid='bobby_drop_tables', password='smith')
# 
# import webrepl
# webrepl.start(password="1234")

#----------calibrate esc----#
# from esc import calibrate
# calibrate()

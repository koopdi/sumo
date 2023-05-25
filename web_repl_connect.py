# Start the webrepl for remote coding.
# This file should be imported in boot.py, after setting up networking.
# Thonny doesn't have an option for pico w, so choose esp8266 instead and configure the connection for webrepl instead of the com port.

import webrepl
webrepl.start(password="1234")

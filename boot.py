# This code will run automatically before main.py

# Signal a successful boot by printing a message and blinking the onboard LED. 
print('boot.py')
import blink_pico_w

# Create a wifi access point and start the webrepl.
import start_AP_IF
import web_repl_connect

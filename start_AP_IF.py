# Create a wifi access point.
# This feature isn't well supported by micropython on the pico w yet.

import network

# Choose a name and password.
# 'micropythoN' is the default password.
my_ssid='bobby_dr00bbles'
my_password='micropythoN'

# Activate WLAN interface in Access Point mode.
ap = network.WLAN(network.AP_IF)
ap.config(essid=my_ssid, password=my_password)
ap.active(True)

# Print out some stats.
print('hostname:', ap.config('hostname'))
print(ap, 'active?:', ap.active())
print('ssid:', ap.config('ssid'))
print('channel:', ap.config('channel'))
if ap.status() == network.STAT_GOT_IP:
    print('status: Got IP')
    print(ap.ifconfig())
if ap.isconnected():
    print('The station is online.')

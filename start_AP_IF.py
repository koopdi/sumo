import network
my_ssid='bobby_dr00bbles'
my_password='micropythoN'
# ap = network.WLAN(network.AP_IF)
# ap.config(ssid='bobby_drop_tables')
# ap.config(password='smith')

ap = network.WLAN(network.AP_IF)
ap.config(essid=my_ssid, password=my_password)
# ap.config(essid=ssid)
# ap.config(password=password)

ap.active(True)

print('hostname:', ap.config('hostname'))
# print('password:', ap.config('password'))
print(ap, 'active?:', ap.active())
print('ssid:', ap.config('ssid'))
print('channel:', ap.config('channel'))
if ap.status() == network.STAT_GOT_IP:
    print('status: Got IP')
    print(ap.ifconfig())
if ap.isconnected():
    print('The station is online.')

# This code will run automatically after boot.py.

import uos
print("System Information")
# display system information
print('uname: ', uos.uname())

import sumo2
print("Launching sumo code...")
sumo2.wait_to_run()

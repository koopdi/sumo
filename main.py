import uos
print("System Information")
# display system information
print('uname: ', uos.uname())



import sumo
print("Launching sumo code...")
sumo.wait_to_run()
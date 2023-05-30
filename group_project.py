from machine import Pin
from utime import sleep, sleep_ms

# Define pin numbers for IR sensor and motor control
IR_PIN = ...#we will write here which pin we have used.
MOTOR_FORWARD_PIN = ...#we will write here which pin we have used.
MOTOR_REVERSE_PIN = ...#we will write here which pin we have used.

# Initialize GPIO pins
ir = Pin(IR_PIN, Pin.IN)
motor_forward = Pin(MOTOR_FORWARD_PIN, Pin.OUT)
motor_reverse = Pin(MOTOR_REVERSE_PIN, Pin.OUT)

# Function to drive the robot forward
def forward(speed):
    motor_forward.on()
    motor_reverse.off()

# Function to drive the robot backward
def reverse(speed):
    motor_forward.off()
    motor_reverse.on()

# Function to stop the robot
def stop():
    motor_forward.off()
    motor_reverse.off()

# Function to perform a turn
def turn():
    # Implement your turn logic here
    # Adjust motor control as per your robot's configuration

# Main loop
while True:
    if ir.value() == 1:  # No line detected, drive forward
        print("No line detected")
        forward(50)
    else:  # Line detected, drive backward then turn
        print("Line detected")
        reverse(50)
        sleep(1)  # Drive backward for 1 second
        stop()  # Stop the robot
        sleep(0.5)  # Pause for a short duration
        turn()  # Perform a turn
        sleep(1)  # Turn for 1 second
        stop()  # Stop the robot

    sleep_ms(100)  # Wait 0.1 seconds in either case

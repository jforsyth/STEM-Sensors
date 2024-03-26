
# include all the relevant libraries
import math
from time import time
import serial
from serial.tools.list_ports import comports

"""
Step 1: Determine which Serial/USB port is in use. This will vary between Windows, Mac, and Linux systems.
If the port cannot be found then an error message will appear listing the various ports available. Keep 
adjusting the variable portName until the correct one is found.
"""
portName = '/dev/cu.usbserial-10'
# portName = 'COM3'

# do not change this parameter
baudRate = 57600

# attempt to open port
try:
    ser = serial.Serial(portName, baudRate)
    print("Opening port " + ser.name)

# if fail, print a helpful message
except:
    print("Couldn't open port. Try changing portName variable to one of the options below:")
    ports_list = comports()
    for port_candidate in ports_list:
        print(port_candidate.device)
    exit(-1)

if ser.is_open:
    print("Success!")

else:
    print("Unable to open port :(")
    exit(0)

# get the start time for the loop
start_time = time()

# set duration and increment counter for the loop
duration = 200
counter = 0

# run this loop for duration seconds
while abs(start_time - time()) < duration:

    # wait until we have a line from the Arduino
    bytes = ser.readline()

    # decode the bytes into a string. Remove all whitespace
    received = bytes.decode('utf-8')
    received = received.replace('\r', '').replace('\n', '')

    # split the string based upon commas
    values = received.split(",")

    # extra sensor data from each field of the CSV line
    temp = float(values[0])
    humidity = float(values[1])
    pressure = float(values[2])
    uv_index = float(values[3])
    x_accel = float(values[4])
    y_accel = float(values[5])
    z_accel = float(values[6])
    magnitude = math.sqrt(x_accel * x_accel + y_accel * y_accel + z_accel * z_accel)
    magnitude = round(magnitude, 2)

    if counter % 10 == 0:
        print("Temp\tHumid\tPressure\tUV\t\tX\t\tY\t\tZ\t\tMag")

    print(str(temp) + "\t" + str(humidity) + "\t" + str(pressure) + "\t\t" + str(uv_index) + "\t"
          + str(x_accel) + "\t" + str(y_accel) + "\t" + str(z_accel) + "\t\t" + str(magnitude))

    counter += 1


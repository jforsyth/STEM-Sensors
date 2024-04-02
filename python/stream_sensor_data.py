
# include all the relevant libraries
import math
from time import time
import serial
from serial.tools.list_ports import comports

from utils import find_serial_port

"""
Scan all the COM/Serial ports to find the correct one...
"""
ser = find_serial_port()

# get the start time for the loop
start_time = time()

# set duration and increment counter for the loop
duration = 120
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
        print("Temp\tHumid\tAlt\t\t\tUV\t\tX\t\tY\t\tZ\t\tMag")

    print(str(temp) + "\t" + str(humidity) + "\t" + str(pressure) + "\t\t" + str(uv_index) + "\t"
          + str(x_accel) + "\t" + str(y_accel) + "\t" + str(z_accel) + "\t\t" + str(magnitude))

    counter += 1

ser.close()
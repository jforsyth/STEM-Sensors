
# include all the relevant libraries
import math
from time import time
import serial
from serial.tools.list_ports import comports

"""
Scan all the COM/Serial ports to find the correct one...
"""
# this parameter should be updated automatically by the software
serial_port_name = ''

# do not change this parameter
baudRate = 9600

print('Scanning serial ports...')
ports_list = comports()
for port_candidate in ports_list:
    port_name = port_candidate.device

    try:
        print("Attempting port " + port_name)
        port = serial.Serial(port_name, baudrate=baudRate, timeout=3)


        # print("Attempting read...")
        line = port.readline()

        if len(line) == 0:
            # print("Nothing read...")
            continue
        else:
            serial_port_name=port_name
            print('Using port ', port_name)
            port.close()
            break
    except:
        # print("Exception occurred.")
        do_nothing = 0


# attempt to open port
try:
    ser = serial.Serial(serial_port_name, baudRate)
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
duration = 10
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

ser.close()
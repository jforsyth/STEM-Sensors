# include all the relevant libraries
import math
from musicpy.musicpy import play, freq_to_note
import serial
from serial.tools.list_ports import comports
from time import time


def scale(value, input_low, input_high, output_low, output_high):
    """
    A custom method to scale 'value' from one input range into another. Input value is restricted to the
    intput value range. Output is also restricted to output range. Scale is linear
    :param value: Value to be scaled
    :param input_low: Low bound for input domain
    :param input_high: Upper bound for output domain
    :param output_low: Low bound for output range
    :param output_high: Upper bound for output range
    :return: Result of scaling operation
    """
    if value < input_low:
        value = input_high

    elif value > input_high:
        value = input_high

    return (value - input_low) / (input_high - input_low) * (output_high - output_low) + output_low


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

        line = port.readline()

        if len(line) == 0:
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
duration = 20
counter = 0

# run this loop for duration seconds
while abs(start_time - time()) < duration:

    # wait until we have a line from the Arduino
    serial_data = ser.readline()

    # decode the bytes into a string. Remove all whitespace
    received = serial_data.decode('utf-8')
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
    """
    Step 1: All data from the sensor board has been read in. Only one sensor can be "played" at a time.
    In the section below use the scale() method, or develop your own equation, to map the sensor data range
    into a musical range. For example: UV may range from 0 to 10. This can be mapped into a reasonable musical 
    range of 300 - 700 Hz.
    
    Adjust the value= parameter to select different sensors.
    Adjust the input_low and input_high parameters to correspond to reasonable upper and lower bounds for the sensor
    Adjust the output_low and output_high parameter to map to suitable frequencies. The human hearing range is ~20Hz to 20,000 Hz
    """

    # scale the sensor data to appropriate values
    temperature_as_frequency = scale(value=temp, input_low=20, input_high=30, output_low=300, output_high=1000)
    humidity_as_frequency = scale(value=humidity, input_low=0, input_high=100, output_low=300, output_high=1000)
    uv_index_as_frequency = scale(value=uv_index, input_low=0, input_high=11, output_low=300, output_high=1000)
    magnitude_as_frequency = scale(value=magnitude, input_low=0.5, input_high=4, output_low=300, output_high=1000)

    # use the built-in freq_to_note method to convert from a frequency (Hertz)
    # to a note (Note, Octave)
    temperature_notes = freq_to_note(temperature_as_frequency)
    humidity_notes = freq_to_note(humidity_as_frequency)
    uv_notes = freq_to_note(uv_index_as_frequency)
    magnitude_notes = freq_to_note(magnitude_as_frequency)

    """
    Step 2: The sensor data has not been converted into notes that the musicpy library can understand. 
    Adjust the instrument= parameter to be one of the 128x instruments available.
    """

    # play the notes with a selected instrument
    play(temperature_notes, wait=False, instrument='Woodblock', save_as_file=False)

ser.close()

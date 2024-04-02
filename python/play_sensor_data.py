# include all the relevant libraries
import math
from musicpy.musicpy import play, freq_to_note
import serial
from serial.tools.list_ports import comports
from time import time

from utils import find_serial_port,scale



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
        print("Temp\tHumid\tAlt\t\tUV\t\tX\t\tY\t\tZ\t\tMag")

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

    # scale the sensor data to appropriate values. You may modify these lines.
    temperature_as_frequency = scale(value=temp, input_low=20, input_high=30, output_low=300, output_high=1000)
    humidity_as_frequency = scale(value=humidity, input_low=15, input_high=75, output_low=300, output_high=1000)
    uv_index_as_frequency = scale(value=uv_index, input_low=0, input_high=4, output_low=300, output_high=1000)
    magnitude_as_frequency = scale(value=magnitude, input_low=0.5, input_high=4, output_low=300, output_high=1000)

    # use the built-in freq_to_note method to convert from a frequency (Hertz)
    # to a note (Note, Octave). Do not modify these lines.
    temperature_notes = freq_to_note(temperature_as_frequency)
    humidity_notes = freq_to_note(humidity_as_frequency)
    uv_notes = freq_to_note(uv_index_as_frequency)
    magnitude_notes = freq_to_note(magnitude_as_frequency)

    """
     Step 2: Adjust the two variables below to select which set of notes to play: temperature_notes, 
     humidity_notes, uv_notes, and magnitude_notes. Also, adjust which instrument to play by selecting 1 of the 128 options.
     """

    # set this equal to temperature_notes,
    # humidity_notes, uv_notes, or magnitude_notes
    notes_to_play = humidity_notes

    # set this equal to one of the 128 instrument options
    instrument_to_play = 'Woodblock'

    # play the notes with a selected instrument
    # adjust note to have duration. Set in terms of musical "bars".
    notes_to_play = notes_to_play.set(duration=.15)
    play(notes_to_play, wait=False, instrument=instrument_to_play, save_as_file=False)

ser.close()

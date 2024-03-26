# INSTRUMENTS = {
#     'Acoustic Grand Piano': 1,
#     'Bright Acoustic Piano': 2,
#     'Electric Grand Piano': 3,
#     'Honky-tonk Piano': 4,
#     'Electric Piano 1': 5,
#     'Electric Piano 2': 6,
#     'Harpsichord': 7,
#     'Clavi': 8,
#     'Celesta': 9,
#     'Glockenspiel': 10,
#     'Music Box': 11,
#     'Vibraphone': 12,
#     'Marimba': 13,
#     'Xylophone': 14,
#     'Tubular Bells': 15,
#     'Dulcimer': 16,
#     'Drawbar Organ': 17,
#     'Percussive Organ': 18,
#     'Rock Organ': 19,
#     'Church Organ': 20,
#     'Reed Organ': 21,
#     'Accordion': 22,
#     'Harmonica': 23,
#     'Tango Accordion': 24,
#     'Acoustic Guitar (nylon)': 25,
#     'Acoustic Guitar (steel)': 26,
#     'Electric Guitar (jazz)': 27,
#     'Electric Guitar (clean)': 28,
#     'Electric Guitar (muted)': 29,
#     'Overdriven Guitar': 30,
#     'Distortion Guitar': 31,
#     'Guitar harmonics': 32,
#     'Acoustic Bass': 33,
#     'Electric Bass (finger)': 34,
#     'Electric Bass (pick)': 35,
#     'Fretless Bass': 36,
#     'Slap Bass 1': 37,
#     'Slap Bass 2': 38,
#     'Synth Bass 1': 39,
#     'Synth Bass 2': 40,
#     'Violin': 41,
#     'Viola': 42,
#     'Cello': 43,
#     'Contrabass': 44,
#     'Tremolo Strings': 45,
#     'Pizzicato Strings': 46,
#     'Orchestral Harp': 47,
#     'Timpani': 48,
#     'String Ensemble 1': 49,
#     'String Ensemble 2': 50,
#     'SynthStrings 1': 51,
#     'SynthStrings 2': 52,
#     'Choir Aahs': 53,
#     'Voice Oohs': 54,
#     'Synth Voice': 55,
#     'Orchestra Hit': 56,
#     'Trumpet': 57,
#     'Trombone': 58,
#     'Tuba': 59,
#     'Muted Trumpet': 60,
#     'French Horn': 61,
#     'Brass Section': 62,
#     'SynthBrass 1': 63,
#     'SynthBrass 2': 64,
#     'Soprano Sax': 65,
#     'Alto Sax': 66,
#     'Tenor Sax': 67,
#     'Baritone Sax': 68,
#     'Oboe': 69,
#     'English Horn': 70,
#     'Bassoon': 71,
#     'Clarinet': 72,
#     'Piccolo': 73,
#     'Flute': 74,
#     'Recorder': 75,
#     'Pan Flute': 76,
#     'Blown Bottle': 77,
#     'Shakuhachi': 78,
#     'Whistle': 79,
#     'Ocarina': 80,
#     'Lead 1 (square)': 81,
#     'Lead 2 (sawtooth)': 82,
#     'Lead 3 (calliope)': 83,
#     'Lead 4 (chiff)': 84,
#     'Lead 5 (charang)': 85,
#     'Lead 6 (voice)': 86,
#     'Lead 7 (fifths)': 87,
#     'Lead 8 (bass + lead)': 88,
#     'Pad 1 (new age)': 89,
#     'Pad 2 (warm)': 90,
#     'Pad 3 (polysynth)': 91,
#     'Pad 4 (choir)': 92,
#     'Pad 5 (bowed)': 93,
#     'Pad 6 (metallic)': 94,
#     'Pad 7 (halo)': 95,
#     'Pad 8 (sweep)': 96,
#     'FX 1 (rain)': 97,
#     'FX 2 (soundtrack)': 98,
#     'FX 3 (crystal)': 99,
#     'FX 4 (atmosphere)': 100,
#     'FX 5 (brightness)': 101,
#     'FX 6 (goblins)': 102,
#     'FX 7 (echoes)': 103,
#     'FX 8 (sci-fi)': 104,
#     'Sitar': 105,
#     'Banjo': 106,
#     'Shamisen': 107,
#     'Koto': 108,
#     'Kalimba': 109,
#     'Bag pipe': 110,
#     'Fiddle': 111,
#     'Shanai': 112,
#     'Tinkle Bell': 113,
#     'Agogo': 114,
#     'Steel Drums': 115,
#     'Woodblock': 116,
#     'Taiko Drum': 117,
#     'Melodic Tom': 118,
#     'Synth Drum': 119,
#     'Reverse Cymbal': 120,
#     'Guitar Fret Noise': 121,
#     'Breath Noise': 122,
#     'Seashore': 123,
#     'Bird Tweet': 124,
#     'Telephone Ring': 125,
#     'Helicopter': 126,
#     'Applause': 127,
#     'Gunshot': 128
# }

# include all the relevant libraries
from time import time
from musicpy.musicpy import play, freq_to_note
import serial
from serial.tools.list_ports import comports


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
Step 1: Determine which Serial/USB port is in use. This will vary between Windows, Mac, and Linux systems.
If the port cannot be found then an error message will appear listing the various ports available. Keep 
adjusting the variable portName until the correct one is found.
"""
portName = '/dev/cu.usbserial-110'
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

# set duration for the loop
duration = 10

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
    uv = float(values[3])
    x_accel = float(values[4])
    y_accel = float(values[5])
    z_accel = float(values[6])

    """
    Step 2: All data from the sensor board has been read in. Only one sensor can be "played" at a time.
    In the section below use the scale() method, or develop your own equation, to map the sensor data range
    into a musical range. For example: UV may range from 0 to 10. This can be mapped into a reasonable musical 
    range of 300 - 700 Hz.
    
    Adjust the value= parameter to select different sensors.
    Adjust the input_low and input_high parameters to correspond to reasonable upper and lower bounds for the sensor
    Adjust the output_low and output_high parameter to map to suitable frequencies. The human hearing range is ~20Hz to 20,000 Hz
    """

    # scale the sensor data to appropriate values
    accel_data_as_frequency = scale(value=x_accel, input_low=-2, input_high=2, output_low=300, output_high=700)

    # use the built-in freq_to_note method to convert from a frequency (Hertz)
    # to a note (Note, Octave)
    accel_notes = freq_to_note(accel_data_as_frequency)

    """
    Step 3: The sensor data has not been converted into notes that the musicpy library can understand. 
    Adjust the instrument= parameter to be one of the 128x instruments available.
    """

    # play the notes with a selected instrument
    play(accel_notes, wait=False, instrument='Marimba')

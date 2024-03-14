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

from time import time

from musicpy.musicpy import play, freq_to_note
from musicpy.structures import note

import serial
from serial.tools.list_ports import comports


def scale(value, input_low, input_high, output_low, output_high):
    if value < input_low:
        value = input_high

    elif value > input_high:
        value = input_high

    return (value - input_low) / (input_high - input_low) * (output_high - output_low) + output_low


# set parameters for serial port
portName = '/dev/cu.usbserial-10'
# portName = 'COM3'
baudRate = 9600

# attempt to open port
try:
    ser = serial.Serial(portName, baudRate)
    print("Opening port " + ser.name)

# if fail, print a helpful message
except:
    print("Couldn't open port. Try changing portName to one of the options below:")
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
    # wait until we have an '!' from the Arduino
    bytes = ser.readline()

    received = bytes.decode('utf-8')
    received = received.replace('\r', '').replace('\n', '')

    values = received.split(",")

    # capture all sensor data
    temp = float(values[0])
    humidity = float(values[1])
    pressure = float(values[2])
    uv = float(values[3])
    x_accel = float(values[4])
    y_accel = float(values[5])
    z_accel = float(values[6])

    accel_freq = scale(x_accel, -2, 2, 300, 700)

    # new_notes = freq_to_note(temp * 15)
    new_notes = freq_to_note(accel_freq)

    print(temp, new_notes)

    play(new_notes, wait=False, instrument='Marimba')

# b = note('A', 3)
# play(b, wait=True, instrument='Violin')

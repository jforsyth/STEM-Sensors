import serial
from serial.tools.list_ports import comports


def find_serial_port(baud_rate=9600):
    serial_port_name=''
    print('Scanning serial ports...')
    ports_list = comports()
    for port_candidate in ports_list:
        port_name = port_candidate.device

        try:
            print("Attempting port " + port_name)
            port = serial.Serial(port_name, baudrate=baud_rate, timeout=3)

            line = port.readline()

            if len(line) == 0:
                continue
            else:
                serial_port_name = port_name
                print('Using port ', port_name)
                return port
        except:
            print("Exception occurred opening port: ",port_name)

    print('Could not find a port to open. Please restart board and try again.')
    exit(-1)


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

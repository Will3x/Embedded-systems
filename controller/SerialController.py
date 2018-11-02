from serial import *
from model import SensordataModel
import serial.tools.list_ports
import re


class SerialController:

    arduino_connections = None
    dict_values = None
    ser = None
    arduino_connections2 = None

    @classmethod
    def setup(cls):
        cls.arduino_connections = {1: '', 2: '', 3: '', 4: '', 5: ''}
        cls.arduino_connections2 = {1: '', 2: '', 3: '', 4: '', 5: ''}
        cls.dict_values = {1: (), 2: (), 3: (), 4: (), 5: (), }
        cls.sensor_model = SensordataModel.SensordataModel()

        cls.open_port()

    @classmethod
    def open_port(cls):
        print('Attempting to connect...')
        try:
            com = cls.find_ports()[0][0]
            cls.ser = Serial(com, 9600, timeout=5)
        except (SerialException, KeyError, IndexError):
            return
        print('Connected to {}!'.format(com))

    @classmethod
    def read(cls):
        """ RECIEVE INCOMING DATA FROM SERIAL PORT """
        try:
            cls.ser.readline()
        except (AttributeError, SerialException):
            print("Couldn't read from serial")
            cls.open_port()
            return

        ports = cls.arduino_connections2

        for count, port in ports.items():
            if port != '':
                try:
                    line = cls.ser.readline().decode('ascii')

                    match = re.findall('(\d+)', line)
                    cls.dict_values[count] = {'t': match[0], 'l': match[1], 'a': match[2]} if len(match) == 3 else None
                    cls.ser.flushInput()
                except SerialException as e:
                    print('SerialController.read(): {}'.format(e))

        return cls.dict_values

    @classmethod
    def find_ports(cls):
        return [tuple(p) for p in list(serial.tools.list_ports.comports()) if 'VID:PID=2341' in p[2]]

    @classmethod
    def check_connection(cls):
        """ Check if Arduino is connected. If so, add to dictionary.
        This function is called every 2 sec from tick(). """
        my_ports = cls.find_ports()

        for id, port in enumerate(my_ports, 1):
            cls.arduino_connections[id] = [port if port != '' else '']

        cls.arduino_connections2.update(cls.arduino_connections)

        return cls.arduino_connections

    @classmethod
    def write(cls, data):
        """ SEND DATA TO SERIAL PORT """
        cls.ser.write(data)

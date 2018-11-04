from serial import *
from model import SensordataModel
import serial.tools.list_ports
import re


class SerialController:

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
            cls.ser = Serial(com, 9600, timeout=2)
            cls.ser.flushInput()
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
            return {1: (), 2: (), 3: (), 4: (), 5: (), }

        ports = cls.arduino_connections2

        for count, port in ports.items():
            if port != '':
                try:
                    line = cls.ser.readline().decode('ascii')
                    cls.ser.flushInput()
                    print(line, end='')

                    match = re.findall('(\d+)', line)
                    if len(match) == 3:
                        cls.dict_values[count] = {'t': match[0], 'l': match[1], 'a': match[2]}
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
            cls.arduino_connections[id] = port

        cls.arduino_connections2.update(cls.arduino_connections)

        return cls.arduino_connections

    @classmethod
    def write(cls, instruction, value):
        """ SEND DATA TO SERIAL PORT """
        if isinstance(value, tuple) and isinstance(instruction, list):
            for x in range(len(instruction)):
                print('writing instruction {} with value {} to serial.'.format(instruction[x], value[x]))
                cls.ser.write(str(instruction[x]).encode())
                cls.ser.write(value[x].encode())
                cls.ser.write(b'/')
        else:
            print('writing instruction {} with value {} to serial.'.format(instruction, value[0]))
            cls.ser.write(str(instruction).encode())
            cls.ser.write(value[0].encode())
            cls.ser.write(b'/')

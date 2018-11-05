from serial import *
import serial.tools.list_ports
import re


class SerialController:

    @classmethod
    def setup(cls):
        cls.dict_values = {1: (), 2: (), 3: (), 4: (), 5: ()}
        cls.connections = {1: '', 2: '', 3: '', 4: '', 5: ''}
        cls.ser = {1: '', 2: '', 3: '', 4: '', 5: ''}

    @classmethod
    def current_values(cls, values=None):
        """ Returns all current values. If new values are added as parameter: update the values.
        Acts as a getter for accessing values """
        if values is None:
            return cls.dict_values
        cls.dict_values = values.copy()

    @classmethod
    def update_ports(cls):
        """ Opens all COM ports that have been scanned and found. """
        connections = cls.check_connection(cls.connections)
        [cls.open_port(num, connections[num][0]) for num in connections if connections[num] != '']
        return connections

    @classmethod
    def open_port(cls, num, com):
        """ Attempts and opens port with given COM and device id (NUM).
        Throws SerialException if port is already open. """
        try:
            cls.ser[num] = (Serial(com, 9600, timeout=2))
            print('Connection to {}!'.format(com))
            cls.ser[num].flushInput()
        except SerialException:
            pass

    @classmethod
    def close_port(cls, port, com):
        print('Closing {}'.format(com))
        port.close()

    @classmethod
    def read(cls):
        """ RECIEVE INCOMING DATA FROM SERIAL PORT """
        ports = cls.update_ports()
        for count, port in ports.items():
            if port != '':
                line = cls.ser[count].readline().decode('ascii')
                cls.ser[count].flushInput()
                cls.dict_values = cls.filter_on_read(line, count, cls.dict_values)

        cls.current_values(cls.dict_values)

    @classmethod
    def filter_on_read(cls, line, count, dict_values):
        """ Filters data to single out values read from serial. """
        match = re.findall('(\d+)', line)

        if len(match) == 3:
            dict_values[count] = {'t': match[0], 'l': match[1], 'a': match[2]}

        return dict_values

    @classmethod
    def find_ports(cls):
        """ Scans all ports and looks for Arduino connections. """
        return [tuple(p) for p in list(serial.tools.list_ports.comports()) if 'VID:PID=2341' in p[2]]

    @classmethod
    def check_connection(cls, con_dict):
        """ Check if Arduino is connected. If so, add to dictionary.
        This function is called every 2 sec from tick(). """
        my_ports = cls.find_ports()
        con_dict.update({id, port} for id, port in enumerate(my_ports, 1))

        return con_dict

    @classmethod
    def write(cls, device, instruction, value):
        """ SEND DATA TO SERIAL PORT """
        if isinstance(value, tuple) and isinstance(instruction, list):
            for x in range(len(instruction)):
                print('writing instruction {} with value {} from device {} to serial.'.format(device, instruction[x], value[x]))
                cls.ser[device].write(str(instruction[x]).encode())
                cls.ser[device].write(value[x].encode())
                cls.ser[device].write(b'/')
        else:
            print('writing instruction {} with value {} from device {} to serial.'.format(device, instruction, value[0]))
            cls.ser[device].write(str(instruction).encode())
            cls.ser[device].write(value[0].encode())
            cls.ser[device].write(b'/')

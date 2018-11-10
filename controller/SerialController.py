from serial import *
import serial.tools.list_ports
import re
import sys


class SerialController:

    @classmethod
    def setup(cls):
        cls.dict_values = {1: None, 2: None, 3: None, 4: None, 5: None}
        cls.connections, cls.ser = cls.dict_values.copy(), cls.dict_values.copy()

    @classmethod
    def current_values(cls, values=None):
        """ Returns all current values. If new values are added as parameter: update the values.
        Acts as a getter for accessing values """
        if values is None:
            return cls.dict_values

        cls.dict_values = values.copy()

    @classmethod
    def current_connections(cls, new_con=None):
        """ Returns all current connections. If new values are added as parameter: update the values.
        Acts as a getter for accessing connections """
        if new_con is None:
            return cls.connections

        cls.connections = new_con.copy()

    @classmethod
    def update_ports(cls):
        """ Opens all COM ports that have been scanned and found and closes all that do not respond,
        thus lost connection. """
        cls.check_connection()
        connections = cls.current_connections()

        for num, con in cls.ser.items():
            if con is not None:
                try:
                    con.read()
                except serial.serialutil.SerialException:
                    cls.ser[num] = None
                    cls.close_port(con)

        for index in connections:
            if connections[index] is not None and cls.ser[index] is None:
                cls.open_port(index, connections[index][0])

    @classmethod
    def open_port(cls, num, com):
        """ Attempts and opens port with given COM and device id (NUM).
        Throws SerialException if port is already open. """
        try:
            cls.ser[num] = (Serial(com, 9600, timeout=2))
            print('Connected to {}!'.format(com))
            cls.ser[num].flushInput()
        except SerialException:
            pass

    @classmethod
    def close_port(cls, port, com='COM'):
        print("Lost connection!")
        print('Closing {}'.format(com))
        port.close()

    @classmethod
    def read(cls):
        """ RECIEVE INCOMING DATA FROM SERIAL PORT """
        cls.update_ports()
        connections = cls.current_connections()

        for count, connection in connections.items():
            if connection is not None:
                try:
                    line = cls.ser[count].readline().decode('ascii')
                except AttributeError:
                    sys.exit('Error: another process might already be running.')

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
        return [tuple(p) for p in serial.tools.list_ports.comports() if 'VID:PID=2341' in p[2]]

    @classmethod
    def check_connection(cls):
        """ Check if Arduino is connected. If so, add to dictionary.
        This function is called every 2 sec from tick(). """
        my_ports = cls.find_ports()
        con_dict = {1: None, 2: None, 3: None, 4: None, 5: None}

        for index, port in enumerate(my_ports, 1):
            con_dict[index] = port

        cls.current_connections(con_dict)

    @classmethod
    def write(cls, device, instruction, value=None):
        """ SEND DATA TO SERIAL PORT """
        print('writing instruction {} with value(s) {} to device {}.'.format(instruction, value, device))
        cls.ser[device].write(str(instruction).encode())

        if value is not None:
            for num in range(len(value)):
                int_val = [int(d) for d in value[num]]

                [int_val.insert(0, 0) for x in range(2 - len(int_val)) if instruction == 3]
                [int_val.insert(0, 0) for x in range(3-len(int_val)) if instruction == 7]

                for d in int_val:
                    cls.ser[device].write(str(d).encode())

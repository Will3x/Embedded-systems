from serial import *
import serial.tools.list_ports
import re


class SerialController:

    @classmethod
    def setup(cls):
        cls.arduino_connections = {1: '', 2: '', 3: '', 4: '', 5: ''}
        cls.dict_values = {1: (), 2: (), 3: (), 4: (), 5: (), }
        cls.ser = {1: '', 2: '', 3: '', 4: '', 5: ''}

    @classmethod
    def update_ports(cls):
        connections = cls.check_connection()
        [cls.open_port(num, connections[num][0]) for num in cls.check_connection() if connections[num] != '']
        return connections

    @classmethod
    def open_port(cls, num, com):
        try:
            cls.ser[num] = (Serial(com, 9600, timeout=2))
            print('Connection to {}!'.format(com))
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
                print(line)
                cls.ser[count].flushInput()
                cls.close_port(cls.ser[count], port[0]) if len(line) == 0 else None

                match = re.findall('(\d+)', line)

                if len(match) == 3:
                    cls.dict_values[count] = {'t': match[0], 'l': match[1], 'a': match[2]}

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
            cls.arduino_connections.update({id: port})

        return cls.arduino_connections

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

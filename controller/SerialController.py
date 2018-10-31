from serial import *
from model import SensordataModel
import serial.tools.list_ports


class SerialController:

    arduino_connections = {1: '', 2: '', 3: '', 4: '', 5: ''}
    arduino_connections2 = {1: '', 2: '', 3: '', 4: '', 5: ''}
    dict_values = {1: (), 2: (), 3: (), 4: (), 5: (), }
    sensor_model = SensordataModel.SensordataModel()
    com_port = set()

    try:
        ser = Serial("COM5", 9600, timeout=None)
        print('Connected!')
    except SerialException as e:
        pass

    @staticmethod
    def openPort():
        try:
            com = SerialController.com_port.pop()
            SerialController.ser = Serial(com, 9600, timeout=5)
            SerialController.com_port.clear()
        except (SerialException, KeyError):
            return
        print('Connected!')

    @staticmethod
    def read():
        """ RECIEVE INCOMING DATA FROM SERIAL PORT """
        try:
            SerialController.ser.readline()
        except (AttributeError, SerialException):
            print('Attempting to connect...')
            SerialController.openPort()
            return

        ports = SerialController.arduino_connections2
        filter = ['Temp', 'LDR', 'Echo', 'Trig', ' : ']

        for count, port in ports.items():
            if port != '':
                try:
                    line = SerialController.ser.readline().decode('ascii')

                    for x in filter:
                        if x in line:
                            line = line.replace(x, '')

                    values = line.split()

                    if len(values) == 4:
                        values_dict = {'temp': values[0], 'ldr': values[1], 'echo': values[2], 'trig': values[3]}
                        SerialController.dict_values[count] = values_dict
                        print(SerialController.dict_values)

                    SerialController.ser.flushInput()
                except SerialException:
                    pass

        return SerialController.dict_values

    @staticmethod
    def check_connection():
        """ Check if Arduino is connected. If so, add to dictionary.
        This function is called every 2 sec from tick(). """
        keywords = ['Serial', 'Serieel', 'Arduino']
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports()) for x in keywords if x in p[1]]

        count = 1
        for port in myports:
            if port != '':
                SerialController.arduino_connections[count] = port
                SerialController.com_port.add(SerialController.arduino_connections[count][0])
            else:
                SerialController.arduino_connections[count] = ''
            count += 1

        SerialController.arduino_connections2.update(SerialController.arduino_connections)

        return SerialController.arduino_connections

    @staticmethod
    def write(data):
        """ SEND DATA TO SERIAL PORT """
        SerialController.ser.write(data)

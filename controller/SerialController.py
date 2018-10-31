from serial import *
from model import SensordataModel
import serial.tools.list_ports


class SerialController:

    arduino_connections = {1: '', 2: '', 3: '', 4: '', 5: ''}
    arduino_connections2 = {1: '', 2: '', 3: '', 4: '', 5: ''}
    sensor_model = SensordataModel.SensordataModel()
    try:
        ser = Serial("COM5", 9600, timeout=None)
        print('Connected!')
    except SerialException:
        pass

    @staticmethod
    def openPort():
        try:
            SerialController.ser = Serial("COM5", 9600, timeout=5)
            print('Connected!')
        except SerialException:
            pass

    @staticmethod
    def read():
        """ RECIEVE INCOMING DATA FROM SERIAL PORT """
        try:
            SerialController.ser.readline()
        except (AttributeError, SerialException) as e:
            print('Attempting to connect...')
            SerialController.openPort()
            return

        ports = SerialController.arduino_connections2
        filter = ['Temp', 'LDR', 'Echo', 'Trig', ' : ']
        my_dict = {1: (), 2: (), 3: (), 4: (), 5: (), }

        for count, port in ports.items():
            if port != '':
                try:
                    line = SerialController.ser.readline().decode('ascii')

                    for x in filter:
                        if x in line:
                            line = line.replace(x, '')

                    values = line.split()

                    values_dict = {'temp': values[0], 'ldr': values[1], 'echo': values[2], 'trig': values[3]}
                    my_dict[count] = values_dict

                    SerialController.ser.flushInput()
                except SerialException:
                    pass

        return my_dict

    @staticmethod
    def check_connection():
        """ Check if Arduino is connected. If so, add to dictionary.
        This function is called every 2 sec from tick(). """
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports()) if p[1] == 'USB Serial Device (COM5)']

        count = 1
        for port in myports:
            if port != '':
                SerialController.arduino_connections[count] = port
            else:
                SerialController.arduino_connections[count] = ''
            count += 1

        SerialController.arduino_connections2.update(SerialController.arduino_connections)

        return SerialController.arduino_connections

    @staticmethod
    def write(cls, data):
        """ SEND DATA TO SERIAL PORT """
        cls.ser.write(data)

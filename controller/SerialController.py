from serial import *
from model import SensordataModel
import serial.tools.list_ports


class SerialController:

    arduino_connections = {1: '', 2: '', 3: '', 4: '', 5: ''}
    try:
        ser = Serial("COM5", 9600)
    except SerialException:
        print('Error: Could not open port "COM5"')

    sensor_model = SensordataModel.SensordataModel()

    @staticmethod
    def read():
        """ RECIEVE INCOMING DATA FROM SERIAL PORT """
        if SerialController.ser.isOpen:
            while True:  # maybe niet nodig omdat Graphview (als het goed is) deze data gaat opvragen in een loop.
                line = SerialController.ser.readline().decode('ascii')
                # ser.flushInput()
                print(line)

    @staticmethod
    def check_connection():
        """ Check if Arduino is connected. If so, add to dictionary.
        This function is called every 2 sec from tick(). """
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]

        count = 1
        for ports in myports:
            if ports != '':
                SerialController.arduino_connections[count] = ports
            else:
                SerialController.arduino_connections[count] = ''
            count += 1

        return SerialController.arduino_connections

    @staticmethod
    def write(cls, data):
        """ SEND DATA TO SERIAL PORT """
        cls.ser.write(data)

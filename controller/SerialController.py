from serial import *
from model import SensordataModel


class SerialController:

    @staticmethod
    def __init__(cls):
        cls.ser = Serial("COM5", 9600, timeout=1)
        cls.sensor_model = SensordataModel.SensordataModel()

    @staticmethod
    def read(cls):
        """ RECIEVE INCOMING DATA FROM SERIAL PORT """
        if cls.isOpen:
            while True:  # maybe niet nodig omdat Graphview (als het goed is) deze data gaat opvragen in een loop.
                line = cls.ser.readline().decode('ascii')
                # ser.flushInput()
                print(line)

    @staticmethod
    def isOpen(cls):
        return len(cls.ser.read()) > 1

    @staticmethod
    def write(cls, data):
        """ SEND DATA TO SERIAL PORT """
        cls.ser.write(data)

    @staticmethod
    def updateView(cls):
        pass

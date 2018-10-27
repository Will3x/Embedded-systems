from serial import *

ser = Serial("COM5", 9600, timeout=1)

if ser.isOpen():
    while True:
        ser.readline().decode('ascii')
        print(ser)
        """ Send incoming data to appropriate model -> Do calculations -> ... -> Send to view."""


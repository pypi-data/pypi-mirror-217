#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from serial.tools import list_ports
from interfaces import serial
import interfaces
import time

class SerialPort(interfaces.serial.Serial):
    def __init__(self, port:str, baudrate:str, vid=-1, pid=-1):
        if baudrate is None:
            raise ValueError('Invalid baudrate!')

        if (port is None or port == '') and vid==-1 and pid==-1:
            raise ValueError('Invalid input parameters!')

        if port is None:
            device_list = list_ports.comports()
            for device in device_list:
                if (device.vid != None or device.pid != None):
                    if (device.vid == vid and device.pid == pid):
                        port = device.device
                        break
                    port = None

        if port is None:
            raise ValueError('Serial port not found!')

        self.__is_connected = False
        try:
            self.__serial = serial.serial_for_url(port, baudrate=int(baudrate), do_not_open=True)
            self.__serial.write_timeout = 0
            self.__serial.timeout = 0
        except ValueError:
            raise "Baudrate is out of range!"

    def __del__(self):
        self.close()

    def open(self):
        try:
            self.__serial.open()
        except serial.SerialException:
            raise "Serial port could not be found or could not be configured!"
        self.__is_connected = True

    def is_open(self):
        return self.__is_connected

    def close(self):
        if self.__is_connected:
            self.__is_connected = False
            self.__serial.cancel_read()
            self.__serial.cancel_write()
            self.__serial.close()

    def write(self, payload):
        if self.__is_connected:
            self.__serial.write(payload)

    def read(self):
        if self.__is_connected:
            time.sleep(0.01)
            return self.__serial.read()
        raise "Serial is not opened!"

    def subscribe(self, callback):
        pass

    def unsubscribe(self, callback):
        pass

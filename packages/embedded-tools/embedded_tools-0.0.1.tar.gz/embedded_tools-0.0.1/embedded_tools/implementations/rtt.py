#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from interfaces import serial
import subprocess
import usb.core
import usb.util
import telnetlib
import time

class Rtt(serial.Serial):
    def __init__(self, uc:str, transport:str, serial_number:str, host='localhost', port=19021):
        if uc is None or transport is None or serial_number is None:
            raise ValueError('Invalid input parameters!')

        dev = usb.core.find(idVendor=0x1366, idProduct=0x0105)
        if dev is None:
            raise ValueError('Jlink not found')

        self.__microcontroller = uc
        self.__transport = transport
        self.__sn = serial_number
        self.__is_connected = False
        self.__host = host
        self.__port = port
        self.__telnet = telnetlib.Telnet(timeout=1)
        self.__gdb_server = None

    def __del__(self):
        self.close()
        time.sleep(2)

    def open(self):
        args = "JLinkGDBServerCLExe -singlerun -nogui -nohalt"
        args += " -device " + self.__microcontroller.upper()
        args += " -if " + self.__transport.upper()
        args += " -port 50000 -swoport 50001 -telnetport 50002"
        args += " -select usb=" + self.__sn
        args += " -RTTTelnetPort " + str(self.__port)

        self.__gdb_server = subprocess.Popen(args.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)

        try:
            self.__telnet.open(self.__host, self.__port)
            time.sleep(2)
        except ConnectionRefusedError:
            self.__gdb_server.terminate()
            raise ConnectionRefusedError(
                f"Could not connect to {self.__host}:{self.__port}."
                " Are you sure that the JLink is running?"
                " You can run it with 'JLink -Device <DEVICE> -If <IF> -AutoConnect 1 -Speed <kHz>'"
            )
        self.__is_connected = True

    def is_open(self):
        return self.__is_connected

    def close(self):
        if self.__is_connected:
            self.__is_connected = False
            self.__telnet.close()
            self.__gdb_server.terminate()

    def write(self, payload):
        if self.__is_connected:
            self.__telnet.write(self.__to_bytes(payload))

    def read(self):
        try:
            rx_data = self.__telnet.read_very_eager()
        except ConnectionResetError:
            return "\x00"

        time.sleep(0.01)

        return rx_data

    def subscribe(self, callback):
        pass

    def unsubscribe(self, callback):
        pass

    def __to_bytes(self, seq):
        """convert a sequence to a bytes type"""
        if isinstance(seq, bytes):
            return seq
        elif isinstance(seq, bytearray):
            return bytes(seq)
        elif isinstance(seq, memoryview):
            return seq.tobytes()
        else:
            # handle list of integers and bytes (one or more items) for Python 2 and 3
            return bytes(bytearray(seq))

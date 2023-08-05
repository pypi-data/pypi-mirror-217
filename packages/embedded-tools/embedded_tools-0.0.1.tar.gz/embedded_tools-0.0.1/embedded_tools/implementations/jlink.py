#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import os
from datetime import datetime
from interfaces import debugger
import subprocess
import usb.core
import usb.util

class JLink(debugger.Debugger):
    def __init__(self, uc:str, transport:str, speed:str, serial_number:str):
        if uc is None or transport is None or speed is None or serial_number is None:
            raise ValueError('Invalid input parameters!')

        dev = usb.core.find(idVendor=0x1366, idProduct=0x0105)
        if dev is None:
            raise ValueError('Jlink not found')

        self.__microcontroller = uc
        self.__interface = transport
        self.__speed = speed
        self.__serial_number = serial_number
        self.__script = '/tmp/micro_' + str(datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")) + '.jlink'

    def reset(self):
        return self.__execute("r\nq\n")

    def load_bin(self, file:str, address:int):
        if '.bin' in file:
            return self.__execute("rx 200\nh\nLoadFile " + file + ", " + str(hex(address)))
        else:
            raise ValueError('File shoule be .bin!')

    def load(self, file:str):
        if '.hex' in file:
            return self.__execute("rx 200\nh\nLoadFile " + file + "\n")
        else:
            raise ValueError('File shoule be .hex!')

    def erase(self, address:int, length:int):
        return self.__execute("h\nerase " + str(hex(address)) + ", " + str(hex(address + length)) + "\ng\nq")

    def erase_all(self):
        return self.__execute("h\nerase\ng\nq")

    def write_ram(self, address:int, payload:int):
        return self.__execute("mww " + str(hex(address)) + " " + str(hex(payload)))

    def read_ram(self, address:int):
        return self.__execute("mdw " + str(hex(address)))

    def start_gdb(self):
        pass

    def stop_gdb(self):
        pass

    def __execute(self, command:str, timeout_sec=120):
        file = open(self.__script, "w")
        self.__ocd_add_header(file)
        self.__ocd_add_command(file, command)
        self.__ocd_add_footer(file)

        args = "JLinkExe"
        args += " -device " + self.__microcontroller.upper()
        args += " -if " + self.__interface.upper()
        args += " -speed " + self.__speed
        args += " -autoconnect 1"
        args += " -commanderscript " + self.__script

        process = subprocess.Popen(args.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        try:
            output, err = process.communicate(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            process.kill()
            output, err = process.communicate()
            raise 'JLink timeout!'

        os.remove(self.__script)

        return output, err

    def __ocd_add_header(self, file):
        file.write("h\n")

    def __ocd_add_command(self, file, command:str):
        file.write(command + "\n")

    def __ocd_add_footer(self, file):
        file.write("g\nq\n")
        file.close()

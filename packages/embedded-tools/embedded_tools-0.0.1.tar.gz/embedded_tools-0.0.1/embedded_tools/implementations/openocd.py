#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from ctypes.wintypes import tagMSG
from datetime import datetime
from enum import Enum
from interfaces import debugger
import os
import subprocess
import usb.core
import usb.util

class Microcontroller(Enum):
    TM4C123GH6PM = 'tm4c123gh6pm'
    TM4C1294NCPDT = 'tm4c1294ncpdt'
    STM32F407VG = 'stm32f407vg'
    STM32F429ZI = 'stm32f429zi'

class Interface(Enum):
    TI_ICDI = 'ti-icdi'
    STLINK = 'stlink'
    JLINK = 'jlink'
    CMSIS_DAP = 'cmsis-dap'

class Transport(Enum):
    NONE = None
    JTAG = 'hla_jtag'
    SWD = 'hla_swd'

class OpenOCD(debugger.Debugger):
    def __init__(self, microcontroller: Microcontroller, interface:Interface, transport:Transport):

        if interface == Interface.JLINK:
            dev = usb.core.find(idVendor=0x1366, idProduct=0x0105)
            if dev is None:
                raise ValueError('Jlink not found')
        elif interface == Interface.TI_ICDI:
            dev = usb.core.find(idVendor=0x1cbe, idProduct=0x00fd)
            if dev is None:
                raise ValueError('ti-icdi not found')

        self.__microcontroller = self.__get_microcontroller(microcontroller)
        self.__interface = interface
        self.__transport = transport
        self.__uc_script = '/tmp/micro_' + str(datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")) + '.cfg'
        self.__ocd_script = '/tmp/ocd_desc.ocd'
        self.__uc_file = open(self.__uc_script, "w")
        self.__populate_micro_file()

    def __del__(self):
        os.remove(self.__uc_script)

    def reset(self):
        return self.__execute("soft_reset_halt\nresume")

    def load_bin(self, file:str, address:int):
        return self.__execute("program " + file + " " + str(hex(address)))

    def load(self, file:str):
        return self.__execute("program " + file)

    def erase(self, address:int, length:int):
        return self.__execute("flash erase_address " + str(hex(address)) + " " + str(hex(length)))

    def erase_all(self):
        return self.__execute("flash erase_sector 0 0 last")

    def write_ram(self, address:int, payload:int):
        return self.__execute("mww " + str(hex(address)) + " " + str(hex(payload)))

    def read_ram(self, address:int):
        return self.__execute("mdw " + str(hex(address)))

    def start_gdb(self):
        pass

    def stop_gdb(self):
        pass

    def __get_microcontroller(self, microcontroller:Microcontroller ):
        dict = {}

        dict[Microcontroller.TM4C123GH6PM] = ('tm4c123gh6pm', '0x8000', 'stellaris')
        dict[Microcontroller.TM4C1294NCPDT] = ('tm4c1294ncpdt', '0x8000', 'stellaris')
        dict[Microcontroller.STM32F407VG] = (None, '0x10000', 'stm32f4x')
        dict[Microcontroller.STM32F429ZI] = (None, '0x20000', 'stm32f4x')

        return dict.get(microcontroller)

    def __populate_micro_file(self):

        micro = self.__microcontroller[0]
        workarea = self.__microcontroller[1]
        target = self.__microcontroller[2]

        self.__uc_file.write("source [find /usr/share/openocd/scripts/interface/" + self.__interface.value + ".cfg]\n")
        self.__uc_file.write("transport select " + self.__transport.value + "\n")
        if workarea is not None:
            self.__uc_file.write("set WORKAREASIZE " + workarea + "\n")
        if micro is not None:
            self.__uc_file.write("set CHIPNAME " + micro + "\n")
        if target is not None:
            self.__uc_file.write("source [find /usr/share/openocd/scripts/target/" + target + ".cfg]\n")
        self.__uc_file.close()


    def __execute(self, command:str, timeout_sec=120):
        file = open(self.__ocd_script, "w")
        self.__ocd_add_header(file)
        self.__ocd_add_command(file, command)
        self.__ocd_add_footer(file)

        args = "openocd -f " + self.__uc_script + " -f " + self.__ocd_script
        process = subprocess.Popen(args.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        try:
            output, err = process.communicate(timeout=timeout_sec)
        except subprocess.TimeoutExpired:
            process.kill()
            output, err = process.communicate()
            raise 'OpenOCD timeout!'

        os.remove(self.__ocd_script)

        return output, err

    def __ocd_add_header(self, file):
        file.write("init\n")
        file.write("halt\n")

    def __ocd_add_command(self, file, command:str):
        file.write(command + "\n")

    def __ocd_add_footer(self, file):
        file.write("reset\n")
        file.write("shutdown\n")
        file.close()

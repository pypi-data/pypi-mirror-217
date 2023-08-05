#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import abc

class Debugger(abc.ABC):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def reset(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def load_bin(self, file:str, address:int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def load(self, file:str):
        raise NotImplementedError

    @abc.abstractclassmethod
    def erase(self, address:int, length:int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def erase_all(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def write_ram(self, address:int, payload:int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def read_ram(self, address:int):
        raise NotImplementedError

    @abc.abstractclassmethod
    def start_gdb(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def stop_gdb(self):
        raise NotImplementedError

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import abc

class Serial(abc.ABC):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def open(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def is_open(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def close(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def write(self, payload):
        raise NotImplementedError

    @abc.abstractclassmethod
    def read(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def subscribe(self, callback):
        raise NotImplementedError

    @abc.abstractclassmethod
    def unsubscribe(self, callback):
        raise NotImplementedError

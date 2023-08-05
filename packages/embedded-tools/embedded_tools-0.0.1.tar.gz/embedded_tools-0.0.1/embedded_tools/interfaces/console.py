#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import sys

class ConsoleBase(object):
    """OS abstraction for console (input/output codec, no echo)"""

    def __init__(self, miniterm):
        self.miniterm = miniterm
        if sys.version_info >= (3, 0):
            self.byte_output = sys.stdout.buffer
        else:
            self.byte_output = sys.stdout
        self.output = sys.stdout

    def setup(self):
        """Set console to read single characters, no echo"""

    def cleanup(self):
        """Restore default console settings"""

    def getkey(self):
        """Read a single key from the console"""
        return None

    def write_bytes(self, byte_string):
        """Write bytes (already encoded)"""
        self.byte_output.write(byte_string)
        self.byte_output.flush()

    def write(self, text):
        """Write string"""
        self.output.write(text)
        self.output.flush()

    def cancel(self):
        """Cancel getkey operation"""

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # context manager:
    # switch terminal temporary to normal mode (e.g. to get user input)

    def __enter__(self):
        self.cleanup()
        return self

    def __exit__(self, *args, **kwargs):
        self.setup()

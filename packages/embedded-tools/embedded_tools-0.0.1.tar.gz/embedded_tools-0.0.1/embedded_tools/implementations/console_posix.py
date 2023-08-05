#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from interfaces import console
import sys
import os

if os.name == 'posix':
    import atexit
    import termios
    import fcntl
    import signal

    class Console(console.ConsoleBase):
        def __init__(self, miniterm):
            super(Console, self).__init__(miniterm)
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            atexit.register(self.cleanup)
            signal.signal(signal.SIGINT, self.sigint)
            if sys.version_info < (3, 0):
                self.enc_stdin = codecs.getreader(sys.stdin.encoding)(sys.stdin)
            else:
                self.enc_stdin = sys.stdin

        def setup(self):
            new = termios.tcgetattr(self.fd)
            new[3] = new[3] & ~termios.ICANON & ~termios.ECHO & ~termios.ISIG
            new[6][termios.VMIN] = 1
            new[6][termios.VTIME] = 0
            termios.tcsetattr(self.fd, termios.TCSANOW, new)

        def getkey(self):
            c = self.enc_stdin.read(1)
            if c == chr(0x7f):
                c = chr(8)    # map the BS key (which yields DEL) to backspace
            return c

        def cancel(self):
            fcntl.ioctl(self.fd, termios.TIOCSTI, b'\0')

        def cleanup(self):
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old)

        def sigint(self, sig, frame):
            """signal handler for a clean exit on SIGINT"""
            self.miniterm.stop()
            self.cancel()

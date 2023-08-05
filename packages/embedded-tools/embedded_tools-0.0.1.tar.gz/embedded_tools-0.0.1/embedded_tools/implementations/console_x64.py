#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

from interfaces import console
import codecs
import sys
import os

if os.name == 'nt':  # noqa
    import msvcrt
    import ctypes
    import platform

    class Out(object):
        """file-like wrapper that uses os.write"""

        def __init__(self, fd):
            self.fd = fd

        def flush(self):
            pass

        def write(self, s):
            os.write(self.fd, s)

    class Console(console.ConsoleBase):
        fncodes = {
            ';': '\x1bOP',  # F1
            '<': '\x1bOQ',  # F2
            '=': '\x1bOR',  # F3
            '>': '\x1bOS',  # F4
            '?': '\x1b[15~',  # F5
            '@': '\x1b[17~',  # F6
            'A': '\x1b[18~',  # F7
            'B': '\x1b[19~',  # F8
            'C': '\x1b[20~',  # F9
            'D': '\x1b[21~',  # F10
        }
        navcodes = {
            'H': '\x1b[A',  # UP
            'P': '\x1b[B',  # DOWN
            'K': '\x1b[D',  # LEFT
            'M': '\x1b[C',  # RIGHT
            'G': '\x1b[H',  # HOME
            'O': '\x1b[F',  # END
            'R': '\x1b[2~',  # INSERT
            'S': '\x1b[3~',  # DELETE
            'I': '\x1b[5~',  # PAGE UP
            'Q': '\x1b[6~',  # PAGE DOWN
        }

        def __init__(self, miniterm):
            super(Console, self).__init__(miniterm)
            self._saved_ocp = ctypes.windll.kernel32.GetConsoleOutputCP()
            self._saved_icp = ctypes.windll.kernel32.GetConsoleCP()
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
            # ANSI handling available through SetConsoleMode since Windows 10 v1511
            # https://en.wikipedia.org/wiki/ANSI_escape_code#cite_note-win10th2-1
            if platform.release() == '10' and int(platform.version().split('.')[2]) > 10586:
                ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
                import ctypes.wintypes as wintypes
                if not hasattr(wintypes, 'LPDWORD'):  # PY2
                    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
                SetConsoleMode = ctypes.windll.kernel32.SetConsoleMode
                GetConsoleMode = ctypes.windll.kernel32.GetConsoleMode
                GetStdHandle = ctypes.windll.kernel32.GetStdHandle
                mode = wintypes.DWORD()
                GetConsoleMode(GetStdHandle(-11), ctypes.byref(mode))
                if (mode.value & ENABLE_VIRTUAL_TERMINAL_PROCESSING) == 0:
                    SetConsoleMode(GetStdHandle(-11), mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
                    self._saved_cm = mode
            self.output = codecs.getwriter('UTF-8')(Out(sys.stdout.fileno()), 'replace')
            # the change of the code page is not propagated to Python, manually fix it
            sys.stderr = codecs.getwriter('UTF-8')(Out(sys.stderr.fileno()), 'replace')
            sys.stdout = self.output
            self.output.encoding = 'UTF-8'  # needed for input

        def __del__(self):
            ctypes.windll.kernel32.SetConsoleOutputCP(self._saved_ocp)
            ctypes.windll.kernel32.SetConsoleCP(self._saved_icp)
            try:
                ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), self._saved_cm)
            except AttributeError:  # in case no _saved_cm
                pass

        def getkey(self):
            while True:
                z = msvcrt.getwch()
                if z == chr(13):
                    return chr(10)
                elif z is chr(0) or z is chr(0xe0):
                    try:
                        code = msvcrt.getwch()
                        if z is chr(0):
                            return self.fncodes[code]
                        else:
                            return self.navcodes[code]
                    except KeyError:
                        pass
                else:
                    return z

        def cancel(self):
            # CancelIo, CancelSynchronousIo do not seem to work when using
            # getwch, so instead, send a key to the window with the console
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            ctypes.windll.user32.PostMessageA(hwnd, 0x100, 0x0d, 0)

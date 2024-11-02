"""
Font: https://gist.github.com/chriskiehl/2906125
"""

import win32con
import win32api
import time

VK_CODE = {'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
            'a':0x41,
            'd':0x44,
            's':0x53,
            'w':0x57,
            'c': 0x43,
            'F1': 0x70,
            'F2': 0x71,
            'F3': 0x72,
            'F4': 0x73,
            'F5': 0x74,
            'F6': 0x75,
            'F7': 0x76,
            'F8':0x77
           }

class KeyBoardInput:

    @staticmethod
    def press(*args):
        '''
        one press, one release.
        accepts as many arguments as you want. e.g. press('left_arrow', 'a','b').
        '''
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0, 0, 0)
            time.sleep(.05)
            win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def pressAndHold(*args):
        '''
        press and hold. Do NOT release.
        accepts as many arguments as you want.
        e.g. pressAndHold('left_arrow', 'a','b').
        '''
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0, 0, 0)
            time.sleep(.05)

    @staticmethod
    def pressHoldRelease(*args):
        '''
        press and hold passed in strings. Once held, release
        accepts as many arguments as you want.
        e.g. pressAndHold('left_arrow', 'a','b').

        this is useful for issuing shortcut command or shift commands.
        e.g. pressHoldRelease('ctrl', 'alt', 'del'), pressHoldRelease('shift','a')
        '''
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0, 0, 0)
            time.sleep(.05)

        for i in args:
            win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(.1)

    @staticmethod
    def release(*args):
        '''
        release depressed keys
        accepts as many arguments as you want.
        e.g. release('left_arrow', 'a','b').
        '''
        for i in args:
            win32api.keybd_event(VK_CODE[i], 0, win32con.KEYEVENTF_KEYUP, 0)



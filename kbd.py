import ctypes
import os
import sys
import glob
from collections import namedtuple
import termios
# /usr/include/linux/input-event-codes.h
event = {
    0x00: 'RELEASED',
    0x01: 'PRESSED',
    0x02: 'REPEATED',
}

# /usr/include/linux/input-event-codes.h
key_map = {
    0: 'KEY_RESERVED',
    1: 'KEY_ESC',
    2: 'KEY_1',
    3: 'KEY_2',
    4: 'KEY_3',
    5: 'KEY_4',
    6: 'KEY_5',
    7: 'KEY_6',
    8: 'KEY_7',
    9: 'KEY_8',
    10: 'KEY_9',
    11: 'KEY_0',
    12: 'KEY_MINUS',
    13: 'KEY_EQUAL',
    14: 'KEY_BACKSPACE',
    15: 'KEY_TAB',
    16: 'KEY_Q',
    17: 'KEY_W',
    18: 'KEY_E',
    19: 'KEY_R',
    20: 'KEY_T',
    21: 'KEY_Y',
    22: 'KEY_U',
    23: 'KEY_I',
    24: 'KEY_O',
    25: 'KEY_P',
    26: 'KEY_LEFTBRACE',
    27: 'KEY_RIGHTBRACE',
    28: 'KEY_ENTER',
    29: 'KEY_LEFTCTRL',
    30: 'KEY_A',
    31: 'KEY_S',
    32: 'KEY_D',
    33: 'KEY_F',
    34: 'KEY_G',
    35: 'KEY_H',
    36: 'KEY_J',
    37: 'KEY_K',
    38: 'KEY_L',
    39: 'KEY_SEMICOLON',
    40: 'KEY_APOSTROPHE',
    41: 'KEY_GRAVE',
    42: 'KEY_LEFTSHIFT',
    43: 'KEY_BACKSLASH',
    44: 'KEY_Z',
    45: 'KEY_X',
    46: 'KEY_C',
    47: 'KEY_V',
    48: 'KEY_B',
    49: 'KEY_N',
    50: 'KEY_M',
    51: 'KEY_COMMA',
    52: 'KEY_DOT',
    53: 'KEY_SLASH',
    54: 'KEY_RIGHTSHIFT',
    55: 'KEY_KPASTERISK',
    56: 'KEY_LEFTALT',
    57: 'KEY_SPACE',
    58: 'KEY_CAPSLOCK',
    59: 'KEY_F1',
    60: 'KEY_F2',
    61: 'KEY_F3',
    62: 'KEY_F4',
    63: 'KEY_F5',
    64: 'KEY_F6',
    65: 'KEY_F7',
    66: 'KEY_F8',
    67: 'KEY_F9',
    68: 'KEY_F10',
    69: 'KEY_NUMLOCK',
    70: 'KEY_SCROLLLOCK',
    71: 'KEY_KP7',
    72: 'KEY_KP8',
    73: 'KEY_KP9',
    74: 'KEY_KPMINUS',
    75: 'KEY_KP4',
    76: 'KEY_KP5',
    77: 'KEY_KP6',
    78: 'KEY_KPPLUS',
    79: 'KEY_KP1',
    80: 'KEY_KP2',
    81: 'KEY_KP3',
    82: 'KEY_KP0',
    83: 'KEY_KPDOT',
    85: 'KEY_ZENKAKUHANKAKU',
    86: 'KEY_102ND',
    87: 'KEY_F11',
    88: 'KEY_F12',
    89: 'KEY_RO',
    90: 'KEY_KATAKANA',
    91: 'KEY_HIRAGANA',
    92: 'KEY_HENKAN',
    93: 'KEY_KATAKANAHIRAGANA',
    94: 'KEY_MUHENKAN',
    95: 'KEY_KPJPCOMMA',
    96: 'KEY_KPENTER',
    97: 'KEY_RIGHTCTRL',
    98: 'KEY_KPSLASH',
    99: 'KEY_SYSRQ',
    100: 'KEY_RIGHTALT',
    101: 'KEY_LINEFEED',
    102: 'KEY_HOME',
    103: 'KEY_UP',
    104: 'KEY_PAGEUP',
    105: 'KEY_LEFT',
    106: 'KEY_RIGHT',
    107: 'KEY_END',
    108: 'KEY_DOWN',
    109: 'KEY_PAGEDOWN',
    110: 'KEY_INSERT',
    111: 'KEY_DELETE',
    112: 'KEY_MACRO',
    113: 'KEY_MUTE',
    114: 'KEY_VOLUMEDOWN',
    115: 'KEY_VOLUMEUP',
    116: 'KEY_POWER',
    117: 'KEY_KPEQUAL',
    118: 'KEY_KPPLUSMINUS',
    119: 'KEY_PAUSE',
    120: 'KEY_SCALE',
    121: 'KEY_KPCOMMA',
    122: 'KEY_HANGEUL,KEY_HANGUEL',
    123: 'KEY_HANJA',
    124: 'KEY_YEN',
    125: 'KEY_LEFTMETA',
    126: 'KEY_RIGHTMETA',
    127: 'KEY_COMPOSE',
    128: 'KEY_STOP',
    129: 'KEY_AGAIN',
    130: 'KEY_PROPS',
    131: 'KEY_UNDO',
    132: 'KEY_FRONT',
    133: 'KEY_COPY',
    134: 'KEY_OPEN',
    135: 'KEY_PASTE',
    136: 'KEY_FIND',
    137: 'KEY_CUT',
    138: 'KEY_HELP',
    139: 'KEY_MENU',
    140: 'KEY_CALC',
    141: 'KEY_SETUP',
    142: 'KEY_SLEEP',
    143: 'KEY_WAKEUP',
    144: 'KEY_FILE',
    145: 'KEY_SENDFILE',
    146: 'KEY_DELETEFILE',
    147: 'KEY_XFER',
    148: 'KEY_PROG1',
    149: 'KEY_PROG2',
    150: 'KEY_WWW',
    151: 'KEY_MSDOS',
    152: 'KEY_COFFEE,KEY_SCREENLOCK',
    153: 'KEY_ROTATE_DISPLAY,KEY_DIRECTION',
    154: 'KEY_CYCLEWINDOWS',
    155: 'KEY_MAIL',
    156: 'KEY_BOOKMARKS',
    157: 'KEY_COMPUTER',
    158: 'KEY_BACK',
    159: 'KEY_FORWARD',
    160: 'KEY_CLOSECD',
    161: 'KEY_EJECTCD',
    162: 'KEY_EJECTCLOSECD',
    163: 'KEY_NEXTSONG',
    164: 'KEY_PLAYPAUSE',
    165: 'KEY_PREVIOUSSONG',
    166: 'KEY_STOPCD',
    167: 'KEY_RECORD',
    168: 'KEY_REWIND',
    169: 'KEY_PHONE',
    170: 'KEY_ISO',
    171: 'KEY_CONFIG',
    172: 'KEY_HOMEPAGE',
    173: 'KEY_REFRESH',
    174: 'KEY_EXIT',
    175: 'KEY_MOVE',
    176: 'KEY_EDIT',
    177: 'KEY_SCROLLUP',
    178: 'KEY_SCROLLDOWN',
    179: 'KEY_KPLEFTPAREN',
    180: 'KEY_KPRIGHTPAREN',
    181: 'KEY_NEW',
    182: 'KEY_REDO',
    183: 'KEY_F13',
    184: 'KEY_F14',
    185: 'KEY_F15',
    186: 'KEY_F16',
    187: 'KEY_F17',
    188: 'KEY_F18',
    189: 'KEY_F19',
    190: 'KEY_F20',
    191: 'KEY_F21',
    192: 'KEY_F22',
    193: 'KEY_F23',
    194: 'KEY_F24',
    200: 'KEY_PLAYCD',
    201: 'KEY_PAUSECD',
    202: 'KEY_PROG3',
    203: 'KEY_PROG4',
    204: 'KEY_DASHBOARD',
    205: 'KEY_SUSPEND',
    206: 'KEY_CLOSE',
    207: 'KEY_PLAY',
    208: 'KEY_FASTFORWARD',
    209: 'KEY_BASSBOOST',
    210: 'KEY_PRINT',
    211: 'KEY_HP',
    212: 'KEY_CAMERA',
    213: 'KEY_SOUND',
    214: 'KEY_QUESTION',
    215: 'KEY_EMAIL',
    216: 'KEY_CHAT',
    217: 'KEY_SEARCH',
    218: 'KEY_CONNECT',
    219: 'KEY_FINANCE',
    220: 'KEY_SPORT',
    221: 'KEY_SHOP',
    222: 'KEY_ALTERASE',
    223: 'KEY_CANCEL',
    224: 'KEY_BRIGHTNESSDOWN',
    225: 'KEY_BRIGHTNESSUP',
    226: 'KEY_MEDIA',
    227: 'KEY_SWITCHVIDEOMODE',
    228: 'KEY_KBDILLUMTOGGLE',
    229: 'KEY_KBDILLUMDOWN',
    230: 'KEY_KBDILLUMUP',
    231: 'KEY_SEND',
    232: 'KEY_REPLY',
    233: 'KEY_FORWARDMAIL',
    234: 'KEY_SAVE',
    235: 'KEY_DOCUMENTS',
    236: 'KEY_BATTERY',
    237: 'KEY_BLUETOOTH',
    238: 'KEY_WLAN',
    239: 'KEY_UWB',
    240: 'KEY_UNKNOWN',
    241: 'KEY_VIDEO_NEXT',
    242: 'KEY_VIDEO_PREV',
    243: 'KEY_BRIGHTNESS_CYCLE',
    244: 'KEY_BRIGHTNESS_AUTO,KEY_BRIGHTNESS_ZERO',
    245: 'KEY_DISPLAY_OFF',
    246: 'KEY_WWAN,KEY_WIMAX',
    247: 'KEY_RFKILL',
    248: 'KEY_MICMUTE',
}


# /usr/include/linux/input.h
# struct input_event
class InputEvent(ctypes.Structure):
    _fields_ = [
        ('time', ctypes.c_ulonglong),
        ('usec', ctypes.c_int),
        ('pad', ctypes.c_int),
        ('type', ctypes.c_uint16),
        ('code', ctypes.c_uint16),
        ('value', ctypes.c_int32)
    ]


class DisableEcho:
    def __init__(self):
        self.settings = termios.tcgetattr(sys.stdin.fileno())
        self.when_flag = termios.TCSAFLUSH
        if hasattr(termios, 'TCSASOFT'):
            self.when_flag |= termios.TCSASOFT

    def disable(self):
        setting = self.settings[:]
        setting[3] &= ~termios.ECHO
        termios.tcsetattr(sys.stdin.fileno(), self.when_flag, setting)

    def restore(self):
        termios.tcsetattr(sys.stdin.fileno(), self.when_flag, self.settings)

    def __enter__(self):
        self.disable()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def __del__(self):
        self.restore()


class Keyboard:
    KeyEvent = namedtuple('KeyEvent', ('time', 'usec', 'pad', 'type', 'code', 'value'))
    buffer_size = ctypes.sizeof(InputEvent)

    def __init__(self, _path, disable_echo=True):
        self.fd = None
        self.fd = os.open(_path, os.O_RDONLY)
        self.disable_echo = DisableEcho() if disable_echo else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()

    def __del__(self):
        if self.disable_echo is not None:
            self.disable_echo.restore()
        try:
            if self.fd is not None:
                os.close(self.fd)
        except OSError:
            pass

    def raw(self):
        buffer = os.read(self.fd, self.buffer_size)
        kbd_event = InputEvent.from_buffer_copy(buffer)
        return self.KeyEvent(kbd_event.time,
                             kbd_event.usec,
                             kbd_event.pad,
                             kbd_event.type,
                             kbd_event.code,
                             kbd_event.value)

    def get(self):
        _kbd = self.raw()
        return self.KeyEvent(_kbd.time, _kbd.usec, _kbd.pad,
                             _kbd.type, key_map.get(_kbd.code),
                             event.get(_kbd.value, 'UNK'))

    def loop(self):
        while True:
            try:
                yield self.get()
            except KeyboardInterrupt:
                break

    def raw_loop(self):
        while True:
            try:
                yield self.raw()
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    path = '/dev/input/by-path/*event-kbd'
    kbd = glob.glob(path)
    with Keyboard(kbd[0])as kbd:
        for key in kbd.loop():
            print(key)

import os
import sys


def init(autoreset=False):
    if os.name == 'posix':
        if 'TERM' in os.environ and os.environ['TERM'] == 'dumb':
            return
        else:
            enable_ansi_escape_sequences(autoreset)
    elif os.name == 'nt':
        enable_win32_color_support(autoreset)

def enable_ansi_escape_sequences(autoreset=False):
    if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
        return

    if 'TERM' not in os.environ:
        os.environ['TERM'] = 'xterm'

    if autoreset:
        sys.stdout.write('\033[0m')
    else:
        sys.stdout.write('\033[0m\033[?1049h')

    sys.stdout.flush()


def enable_win32_color_support(autoreset=False):
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32

        handle = kernel32.GetStdHandle(-11)

        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))

        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
        kernel32.SetConsoleMode(handle, mode)

        if autoreset:
            sys.stdout.write('\033[0m')
        else:
            sys.stdout.write('\033[0m\033[?1049h')

        sys.stdout.flush()

    except Exception as e:
        print(f'Error: {e}')

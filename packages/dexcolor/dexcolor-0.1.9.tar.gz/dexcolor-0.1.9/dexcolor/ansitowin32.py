import re
import ctypes

ANSI_ESCAPE_REGEX = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')


def convert_ansi_to_win32(text):
    def repl(match):
        code = match.group()
        if code == '\x1b[0m':
            return '\033[0m\033[?1049l'
        elif code.startswith('\x1b[') and code.endswith('m'):
            codes = code[2:-1].split(';')
            win32_codes = []

            for c in codes:
                if c == '0':
                    win32_codes.append(0x0001)  # FOREGROUND_INTENSITY
                elif c == '1':
                    win32_codes.append(0x0008)  # FOREGROUND_INTENSITY
                elif c == '30':
                    win32_codes.append(0x0000)  # FOREGROUND_BLACK
                elif c == '31':
                    win32_codes.append(0x0004)  # FOREGROUND_RED
                elif c == '32':
                    win32_codes.append(0x0002)  # FOREGROUND_GREEN
                elif c == '33':
                    win32_codes.append(0x0006)  # FOREGROUND_YELLOW
                elif c == '34':
                    win32_codes.append(0x0001)  # FOREGROUND_BLUE
                elif c == '35':
                    win32_codes.append(0x0005)  # FOREGROUND_MAGENTA
                elif c == '36':
                    win32_codes.append(0x0003)  # FOREGROUND_CYAN
                elif c == '37':
                    win32_codes.append(0x0007)  # FOREGROUND_WHITE
                elif c == '90':
                    win32_codes.append(0x0008)  # FOREGROUND_INTENSITY
                elif c == '91':
                    win32_codes.append(0x000C)  # FOREGROUND_RED | FOREGROUND_INTENSITY
                elif c == '92':
                    win32_codes.append(0x000A)  # FOREGROUND_GREEN | FOREGROUND_INTENSITY
                elif c == '93':
                    win32_codes.append(0x000E)  # FOREGROUND_YELLOW | FOREGROUND_INTENSITY
                elif c == '94':
                    win32_codes.append(0x0009)  # FOREGROUND_BLUE | FOREGROUND_INTENSITY
                elif c == '95':
                    win32_codes.append(0x000D)  # FOREGROUND_MAGENTA | FOREGROUND_INTENSITY
                elif c == '96':
                    win32_codes.append(0x000B)  # FOREGROUND_CYAN | FOREGROUND_INTENSITY
                elif c == '97':
                    win32_codes.append(0x000F)  # FOREGROUND_WHITE | FOREGROUND_INTENSITY

            win32_code = sum(win32_codes)
            return f'\033[38;5;{win32_code}m'

        return ''

    converted_text = ANSI_ESCAPE_REGEX.sub(repl, text)

    return converted_text

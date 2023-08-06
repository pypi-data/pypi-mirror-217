Color_code = {
    'GRAY': '30',
    'RED': '31',
    'GREEN': '32',
    'YELLOW': '33',
    'BLUE': '34',
    'MAGENTA': '35',
    'CYAN': '36',
    'WHITE': '37',
    'BRIGHT_BLACK': '90',
    'BRIGHT_RED': '91',
    'BRIGHT_GREEN': '92',
    'BRIGHT_YELLOW': '93',
    'BRIGHT_BLUE': '94',
    'BRIGHT_MAGENTA': '95',
    'BRIGHT_CYAN': '96',
    'BRIGHT_WHITE': '97',
}

Styles_code = {
    'BOLD': '1',
    'DIM': '2',
    'ITALIC': '3',
    'UNDERLINE': '4',
    'BLINK': '5',
    'REVERSE': '7',
}

class STYLE:
    @staticmethod
    def BOLD(text):
        return f"\033[1m{text}\033[0m"
    
    @staticmethod
    def DIM(text):
        return f"\033[2m{text}\033[0m"
    
    @staticmethod
    def ITALIC(text):
        return f"\033[3m{text}\033[0m"
    
    @staticmethod
    def BOLD_ITALIC(text):
        return f"\033[1m\033[3m{text}\033[0m"
    
    @staticmethod
    def BOLD_DIM(text):
        return f"\033[2m\033[1m{text}\033[0m"
    
    @staticmethod
    def DIM_ITALIC(text):
        return f"\033[2m\033[3m{text}\033[0m"
    
    @staticmethod
    def UNDERLINE(text):
        return f"\033[4m{text}\033[0m"
    
    @staticmethod
    def BLINK(text):
        return f"\033[5m{text}\033[0m"
    
    @staticmethod
    def REVERSE(text):
        return f"\033[7m{text}\033[0m"

class DEX:
    @classmethod
    def _sty(cls, text, color=None, style=None):
        color_format = ''
        style_format = ''

        if color:
            color_code = Color_code.get(color, '37')
            color_format = f"\033[{color_code}m"

        if style:
            style_codes = [Styles_code.get(s, '0') for s in style.split()]
            style_format = ';'.join(style_codes)
            style_format = f"\033[{style_format}m"

        return f"{color_format}{style_format}{text}"

    @classmethod
    def GRAY(cls, text, style=None):
        return cls._sty(text, color='GRAY', style=style)
        
    @classmethod
    def RED(cls, text, style=None):
        return cls._sty(text, color='RED', style=style)

    @classmethod
    def GREEN(cls, text, style=None):
        return cls._sty(text, color='GREEN', style=style)

    @classmethod
    def YELLOW(cls, text, style=None):
        return cls._sty(text, color='YELLOW', style=style)

    @classmethod
    def BLUE(cls, text, style=None):
        return cls._sty(text, color='BLUE', style=style)

    @classmethod
    def MAGENTA(cls, text, style=None):
        return cls._sty(text, color='MAGENTA', style=style)

    @classmethod
    def CYAN(cls, text, style=None):
        return cls._sty(text, color='CYAN', style=style)

    @classmethod
    def WHITE(cls, text, style=None):
        return cls._sty(text, color='WHITE', style=style)

    @classmethod
    def BRIGHT_BLACK(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_BLACK', style=style)

    @classmethod
    def BRIGHT_RED(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_RED', style=style)

    @classmethod
    def BRIGHT_GREEN(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_GREEN', style=style)

    @classmethod
    def BRIGHT_YELLOW(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_YELLOW', style=style)

    @classmethod
    def BRIGHT_BLUE(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_BLUE', style=style)

    @classmethod
    def BRIGHT_MAGENTA(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_MAGENTA', style=style)

    @classmethod
    def BRIGHT_CYAN(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_CYAN', style=style)

    @classmethod
    def BRIGHT_WHITE(cls, text, style=None):
        return cls._sty(text, color='BRIGHT_WHITE', style=style)
    RESET = '\033[0m'
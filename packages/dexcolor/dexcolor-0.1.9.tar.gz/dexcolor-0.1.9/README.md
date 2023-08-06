# dexcolor

**dexcolor** is a Python package that provides a simple and convenient way to add color and style to text output in the terminal. It supports various ANSI escape sequences for text formatting and provides a cross-platform solution for both POSIX and Windows operating systems.

## Installation

You can install **dexcolor** using pip:

```
pip install dexcolor
```

## Usage

### Using Colors Only

You can use **dexcolor** to add colors to your text. Available colors are:

- GRAY
- RED
- GREEN
- YELLOW
- BLUE
- MAGENTA
- CYAN
- WHITE
- BRIGHT_BLACK
- BRIGHT_RED
- BRIGHT_GREEN
- BRIGHT_YELLOW
- BRIGHT_BLUE
- BRIGHT_MAGENTA
- BRIGHT_CYAN
- BRIGHT_WHITE

Example:

```python
from dexcolor import DEX

print(DEX.RED("Hello, World!"))
```

### Using Colors and Styles

You can combine colors with styles to customize the appearance of your text even further. Available styles are:

- BOLD
- DIM
- ITALIC
- UNDERLINE
- BLINK
- REVERSE

Example:

```python
from dexcolor import DEX

print(DEX.MAGENTA("Hello, World!", style='BOLD'))
```

### Using Styles Only

You can also apply styles without any specific color:

```python
from dexcolor import STYLE

print(STYLE.DIM("Hello, World!"))
```

### Resetting Colors and Styles

To reset the text color and style to the default, you can use the RESET attribute:

```python
from dexcolor import DEX

print(DEX.RED("Hello, World!") + DEX.RESET)
print(DEX.RED("Hello, World!", style='BOLD') + DEX.RESET)
```

### Windows Compatibility

**dexcolor** is compatible with Windows operating systems. If you are working on Windows and want to convert ANSI escape sequences to the Win32 format, you can use the provided conversion function.

#### ANSI Escape Sequences Conversion (Windows)

To convert ANSI escape sequences to the Win32 format on Windows, you can use the following code:

```python
from dexcolor import convert_ansi_to_win32

text = '\033[31mHello, World!\033[0m'  # Example text with ANSI escape sequences
converted_text = convert_ansi_to_win32(text)  # Convert ANSI escape sequences to Win32 format

print(converted_text)  # Display the converted text
```

This conversion function is specifically useful on Windows to ensure proper rendering of colored and styled text.

## Compatibility

**dexcolor** is compatible with Linux, macOS, and Windows operating systems. It utilizes ANSI escape sequences, which are widely supported on various platforms.


- [GitHub Repository](https://github.com/Terong333/dexcolor)
- [PyPI Package](https://pypi.org/project/dexcolor/)

---

If you have any questions or need further assistance, feel free to ask!
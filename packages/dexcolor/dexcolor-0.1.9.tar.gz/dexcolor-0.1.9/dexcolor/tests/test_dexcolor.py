import unittest
from dexcolor import DEX, STYLE, convert_ansi_to_win32

class DexColorTestCase(unittest.TestCase):
    def test_text_color(self):
        text = "Hello, World!"
        red_text = DEX.RED(text)
        self.assertEqual(red_text, '\033[31mHello, World!\033[0m')

    def test_text_style(self):
        text = "Hello, World!"
        bold_text = STYLE.BOLD(text)
        self.assertEqual(bold_text, '\033[1mHello, World!\033[0m')

    def test_combined_color_and_style(self):
        text = "Hello, World!"
        blue_bold_text = DEX.BLUE(STYLE.BOLD(text))
        expected_output = '\033[34;1mHello, World!\033[0m'
        self.assertEqual(blue_bold_text, expected_output)

    def test_reset_color_and_style(self):
        text = "Hello, World!"
        reset_text = DEX.RED(text) + DEX.RESET
        self.assertEqual(reset_text, '\033[31mHello, World!\033[0m\033[0m')

    def test_style_only(self):
        text = "Hello, World!"
        dim_text = STYLE.DIM(text)
        self.assertEqual(dim_text, '\033[2mHello, World!\033[0m')

    def test_windows_conversion(self):
        text = '\033[31mHello, World!\033[0m'
        converted_text = convert_ansi_to_win32(text)
        self.assertEqual(converted_text, 'Hello, World!')

if __name__ == '__main__':
    unittest.main()
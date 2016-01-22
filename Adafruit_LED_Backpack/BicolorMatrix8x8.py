# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from Matrix8x8 import Matrix8x8

# Color values as convenient globals.
# This is a bitmask value where the first bit is green, and the second bit is
# red.  If both bits are set the color is yellow (red + green light).
OFF = 0
GREEN = 1
RED = 2
YELLOW = 3


class BicolorMatrix8x8(Matrix8x8):
    """Bi-color 8x8 matrix LED backpack display."""

    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(BicolorMatrix8x8, self).__init__(**kwargs)

    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 8.  Value should be OFF, GREEN, RED, or YELLOW.
        """
        if x < 0 or x > 7 or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return
        # Set green LED based on 1st bit in value.
        self.set_led(y * 16 + x, 1 if value & GREEN > 0 else 0)
        # Set red LED based on 2nd bit in value.
        self.set_led(y * 16 + x + 8, 1 if value & RED > 0 else 0)

    def set_image(self, image):
        """Set display buffer to Python Image Library image.  Red pixels (r=255,
        g=0, b=0) will map to red LEDs, green pixels (r=0, g=255, b=0) will map to
        green LEDs, and yellow pixels (r=255, g=255, b=0) will map to yellow LEDs.
        All other pixel values will map to an unlit LED value.
        """
        imwidth, imheight = image.size
        if imwidth != 8 or imheight != 8:
            raise ValueError('Image must be an 8x8 pixels in size.')
        # Convert image to RGB and grab all the pixels.
        pix = image.convert('RGB').load()
        # Loop through each pixel and write the display buffer pixel.
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                color = pix[(x, y)]
                # Handle the color of the pixel.
                if color == (255, 0, 0):
                    self.set_pixel(x, y, RED)
                elif color == (0, 255, 0):
                    self.set_pixel(x, y, GREEN)
                elif color == (255, 255, 0):
                    self.set_pixel(x, y, YELLOW)
                else:
                    # Unknown color, default to LED off.
                    self.set_pixel(x, y, OFF)

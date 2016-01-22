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
import HT16K33
import Image
import time


class Matrix8x8(HT16K33.HT16K33):
    """Single color 8x8 matrix LED backpack display."""

    def __init__(self, **kwargs):
        """Initialize display.  All arguments will be passed to the HT16K33 class
        initializer, including optional I2C address and bus number parameters.
        """
        super(Matrix8x8, self).__init__(**kwargs)

    def set_pixel(self, x, y, value):
        """Set pixel at position x, y to the given value.  X and Y should be values
        of 0 to 8.  Value should be 0 for off and non-zero for on.
        """
        if x < 0 or x > 7 or y < 0 or y > 7:
            # Ignore out of bounds pixels.
            return
        self.set_led(y * 16 + ((x + 7) % 8), value)

    def set_image(self, image):
        """Set display buffer to Python Image Library image.  Image will be converted
        to 1 bit color and non-zero color values will light the LEDs.
        """
        imwidth, imheight = image.size
        if imwidth != 8 or imheight != 8:
            raise ValueError('Image must be an 8x8 pixels in size.')
        # Convert image to 1 bit color and grab all the pixels.
        pix = image.convert('1').load()
        # Loop through each pixel and write the display buffer pixel.
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                color = pix[(x, y)]
                # Handle the color of the pixel, off or on.
                if color == 0:
                    self.set_pixel(x, y, 0)
                else:
                    self.set_pixel(x, y, 1)

    def create_blank_image(self):
        return Image.new("RGB", (8, 8))


    def horizontal_scroll(self, image, padding=True):
        """Returns a list of images which appear to scroll from left to right
        across the input image when displayed on the LED matrix in order.

        The input image is not limited to being 8x8. If the input image is
        larger than this, then all columns will be scrolled through but only
        the top 8 rows of pixels will be displayed.

        Keyword arguments:
        image -- The image to scroll across.
        padding -- If True, the animation will begin with a blank screen and the
            input image will scroll into the blank screen one pixel column at a
            time. Similarly, after scrolling across the whole input image, the
            end of the image will scroll out of a blank screen one column at a
            time. If this is not True, then only the input image will be scroll
            across without beginning or ending with "whitespace."
            (Default = True)
        """

        image_list = list()
        width = image.size[0]
        # Scroll into the blank image.
        if padding:
            for x in range(8):
                section = image.crop((0, 0, x, 8))
                display_section = self.create_blank_image()
                display_section.paste(section, (8 - x, 0, 8, 8))
                image_list.append(display_section)

        #Scroll across the input image.
        for x in range(8, width + 1):
            section = image.crop((x - 8, 0, x, 8))
            display_section = self.create_blank_image()
            display_section.paste(section, (0, 0, 8, 8))
            image_list.append(display_section)

        #Scroll out, leaving the blank image.
        if padding:
            for x in range(width - 7, width + 1):
                section = image.crop((x, 0, width, 8))
                display_section = self.create_blank_image()
                display_section.paste(section, (0, 0, 7 - (x - (width - 7)), 8))
                image_list.append(display_section)

        #Return the list of images created
        return image_list

    def vertical_scroll(self, image, padding=True):
        """Returns a list of images which appear to scroll from top to bottom
        down the input image when displayed on the LED matrix in order.

        The input image is not limited to being 8x8. If the input image is
        largerthan this, then all rows will be scrolled through but only the
        left-most 8 columns of pixels will be displayed.

        Keyword arguments:
        image -- The image to scroll down.
        padding -- If True, the animation will begin with a blank screen and the
            input image will scroll into the blank screen one pixel row at a
            time. Similarly, after scrolling down the whole input image, the end
            of the image will scroll out of a blank screen one row at a time.
            If this is not True, then only the input image will be scroll down
            without beginning or ending with "whitespace." (Default = True)
        """

        image_list = list()
        height = image.size[1]
        # Scroll into the blank image.
        if padding:
            for y in range(8):
                section = image.crop((0, 0, 8, y))
                display_section = self.create_blank_image()
                display_section.paste(section, (0, 8 - y, 8, 8))
                image_list.append(display_section)

        #Scroll across the input image.
        for y in range(8, height + 1):
            section = image.crop((0, y - 8, 8, y))
            display_section = self.create_blank_image()
            display_section.paste(section, (0, 0, 8, 8))
            image_list.append(display_section)

        #Scroll out, leaving the blank image.
        if padding:
            for y in range(height - 7, height + 1):
                section = image.crop((0, y, 8, height))
                display_section = self.create_blank_image()
                display_section.paste(section, (0, 0, 8, 7 - (y - (height - 7))))
                image_list.append(display_section)

        #Return the list of images created
        return image_list

    def animate(self, images, delay=.25):
        """Displays each of the input images in order, pausing for "delay"
        seconds after each image.

        Keyword arguments:
        image -- An iterable collection of Image objects.
        delay -- How many seconds to wait after displaying an image before
            displaying the next one. (Default = .25)
        """
        for image in images:
            # Draw the image on the display buffer.
            self.set_image(image)

            # Draw the buffer to the display hardware.
            self.write_display()
            time.sleep(delay)

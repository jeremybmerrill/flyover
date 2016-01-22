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


# Color values as convenient globals.
# This is a bitmask value where the first bit is green, and the second bit is
# red.  If both bits are set the color is yellow (red + green light).
OFF = 0
GREEN = 1
RED = 2
YELLOW = 3


class BicolorBargraph24(HT16K33.HT16K33):
	"""Bi-color 24 segment bar graph LED backpack display."""

	def __init__(self, **kwargs):
		"""Initialize display.  All arguments will be passed to the HT16K33 class
		initializer, including optional I2C address and bus number parameters.
		"""
		super(BicolorBargraph24, self).__init__(**kwargs)

	def set_bar(self, bar, value):
		"""Set bar to desired color.  Bar should be a value of 0 to 23, and value
		should be OFF, GREEN, RED, or YELLOW.
		"""
		if bar < 0 or bar > 23:
			# Ignore out of bounds bars.
			return
		# Compute cathode and anode value.
		c = (bar if bar < 12 else bar - 12) / 4
		a = bar % 4
		if bar >= 12:
			a += 4
		# Set green LED based on 1st bit in value.
		self.set_led(c*16+a+8, 1 if value & GREEN > 0 else 0)
		# Set red LED based on 2nd bit in value.
		self.set_led(c*16+a, 1 if value & RED > 0 else 0)

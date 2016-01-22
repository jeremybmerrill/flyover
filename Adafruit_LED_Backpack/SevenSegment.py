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


# Digit value to bitmask mapping:
DIGIT_VALUES = {
	' ': 0x00,
	'-': 0x40,
	'0': 0x3F,
	'1': 0x06,
	'2': 0x5B,
	'3': 0x4F,
	'4': 0x66,
	'5': 0x6D,
	'6': 0x7D,
	'7': 0x07,
	'8': 0x7F,
	'9': 0x6F,
	'A': 0x77,
	'B': 0x7C,
	'C': 0x39,
	'D': 0x5E,
	'E': 0x79,
	'F': 0x71
}

IDIGIT_VALUES = {
	' ': 0x00,
	'-': 0x40,
	'0': 0x3F,
	'1': 0x30,
	'2': 0x5B,
	'3': 0x79,
	'4': 0x74,
	'5': 0x6D,
	'6': 0x6F,
	'7': 0x38,
	'8': 0x7F,
	'9': 0x7D,
	'A': 0x7E,
	'B': 0x67,
	'C': 0x0F,
	'D': 0x73,
	'E': 0x4F,
	'F': 0x4E
}



class SevenSegment(HT16K33.HT16K33):
	"""Seven segment LED backpack display."""

	def __init__(self, invert=False, **kwargs):
		"""Initialize display.  All arguments will be passed to the HT16K33 class
		initializer, including optional I2C address and bus number parameters.
		"""
		super(SevenSegment, self).__init__(**kwargs)
		self.invert = invert

	def set_invert(self, _invert):
		"""Set whether the display is upside-down or not.
		"""
		self.invert = _invert

	def set_digit_raw(self, pos, bitmask):
		"""Set digit at position to raw bitmask value.  Position should be a value
		of 0 to 3 with 0 being the left most digit on the display."""
		if pos < 0 or pos > 3:
			# Ignore out of bounds digits.
			return
		# Jump past the colon at position 2 by adding a conditional offset.
		offset = 0 if pos < 2 else 1

		# Calculate the correct position depending on orientation
		if self.invert:
			pos = 4-(pos+offset)
		else:
			pos = pos+offset

		# Set the digit bitmask value at the appropriate position.
		self.buffer[pos*2] = bitmask & 0xFF

	def set_decimal(self, pos, decimal):
		"""Turn decimal point on or off at provided position.  Position should be
		a value 0 to 3 with 0 being the left most digit on the display.  Decimal
		should be True to turn on the decimal point and False to turn it off.
		"""
		if pos < 0 or pos > 3:
			# Ignore out of bounds digits.
			return
		# Jump past the colon at position 2 by adding a conditional offset.
		offset = 0 if pos < 2 else 1

		# Calculate the correct position depending on orientation
		if self.invert:
			pos = 4-(pos+offset)
		else:
			pos = pos+offset

		# Set bit 7 (decimal point) based on provided value.
		if decimal:
			self.buffer[pos*2] |= (1 << 7)
		else:
			self.buffer[pos*2] &= ~(1 << 7)

	def set_digit(self, pos, digit, decimal=False):
		"""Set digit at position to provided value.  Position should be a value
		of 0 to 3 with 0 being the left most digit on the display.  Digit should
		be a number 0-9, character A-F, space (all LEDs off), or dash (-).
		"""
		if self.invert:
			self.set_digit_raw(pos, IDIGIT_VALUES.get(str(digit).upper(), 0x00))
		else:
			self.set_digit_raw(pos, DIGIT_VALUES.get(str(digit).upper(), 0x00))

		if decimal:
			self.set_decimal(pos, True)

	def set_colon(self, show_colon):
		"""Turn the colon on with show colon True, or off with show colon False."""
		if show_colon:
			self.buffer[4] |= 0x02
		else:
			self.buffer[4] &= (~0x02) & 0xFF

	def set_left_colon(self, show_colon):
		"""Turn the left colon on with show color True, or off with show colon
		False.  Only the large 1.2" 7-segment display has a left colon.
		"""
		if show_colon:
			self.buffer[4] |= 0x04
			self.buffer[4] |= 0x08
		else:
			self.buffer[4] &= (~0x04) & 0xFF
			self.buffer[4] &= (~0x08) & 0xFF
	
	def set_fixed_decimal(self, show_decimal):
		"""Turn on/off the single fixed decimal point on the large 1.2" 7-segment
		display.  Set show_decimal to True to turn on and False to turn off.
		Only the large 1.2" 7-segment display has this decimal point (in the
		upper right in the normal orientation of the display).
		"""
		if show_decimal:
			self.buffer[4] |= 0x10
		else:
			self.buffer[4] &= (~0x10) & 0xFF

	def print_number_str(self, value, justify_right=True):
		"""Print a 4 character long string of numeric values to the display.
		Characters in the string should be any supported character by set_digit,
		or a decimal point.  Decimal point characters will be associated with
		the previous character.
		"""
		# Calculate length of value without decimals.
		length = len(value.translate(None, '.'))
		# Error if value without decimals is longer than 4 characters.
		if length > 4:
			self.print_number_str('----')
			return
		# Calculcate starting position of digits based on justification.
		pos = (4-length) if justify_right else 0
		# Go through each character and print it on the display.
		for i, ch in enumerate(value):
			if ch == '.':
				# Print decimal points on the previous digit.
				self.set_decimal(pos-1, True)
			else:
				self.set_digit(pos, ch)
				pos += 1

	def print_float(self, value, decimal_digits=2, justify_right=True):
		"""Print a numeric value to the display.  If value is negative
		it will be printed with a leading minus sign.  Decimal digits is the
		desired number of digits after the decimal point.
		"""
		format_string = '{{0:0.{0}F}}'.format(decimal_digits)
		self.print_number_str(format_string.format(value), justify_right)

	def print_hex(self, value, justify_right=True):
		"""Print a numeric value in hexadecimal.  Value should be from 0 to FFFF.
		"""
		if value < 0 or value > 0xFFFF:
			# Ignore out of range values.
			return
		self.print_number_str('{0:X}'.format(value), justify_right)

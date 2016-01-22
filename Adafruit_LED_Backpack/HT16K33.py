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


# Constants
DEFAULT_ADDRESS				= 0x70
HT16K33_BLINK_CMD 			= 0x80
HT16K33_BLINK_DISPLAYON 	= 0x01
HT16K33_BLINK_OFF 			= 0x00
HT16K33_BLINK_2HZ 			= 0x02
HT16K33_BLINK_1HZ 			= 0x04
HT16K33_BLINK_HALFHZ 		= 0x06
HT16K33_SYSTEM_SETUP		= 0x20
HT16K33_OSCILLATOR			= 0x01
HT16K33_CMD_BRIGHTNESS 		= 0xE0


class HT16K33(object):
	"""Driver for interfacing with a Holtek HT16K33 16x8 LED driver."""

	def __init__(self, address=DEFAULT_ADDRESS, i2c=None, **kwargs):
		"""Create an HT16K33 driver for devie on the specified I2C address
		(defaults to 0x70) and I2C bus (defaults to platform specific bus).
		"""
		if i2c is None:
			import Adafruit_GPIO.I2C as I2C
			i2c = I2C
		self._device = i2c.get_i2c_device(address, **kwargs)
		self.buffer = bytearray([0]*16)

	def begin(self):
		"""Initialize driver with LEDs enabled and all turned off."""
		# Turn on the oscillator.
		self._device.writeList(HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR, [])
		# Turn display on with no blinking.
		self.set_blink(HT16K33_BLINK_OFF)
		# Set display to full brightness.
		self.set_brightness(15)

	def set_blink(self, frequency):
		"""Blink display at specified frequency.  Note that frequency must be a
		value allowed by the HT16K33, specifically one of: HT16K33_BLINK_OFF,
		HT16K33_BLINK_2HZ, HT16K33_BLINK_1HZ, or HT16K33_BLINK_HALFHZ.
		"""
		if frequency not in [HT16K33_BLINK_OFF, HT16K33_BLINK_2HZ, 
							 HT16K33_BLINK_1HZ, HT16K33_BLINK_HALFHZ]:
			raise ValueError('Frequency must be one of HT16K33_BLINK_OFF, HT16K33_BLINK_2HZ, HT16K33_BLINK_1HZ, or HT16K33_BLINK_HALFHZ.')
		self._device.writeList(HT16K33_BLINK_CMD | HT16K33_BLINK_DISPLAYON | frequency, [])

	def set_brightness(self, brightness):
		"""Set brightness of entire display to specified value (16 levels, from
		0 to 15).
		"""
		if brightness < 0 or brightness > 15:
			raise ValueError('Brightness must be a value of 0 to 15.')
		self._device.writeList(HT16K33_CMD_BRIGHTNESS | brightness, [])

	def set_led(self, led, value):
		"""Sets specified LED (value of 0 to 127) to the specified value, 0/False 
		for off and 1 (or any True/non-zero value) for on.
		"""
		if led < 0 or led > 127:
			raise ValueError('LED must be value of 0 to 127.')
		# Calculate position in byte buffer and bit offset of desired LED.
		pos = led / 8
		offset = led % 8
		if not value:
			# Turn off the specified LED (set bit to zero).
			self.buffer[pos] &= ~(1 << offset)
		else:
			# Turn on the speciried LED (set bit to one).
			self.buffer[pos] |= (1 << offset)

	def write_display(self):
		"""Write display buffer to display hardware."""
		for i, value in enumerate(self.buffer):
			self._device.write8(i, value)

	def clear(self):
		"""Clear contents of display buffer."""
		for i, value in enumerate(self.buffer):
			self.buffer[i] = 0

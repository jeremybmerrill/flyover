#!/usr/bin/python3
# encoding: utf-8

from PIL import ImageFont, ImageDraw, Image
import board
import busio
from adafruit_ht16k33.matrix import Matrix8x8
import sys
import os
import re
from time import sleep




class CorrectlyOrderedMatrix16x8(Matrix8x8):
    """Adafruit's Matrix16x8 code does some funny business switching coordinates around,
       I think because their's has the two 8x8s arranged vertically from the computer's 
       perspective, but they're betting you have it on its side physically.
      
       This class undoes their funny business. X is x, y is y.
       """
    _columns = 16
    _rows = 8
    def pixel(self, x, y, color=None):
        """Get or set the color of a given pixel."""
        if not 0 <= x <= 15:
            return None
        if not 0 <= y <= 7:
            return None
        return super()._pixel(x, y, color)  # pylint: disable=arguments-out-of-order




class Flyover:

  @classmethod
  def literally_show(self, airport_code):
    i2c = busio.I2C(board.SCL, board.SDA)
    display = CorrectlyOrderedMatrix16x8(i2c)
    display.brightness = 0.4
    display.fill(0)

    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'thintel/Thintel.ttf'), 15)
    if len(airport_code) == 4:
      image = Image.new('1', (21, 8))
      draw = ImageDraw.Draw(image)

      for i in range(58):
        n = 5 - abs((i % 12) - 5)
        draw.text((0, 0), airport_code,  font=font, fill=255)
        display.fill(0)
        display.image(image.crop((n, 0, n + 16, 8)))
        display.show()        
        sleep( 0.5 if i > 0 else 3)
    elif len(airport_code) == 3 or len(airport_code) == 0:
      image = Image.new('1', (16, 8))
      draw = ImageDraw.Draw(image)
      draw.text((0, 0), airport_code,  font=font, fill=255)
      display.image(image)
      display.show()

  @classmethod
  def show(self, airport):
    # either in the form of 
    # - KRDU or
    # - CYUL
    # and eventually, perhaps, in this format
    # - KRDU (Raleigh-Durham, NC)
    # - CYUL (Montreal Trudeau, QC)
    # - UUEE (Moscow-Sheremetyevo, Russia)
    # which would be displayed like this:
    # show the first three letters (or letters 2, 3, 4 for US/Canada) for a little bit, then scroll the rest

    # right now, displays US and Canadian airports by the last three letters of their ICAO code
    # which is usually right but occasionally (theoretically) wrong!
    # in other cases, it displays all four letters in a hacky bouncy way
    us_airport_match = re.match("K([A-Z][A-Z][A-Z])", airport[0:4])
    if us_airport_match:
      self.literally_show(us_airport_match.groups(0)[0])
    elif airport[0:1] in ('CY', 'CZ'):
      self.literally_show(airport[1:4]) # Canada is okay to display as only three letters too!
    elif len(airport) in (4,3,0):
      self.literally_show(airport)
    else:
      print("ignoring invalid airport_code input {}".format(airport))
      self.literally_show('')
      return

if __name__ == "__main__":
  # doesn't support quotes in input because naively splits on whitespace
  # stdin = " ".join(sys.stdin.readlines()).split()
  stdin = ((input() if (sys.version_info > (3, 0)) else raw_input()) or '').split()
  print("displaying: %s" % ','.join(stdin))
  Flyover.show( stdin[0] if len(stdin) else ''  )


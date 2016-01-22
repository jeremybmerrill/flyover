#!/usr/bin/python
# encoding: utf-8

import ImageFont
import ImageDraw
import Image
from Adafruit_LED_Backpack import Matrix16x8
import sys
import os
import re

class Flyover:

  @classmethod
  def literally_show(self, three_letters):
    if len(three_letters) > 3:
      return
    display = Matrix16x8.Matrix16x8()
    display.begin()
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'thintel/Thintel.ttf'), 15)
    image = Image.new('1', (16, 8))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), three_letters,  font=font, fill=255)
    display.set_image(image)
    display.write_display()

  @classmethod
  def show(self, airport):
    # either in the form of 
    # - KRDU
    # - CYUL
    # - RDU
    # - KRDU (Raleigh-Durham, NC)
    # - CYUL (Montreal Trudeau, QC)
    us_airport_match = re.match("K([A-Z][A-Z][A-Z])", airport[0:4])
    if us_airport_match:
      self.literally_show(us_airport_match.groups(0)[0])
    else:
      self.literally_show('')
      return
      # show the first four letters for a little bit, then scroll the rest

if __name__ == "__main__":
  # doesn't support quotes in input because naively splits on whitespace
  stdin = " ".join(sys.stdin.readlines()).split()[0]
  print("input", stdin)
  print(Flyover.show(stdin))

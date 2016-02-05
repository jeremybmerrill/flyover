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
    display.set_brightness(4)
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), 'thintel/Thintel.ttf'), 15)
    image = Image.new('1', (16, 8))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), three_letters,  font=font, fill=255)
    display.set_image(image)
    display.write_display()

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

    # right now, only displays US airports by their code, along with Toronto, Montreal and Ottawa,
    # which are the only Canadian airports with service to LaGuardia
    # if this code were to be used more generically (as in, not just by Jeremy)
    # this needs to be generalized.
    us_airport_match = re.match("K([A-Z][A-Z][A-Z])", airport[0:4])
    if us_airport_match:
      self.literally_show(us_airport_match.groups(0)[0])
    elif airport[0:4] in ('CYYZ', 'CYUL', 'CYOW'):
      self.literally_show(airport[1:4]) # Canada is okay too!
    else:
      self.literally_show('')
      return

if __name__ == "__main__":
  # doesn't support quotes in input because naively splits on whitespace
  # stdin = " ".join(sys.stdin.readlines()).split()
  stdin = (input() if (sys.version_info > (3, 0)) else raw_input()).split()
  print("displaying: %s" % ','.join(stdin))
  Flyover.show( stdin[0] if len(stdin) else ''  )

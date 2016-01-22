#!/usr/bin/python
# encoding: utf-8

# gets the dump1090 JSON, assumes its on localhost
from __future__ import print_function
import requests
import re
import geojson
from sys import stderr
from shapely.geometry import Point, shape

class Flyover:
  flight_num_re = re.compile("^[A-Z]{2,3}\d+$", re.IGNORECASE)

  @classmethod
  def get_nearest_airplane(self, options):
    location =      requests.get("http://%s/dump1090/data/receiver.json" % options.host).json()
    aircraft_resp = requests.get("http://%s/dump1090/data/aircraft.json" % options.host).json()
    flights = aircraft_resp["aircraft"]
    flights = [f for f in flights if "flight" in f and self.flight_num_re.match(f["flight"].strip()) ] 
    def distance(f):
      return ((f.get("lat", 0) - location["lat"]) ** 2 + (f.get("lon", 0) - location["lon"]) ** 2) ** 0.5

    def within_area(flight, area_geojson_location):
      if not area_geojson_location:
        return True
      try:
        with open(area_geojson_location, 'r') as geo:
          bounds = geojson.loads(geo.read())["geometry"]
          flight_loc = Point(f.get("lon", 0), f.get("lat", 0))
          return shape(bounds).contains(flight_loc)
      except IOError:
        print("couldn't find geojson file at %s, ignoring" % area_geojson_location, file=stderr)
        return True

    def altitude(flight, altitude_string):
      if not altitude_string:
        return True 
      altitude_string = altitude_string.strip()
      if 'altitude' not in flight:
        return False 
      if altitude_string[0] == ">":
        return flight['altitude'] > int(altitude_string[1:])
      elif altitude_string[0] == "<":
        return flight['altitude'] < int(altitude_string[1:])
      else: # assume less than
        return flight['altitude'] < int(altitude_string)

    flights = [f for f in flights if altitude(f, options.altitude) and within_area(f, options.area)]
    try:
      nearest_flight = sorted(flights, key=distance)[0]
      return "%s %i" % (nearest_flight['flight'].strip(), nearest_flight.get("vert_rate", 0))
    except IndexError:
      return

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description='Usage: dump1090_to_nearest_flight.py [options]')
  parser.add_argument('-H', '--host',
                      help="The location of the dump1090 server's HTTP interface",
                      required=False,
                      default='localhost')
  parser.add_argument("-a", '--altitude',
                      help="a location constraint for aircraft, e.g. '<10000' or '>30000'. In feet. ",
                      required=False,
                      default=None)
  parser.add_argument("-g", '--area',
                      help="path to geojson of a geographic constraint for aircraft",
                      required=False,
                      default=None)
  # parser.add_argument('-h', '--help',
  #                     help="Display this screen", )
  args = parser.parse_args()

  print(Flyover.get_nearest_airplane(args))

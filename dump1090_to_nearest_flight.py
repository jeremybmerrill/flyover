#!/usr/bin/python
# encoding: utf-8

# gets the dump1090 JSON, assumes its on localhost

import requests
import re

class Flyover:
  flight_num_re = re.compile("^[A-Z]{2,3}\d+$", re.IGNORECASE)

  @classmethod
  def get_nearest_airplane(self, options):
    location =      requests.get("http://%s/dump1090/data/receiver.json" % options.host).json()
    aircraft_resp = requests.get("http://%s/dump1090/data/aircraft.json" % options.host).json()
    flights = aircraft_resp["aircraft"]
    flights = [f for f in flights if "flight" in f and self.flight_num_re.match(f["flight"].strip()) ] 
    def distance(flight):
      return ((f.get("lat", 0) - location["lat"]) ** 2 + (f.get("lon", 0) - location["lon"]) ** 2) ** 0.5
    nearest_flight = sorted(flights, key=distance)[0]
    if nearest_flight: 
      return "%s %i" % (nearest_flight['flight'].strip(), nearest_flight.get("vert_rate", 0))

if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description='Usage: dump1090_to_nearest_flight.py [options]')
  parser.add_argument('-H', '--host',
                      help="The location of the dump1090 server's HTTP interface",
                      required=False,
                      default='localhost')
  # parser.add_argument('-h', '--help',
  #                     help="Display this screen", )
  args = parser.parse_args()

  print(Flyover.get_nearest_airplane(args))

#!/usr/bin/python3
# encoding: utf-8
from __future__ import print_function
import re
from subprocess import check_output, CalledProcessError
import sys
import os.path

class Flyover:
  NYC_AIRPORTS = ["KLGA", "KJFK", "KEWR"]
  TRANSLATIONS = {
    "JB": "JBU",
  }

  flight_number_re = re.compile("^([A-Z]+)?(\d+)$")

  @classmethod
  def where(self, flight_number, delta_altitude):
    airline, number = self.flight_number_re.match(flight_number).groups()

    if airline in self.TRANSLATIONS:
      airline = self.TRANSLATIONS[airline]

    # data is FlightNumbers.csv from http://www.virtualradarserver.co.uk/FlightRoutes.aspx
    # script assumes that the datafile is in the same directory as this script
    # script assumes that grep is installed (i.e. this script won't work on Windows, sorry! Pull Request would be accepted though.)
    try:
      flight_rows = check_output(["grep", "%s,%s,"%(airline, number), os.path.join(os.path.dirname(os.path.realpath(__file__)),  "FlightNumbers.csv") ]).decode("utf-8").strip().split("\r\n")
    except CalledProcessError:
      flight_rows = []

    # if there is more than one match for the given flight number, we're in trouble, but continue after warning
    if len(flight_rows) > 1: 
      print("WARN: %s matches for %s: %s" % (len(flight_rows), flight_number, '|'.join(flight_rows) ), file=sys.stderr)
    if len(flight_rows) < 1: 
      print("WARN: zero matches for %s" % flight_number, file=sys.stderr)
    if not flight_rows:
      return 
    route = flight_rows[0].split(",")[-1]
    
    # get a list of the airports served by this flight number
    airports = route.split("-")
    print("DEBUG: row: %s"%flight_rows[0].strip(), file=sys.stderr)

    # determine if this flight number goes to New York 
    if any([nyc_airport in airports for nyc_airport in self.NYC_AIRPORTS]):
      # if this flight number goes to several airports, ignore the New York airports and the airports from which this flight does not come or go from New York. (because that's not a relevant destination here, except in potential odd cases)
      nyc_adjacent_airports = [airport for idx, airport in enumerate(airports) if (idx > 0 and airports[idx-1] in self.NYC_AIRPORTS) or (idx < (len(airports) -1) and airports[idx+1] in self.NYC_AIRPORTS) ]


      # if there's only one non-NYC airport that is adjacent to an NYC airport in the itinerary, then return that
      if len(set(nyc_adjacent_airports)) == 1:
        return nyc_adjacent_airports[0]
      else: # if there's multiple non-NYC airports that are adjacent to an NYC airport in the itinerary, then
        if delta_altitude > 0:   # if change in altitude over two measurements is positive, plane is ascending, so we'll assume it's departing, so we'll take the last listed airport (destination from NYC)
          return nyc_adjacent_airports[-1]
        elif delta_altitude < 0: # if change in altitude over two measurements is negative, plane is descending, so it's arriving to New York, so we'll take the first listed airport (departure, to NYC)
          return nyc_adjacent_airports[0]
        else: # if we don't know its change in position, then we don't know if it's coming or going, let's wait until we do 
          nil
    else: # if this flight doesn't go to NYC, and is just flying over, show its final destination
         # possible enhancement
         # TODO: find the airport pair whose great-circle path comes closest to New York City, then show the farthest member of that pair
         # e.g. if this is a flight number from Dallas to Cancun to Boston, first determine that the Cancun-Boston pair passes cloer to New York than Dallas-Cancun, then determine that Cancun is farther from New York than Boston, so return Cancun
      return airports[-1]

if __name__ == "__main__":
  # doesn't support quotes in input because naively splits on whitespace
  stdin = " ".join(sys.stdin.readlines()).split()
  if not len(stdin):
    print('')
  print(Flyover.where(stdin[0], int(stdin[1]) )) # actual output

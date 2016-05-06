#!/usr/bin/python3
# encoding: utf-8
from __future__ import print_function
import re
from subprocess import check_output, CalledProcessError
import sys
import os.path

class Flyover:
  TRANSLATIONS = {
    "JB": "JBU",
  }

  flight_number_re = re.compile("^([A-Z]+)?(\d+)$")

  @classmethod
  def where(self, options, flight_number, delta_altitude):
    airline, number = self.flight_number_re.match(flight_number).groups()
    local_airports = [ ("K" + airport ) if len(airport) == 3 else airport for airport in options.airports.split(",")]

    if airline in self.TRANSLATIONS:
      airline = self.TRANSLATIONS[airline]

    # data is FlightNumbers.csv from http://www.virtualradarserver.co.uk/FlightRoutes.aspx
    # script assumes that the datafile is in the same directory as this script
    # script assumes that grep is installed (i.e. this script won't work on Windows, sorry! Pull Request would be accepted though.)
    try:
      flight_rows = check_output(["grep", "%s,%s,"%(airline, number), os.path.join(os.path.dirname(os.path.realpath(__file__)),  "FlightNumbers.csv") ]).decode("utf-8").strip().split("\r\n")
    except CalledProcessError:
      print("ERROR: FlightNumbers.csv doesn't exist. Run ./ensure_flightnumbers_csv_exists.sh to download it. ", file=sys.stderr)
      return

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
    if any([nyc_airport in airports for nyc_airport in local_airports]):
      # if this flight number goes to several airports, ignore the New York airports and the airports from which this flight does not come or go from New York. (because that's not a relevant destination here, except in potential odd cases)
      nyc_adjacent_airports = [airport for idx, airport in enumerate(airports) if (idx > 0 and airports[idx-1] in local_airports) or (idx < (len(airports) -1) and airports[idx+1] in local_airports) ]


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
    else: 
         # if this flight doesn't go to NYC, and is just flying over, don't show it.
         # possible enhancement
         # TODO: find the airport pair whose great-circle path comes closest to New York City, then show the farthest member of that pair
         # that would be, basically, the "most interesting" point on its current path, whether source or destination 
         # e.g. if this is a flight number from Dallas to Cancun to Boston, first determine that the Cancun-Boston pair passes cloer to New York than Dallas-Cancun, then determine that Cancun is farther from New York than Boston, so return Cancun
      return None # airports[-1]

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser(description='Usage: dump1090_to_nearest_flight.py [options]')
  parser.add_argument('-a', '--airports',
                      help="Your home airport(s), used to differentiate planes arriving, leaving or flying over. e.g. `KLGA,KJFK,KEWR`.",
                      required=False,
                      default='KLGA,KJFK,KEWR')
  args = parser.parse_args()

  # doesn't support quotes in input because naively splits on whitespace
  # stdin = " ".join(sys.stdin.readlines()).strip().split()
  stdin = (input() if (sys.version_info > (3, 0)) else raw_input()).split()
  if not len(stdin):
    print('')
  else:
    print(Flyover.where(args, stdin[0], int(stdin[1]) )) # actual output

#!/bin/bash
# encoding: utf-8

pushd $(dirname $0)
if [ -f FlightNumbers.csv ]; then
  mv FlightNumbers.csv FlightNumbers.csv.bak
fi
wget -N  http://www.virtualradarserver.co.uk/Files/FlightNumbers.csv
rm -rf flightnumbers.sqlite3
sqlite3 flightnumbers.sqlite3 -cmd ".mode csv" ".import FlightNumbers.csv flightnumbers"
popd
#!/bin/bash
# encoding: utf-8

if [ -f FlightNumbers.csv ]; then
  mv FlightNumbers.csv FlightNumbers.csv.bak
fi
wget -q -O $(dirname $0)/FlightNumbers.csv -nc http://www.virtualradarserver.co.uk/Files/FlightNumbers.csv
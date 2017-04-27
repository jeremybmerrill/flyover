#!/bin/bash
# encoding: utf-8
mv FlightNumbers.csv FlightNumbers.csv.bak
wget -q -O FlightNumbers.csv -nc http://www.virtualradarserver.co.uk/Files/FlightNumbers.csv
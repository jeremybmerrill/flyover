Adafruit Python LED Backpack
============================

Python library for controlling LED backpack displays such as 8x8 matrices, bar graphs, and 7/14-segment displays on a Raspberry Pi or BeagleBone Black.

Designed specifically to work with the Adafruit LED backpack displays ----> https://learn.adafruit.com/adafruit-led-backpack/overview

For all platforms (Raspberry Pi and Beaglebone Black) make sure your system is able to compile Python extensions.  On Raspbian or Beaglebone Black's Debian/Ubuntu image you can ensure your system is ready by executing:

````
sudo apt-get update
sudo apt-get install build-essential python-dev
````

You will also need to make sure the python-smbus and python-imaging library is installed by executing:

````
sudo apt-get install python-smbus python-imaging
````

Install the library by downloading with the download link on the right, unzipping the archive, navigating inside the library's directory and executing:

````
sudo python setup.py install
````

See example of usage in the examples folder.

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Written by Tony DiCola for Adafruit Industries. (With a few modifications by Jeremy B. Merrill, mostly in Matrix16x8.py)

MIT license, all text above must be included in any redistribution

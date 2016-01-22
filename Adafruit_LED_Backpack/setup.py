from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name 				= 'Adafruit_LED_Backpack',
	  version 			= '1.7.1',
	  author			= 'Tony DiCola',
	  author_email		= 'tdicola@adafruit.com',
	  description		= 'Library to control LED backpack displays such as 8x8 single and bi-color matrices, bargraphs, 7 segment, and 14 segment displays.',
	  license			= 'MIT',
	  url				= 'https://github.com/adafruit/Adafruit_Python_LED_Backpack/',
	  dependency_links	= ['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.6.5'],
	  install_requires	= ['Adafruit-GPIO>=0.6.5'],
	  packages 			= find_packages())

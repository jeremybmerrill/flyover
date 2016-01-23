           ___                                   ___                        ___           ___     
          /  /\                      ___        /  /\          ___         /  /\         /  /\    
         /  /:/_                    /__/|      /  /::\        /__/\       /  /:/_       /  /::\   
        /  /:/ /\  ___     ___     |  |:|     /  /:/\:\       \  \:\     /  /:/ /\     /  /:/\:\  
       /  /:/ /:/ /__/\   /  /\    |  |:|    /  /:/  \:\       \  \:\   /  /:/ /:/_   /  /:/~/:/  
      /__/:/ /:/  \  \:\ /  /:/  __|__|:|   /__/:/ \__\:\  ___  \__\:\ /__/:/ /:/ /\ /__/:/ /:/___
      \  \:\/:/    \  \:\  /:/  /__/::::\   \  \:\ /  /:/ /__/\ |  |:| \  \:\/:/ /:/ \  \:\/:::::/
       \  \::/      \  \:\/:/      ~\~~\:\   \  \:\  /:/  \  \:\|  |:|  \  \::/ /:/   \  \::/~~~~ 
        \  \:\       \  \::/         \  \:\   \  \:\/:/    \  \:\__|:|   \  \:\/:/     \  \:\     
         \  \:\       \__\/           \__\/    \  \::/      \__\::::/     \  \::/       \  \:\    
          \__\/                                 \__\/           ~~~~       \__\/         \__\/    


What's that plane flying overhead? 

I live underneath a flight path for airplanes arriving at LaGuardia Airport in New York. When I hear the planes, I get curious. Where are those people coming from? I wrote this to find out.

Hardware Setup
--------------

- an SDR antenna
- a Raspberry Pi
- a 16x8 LED matrix ([e.g.](https://www.adafruit.com/products/2037))

How does this work?
-------------------

On the Raspberry Pi, we're running [Dump1090](https://github.com/mutability/dump1090) to handle the hard work of determining what planes are in the sky nearby. Piggybacking on Dump1090's JSON, `dump1090_to_nearest_flight.py` outputs the flight number and change-in-altitude of the nearest plane, optionally restricting that plane to a given area and/or altitude . `flight_number_to_departure_airport.py` translates that flight number, using a database, to the mostly likely non-NYC airport that is that flight's departure airport or destination. `display_letters.py` displays that airport's code (and, maybe, eventually, the city name for non-US airports). 

TODO
----
- look up airport names for non-US airports and display them too. (Where right now we'd display EGLL, we should instead display EGLL (London Heathrow, UK)).

Theoretically Askable Questions
-------------------------------

*Are you a NIMBY who is opposed to noise, airplanes, travel, etc.?*

Nah. I can hear the planes, but it's not really annoying. I'm not worried or angry, just curious about the world around me... :)

I do have a cat named Nimby though.

*But airplanes flying overhead could crash on you! They are dangerous!*

No, they're not. Please don't contact me anymore.

*Why isn't this Python 3 compatible?*

I couldn't get the Adafruit Python LED Backpack library working in Python 3. That's probably because I'm bad at Python, not on them.

I would like to thank the Academy...
------------------------------------
This project would have been impossible without:

1. the maintainers of [dump1090](https://github.com/antirez/dump1090) and the [Mutability fork](https://github.com/mutability/dump1090).
2. the maintainers of the Virtual Radar Server flightnumbers dump.
3. @calus at the FlightAware forums who [pointed me there](http://discussions.flightaware.com/ads-b-flight-tracking-f21/mapping-n-numbers-to-departure-airports-t36511.html).
4. Adafruit for their cool hardware and libraries.
5. [Sam Keddy](http://samkeddy.com/) who created the Thintel font I'm using.


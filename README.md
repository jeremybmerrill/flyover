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

I live underneath a flight path for airplanes arriving at LaGuardia Airport in New York. When I hear the planes, I get curious: where are those people coming from? I wrote this to find out. You can read more about my feelings [here](http://jeremybmerrill.com/blog/2016/01/flyover.html).

How does this work?
-------------------

On the Raspberry Pi, we're running [Dump1090](https://github.com/mutability/dump1090) to handle the hard work of determining what planes are in the sky nearby. Piggybacking on Dump1090's JSON, `dump1090_to_nearest_flight.py` outputs the flight number and change-in-altitude of the nearest plane, optionally restricting that plane to a given area and/or altitude . `flight_number_to_departure_airport.py` translates that flight number, using a database, to the mostly likely non-NYC airport that is that flight's departure airport or destination. `display_letters.py` displays that airport's code (and, maybe, eventually, the city name for non-US airports). 

Build your own
---------------

[Follow the instructions!](/instructions.md) If something seems wrong or could be improved upon, please submit a pull request.

If you need to draw an area for your favorite flight path, use [geojson.io](http://geojson.io). That's what I used to generate [laguardia_area.geojson](laguardia_area.geojson).

TODO
----
- look up airport names for non-US airports and display them too. (Where right now we'd display EGLL, we should instead display EGLL (London Heathrow, UK)).
- maybe also track noise. cf. http://webtrak5.bksv.com/panynj4
- it appears Southwest's airplanes may broadcast their flight number as just the number, i.e. 539, not SWA539. 

Theoretically Askable Questions
-------------------------------

*Are you a NIMBY who is opposed to noise, airplanes, travel, etc.?*

Nah. I can hear the planes, but it's not really annoying. I'm not worried or angry, just curious about the world around me... :)

I do have a cat named Nimby though.

*But airplanes flying overhead could crash on you! They are dangerous!*

No, they're not. Please don't contact me anymore.

*Why isn't this Python 3 compatible?*

I couldn't get the Adafruit Python LED Backpack library working in Python 3. That's probably because I'm bad at Python, not on them.

*I have an idea to make this better. Can I send you a pull request?*

Yes, please. I would like that very much.

I would like to thank the Academy...
------------------------------------
This project would have been impossible without:

1. the maintainers of [dump1090](https://github.com/antirez/dump1090) and the [Mutability fork](https://github.com/mutability/dump1090).
2. the maintainers of the Virtual Radar Server [FlightNumbers dump](http://www.virtualradarserver.co.uk/FlightRoutes.aspx).
3. @calus at the FlightAware forums who [pointed me there](http://discussions.flightaware.com/ads-b-flight-tracking-f21/mapping-n-numbers-to-departure-airports-t36511.html).
4. Adafruit for their cool hardware and libraries.
5. [Sam Keddy](http://samkeddy.com/) who created the Thintel font I'm using.


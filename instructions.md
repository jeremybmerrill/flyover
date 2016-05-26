Flyover setup
=============

Here are instructions on how to build your own version of the [Flyover
notifier](http://jeremybmerrill.com/blog/2016/01/flyover.html). I can't
necessarily offer personalized support, but, hell, send me an email, I
might respond!

I've tried to make these instructions as detailed as possible, but if
something is imprecise, hard to understand or incorrect, please submit a
pull request or send me a note.

Hardware:
=========

You need the following pieces of equipment for an exact clone of my
setup; the cost should be about $100 (USD) total. If you're hardware and software savvy, you can certainly
substitute different things. They're probably available for sale at
somewhere other than Adafruit, but Adafruit is nice and friendly and
generally seem like good people. (I'm not getting anything in exchange
for linking to any of these projects, e.g. referral points or anything.)
You can also use [FlightAware's shopping list](https://flightaware.com/adsb/piaware/build).

-   [Raspberry Pi 2](https://www.adafruit.com/products/2358) (I'm sure the new Pi 3 will work too, and it includes WiFi)
    -   [Power adapter](https://www.adafruit.com/products/1995)
    -   [Wi-Fi adapter](http://www.amazon.com/gp/product/B003MTTJOY?psc=1&redirect=true&ref_=od_aui_detailpages00) (unless you can reach your device with an ethernet cable, in which case you don't need this)
    -   [microSD card](http://www.bestbuy.com/site/samsung-evo-32gb-microsdhc-class-10-uhs-1-memory-card-red-white/4568505.p?id=1219769553726&skuId=4568505&cmp=RMX) (You don't need 32gb, 8gb would be fine.)
    -   an ethernet cable (if you buy a Wi-Fi adapter, the ethernet cable is for initial setup only, so you'll only need the cable for a few minutes -- just borrow it from something)
-   [Software-Defined Radio stick and antenna](https://www.adafruit.com/products/1497)
-   [16x8 LED matrix screen](https://www.adafruit.com/products/2037) (or substitute your own display, this one wasn't the best choice for this project, since it can only display three characters)
-   [Female-to-female Jumpers](https://www.adafruit.com/products/266) (or a "[Pi Cobbler](https://www.adafruit.com/products/2029)", breadboard and male-to-male jumpers)
-   [Soldering Iron](https://www.adafruit.com/products/180) and [Solder](https://www.adafruit.com/products/1886)

Setup
=====

Set up SD Card with operating system
------------------------------------

1.  download the Raspbian operating system from here [https://www.raspberrypi.org/downloads/raspbian/](https://www.raspberrypi.org/downloads/raspbian/), current version is Jessie
2.  once it's downloaded, unzip it, you should get an .img file
3.  now we need to copy it to the SD Card, but we can't just drag-and-drop it, so follow these instructions:
    a.  plug the SD card into the computer using a microSD reader (or, more likely, a microSD-to-SD adapter and an SD card reader
    b.  run this command on Linux or Mac: `$ sudo dd bs=4M if=2015-11-21-raspbian-jessie.img of=/dev/mmcblk0` on windows, there's probably an equivalent, but I don't know what it is. It's definitely doable and not terribly difficult though.
4.  now just insert the card in the Raspberry Pi

Connecting Your Computer to the Raspberry Pi
--------------------------------------------

now we have to figure out how to talk to the raspberry pi.

1.  plug it all in. don't worry about the SDR antenna or the display yet. Just plug the SD card into the Raspberry Pi and plug the power adapter into the Pi (and into the wall). The lights on the Raspberry Pi should start blinking.
2.  Open the command line on Linux or Mac (if you use Windows, download PuTTY and use that) and type `ssh pi@raspberrypi.local`
3.  Enter the password `raspberry`.
4.  You should now see a prompt that begins with \`pi@raspberrypi\`

If you get an error message like: `ssh: Could not resolve hostname
raspberrypi4.local: Name or service not known`

That means that your home network isn't set up to route via Avahi.
You'll need to find the Raspberry Pi's IP address directly. You'll need
to log into your router (probably at [http://192.168.1.1](http://192.168.1.1)), view the list
of existing DHCP leases, and find the one belonging to your Raspberry
Pi. I can't give you more specific instructions because it depends on
your router version. It will probably be something like `192.168.1.xxx`,
where `xxx` is a number less than 255. It might also be something like
`10.xxx.xxx.xxx`

Once you find it, try this:

1.  Open the command line on Linux or Mac (if you use Windows, download PuTTY and use that) and type `ssh pi@192.168.1.xxx`
2.  Enter the password `raspberry`.
3.  You should now see a prompt that begins with `pi@raspberrypi`

Installing dump1090
-------------------

More detailed instructions are found here:
[https://github.com/mutability/dump1090](https://github.com/mutability/dump1090)

Now you should plug in the SDR adapter to one of the USB ports on the
Raspberry Pi. Doesn't matter which.

You should run these commands in the command-line window that begins
with `pi@raspberrypi`. Don't type the $. (It just signifies that
you're in the command line.)

````
$ wget https://github.com/mutability/mutability-repo/releases/download/v0.1.0/mutability-repo_0.1.0_armhf.deb`
$ sudo dpkg -i mutability-repo_0.1.0_armhf.deb
$ sudo apt-get update && sudo apt-get install dump1090-mutability
```

Now we have to configure the dump1090 software. The defualt options are
all okay, but you need to fill out the latitude/longitude of the spot
you're in now. Google Maps will tell you. Navigate with the arrow keys and accept with Enter.

`$ sudo dpkg-reconfigure dump1090-mutability`

`$ sudo apt-get install lighttpd && sudo lighty-enable-mod dump1090`

Now we're doing some detailed, boring stuff to make the hardware work.
````
$ echo "blacklist dvb_usb_rtl28xxu" | sudo tee /etc/modprobe.d/blacklist.conf`
$ echo "SUBSYSTEMS==\"usb\", ATTRS{idVendor}==\"0bda\", ATTRS{idProduct}==\"2838\", MODE:=\"0666\"" | sudo tee /etc/udev/rules.d/50-sdr.rules
$ sudo service udev restart
````

Now, you should be able to go to
[http://raspberrypi.local:80](http://raspberrypi.local:80) or
[http://192.168.x.xxx:80](http://192.168.x.xxx:80) (the same as
above). And there should be a fun page from dump1090 showing planes
overhead.

Installing Flyover
------------------

Run these commands, still on the command prompt on your computer that
represents the Raspberry Pi.c

Installs a few libraries: `$ sudo apt-get install python-smbus python-imaging libgeos-dev`

And some Python libraries: `$ pip install geojson shapely`

Download and unzip the Flyover code: 
````
$ wget https://github.com/jeremybmerrill/flyover/archive/master.zip
$ unzip master.zip
$ mv flyover-master flyover
````


Move this script to `/etc/cron.d/` tells the computer to run the Flyover code once every thirty seconds.
````
$ sudo mv flyover/flyover-cron /etc/cron.d/
$ sudo chown root:root /etc/cron.d/flyover-cron
````

And enable the Dump1090 web interface in the location that Flyover expects it.

`$ sudo mv flyover/89-dump1090.conf /etc/lighttpd/conf-enabled/89-dump1090.conf`

And download the latest database of routes from FlightRadarServer:

`$ flyover/ensure_flightnumbers_csv_exists.sh`

Finishing up
============

Display Assembly
----------------
Solder together the LED matrix, following Adafruit's instructions.

Hook it up to the Pi. If you have a Raspberry Pi 2 Model B like I do, you'd be following a pin-out diagram [like this](http://www.raspberry-projects.com/pi/pi-hardware/raspberry-pi-2-model-b/rpi2-model-b-io-pins). Connect the following pins on the display (they're labeled on the back of the display board) to the Pi:

 - *VCC* pin to pin #4, to supply 5V power
 - *GND* pin to pin #6, for ground
 - *SCL* pin to pin #5 for I2C SCL (who knows what that stands for, maybe clock?)
 - *SDA* pin to pin #3 for I2C SDA (maybe data?)
 
You can connect the wires with female-to-female jumpers or by soldering. The pins are labeled on the front of the display board as `D`, `C`, `-` and `+`, where `D` is *SDA*, `C` is *SCL*, `+` is *VCC* and `-` is *GND*.

Almost there...
---------------
Restart the Pi. (Either type `sudo reboot` or just unplug it and plug it back in again) It should just work (assuming there's a plane flying overhead!!). It might not. Open an issue with
the error if it doesn't... 

Details...
==========

Copyright 2016 Jeremy B. Merrill.

Thanks to my dad for sending in fixes to these instructions!

This work is licensed under the **CC 3.0 BY-NC-SA** license.

You follow this guide at your own risk. Soldering, in particular, can be
dangerous and you shouldn't do it if you don't know what you're doing.
If you break your stuff or set your house on fire or give your dog lead poisoning, it's your fault, not
mine.

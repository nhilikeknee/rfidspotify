#!/bin/sh
# launcher.sh

# this shell script will automatically run the program without the user needing to click on anything or even have a monitor/UI



# 1. Navigate to home directory 
# 2. Navigate to directory with the player.py file, in my case, /Documents/rfidspotify 
# 3. Then execute python script
# 4. Go back home


cd /
cd home/pi/Documents/rfidspotify
sudo python3 player.py
cd /


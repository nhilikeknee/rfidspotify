#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep


# TODO: Fill in your own unique IDs
DEVICE_ID="YOUR_UNIQUE_DEVICE_ID OR PICK ONE FROM THE DEVICE LIST BELOW"
CLIENT_ID="YOUR_UNIQUE_CLIENT_ID"
CLIENT_SECRET="YOUR_YNIQUE_CLIENT_SECRET"


# DEVICE LIST
# TODO: Fill out IDs for as many different devices as you want
PIXEL_PHONE_DEVICE_ID = 'DEVICE_ID_1'
IPAD_TABLET_DEVICE_ID = 'DEVICE_ID_2'
RASPBERRY_PI_DEVICE_ID = 'DEVICE_ID_3'
LAPTOP_DESKTOP_APP = 'DEVICE_ID_4'
WEB_PLAYER_CHROME = 'DEVICE_ID_5'



# define class of Music objects 
# savedID:  linked ID number from physical RFID tag to this particular song/album/playlist
# URI:      unique to each song/album/playlist, retrieved from Spotify  
class Music: 
    def __init__(self, savedID, content_type, URI): 
        self.savedID = savedID
        self.content_type = content_type
        self.URI = URI
   



 
# creating empty list       
music_collection = [] 
  
# TODO: add in new music (tracks/albums/playlists) here:
# Music(known RFID, content type, Spotify URI)


# album Golden Hour by Kacey Musgraves
music_collection.append( Music(536413732569, 'album', 'spotify:album:7f6xPqyaolTiziKf5R5Z0c') )

#playlist 'This is Lady Gaga' by Spotify
music_collection.append( Music(288610032533, 'playlist', 'spotify:playlist:37i9dQZF1DXc7FZ2VBjaeT') )

# song 'Wuthering Heights' by Kate Bush
music_collection.append( Music(1086152769118, 'track', 'spotify:track:5YSI1311X8t31PBjkBG4CZ') )




# shouldn't need to modify anything below this line for updating music selection

while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri="http://localhost:8080",
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
            
            while True:
                # Switch to specified device
                if id==152222642510:
                    print('switching to iPad')
                    DEVICE_ID=IPAD_TABLET_DEVICE_ID
                    break
                elif id==360311960002:
                    print('switching to Pixel')
                    DEVICE_ID=PIXEL_PHONE_DEVICE_ID
                    break

                # loop through list of existing linked RFID tags (music_collection) and play the corresponding track/album/playlist
                for obj in music_collection:
                    print(obj.savedID)
                    if id==obj.savedID:
                        print(obj.savedID)
                        print(obj.URI)
                        print('on this device: ')
                        print(DEVICE_ID)
                        if obj.content_type=='track':
                            sp.start_playback(device_id=DEVICE_ID, uris=[obj.URI])
                        else:
                            sp.start_playback(device_id=DEVICE_ID, context_uri=obj.URI)
                        sleep(2)
                        continue
                break
            

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
   
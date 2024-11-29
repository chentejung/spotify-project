# Spotify-project

## Getting started
* Create a Spotify app to obtain the Client ID and Secret
  * Go to https://developer.spotify.com/documentation/web-api and log in with your Spotify account.
  * Follow the steps in the "Getting Started" guide to create an app and obtain the Client ID and Secret.

### Environment
* Python: 3.9
* Docker: 1.24

##### .env sample
```
CLIENT_ID = ""
CLIENT_SECRET = ""
DB_ROOT_USERNAME = ''
DB_ROOT_PASSWORD = ''
DB_HOST = localhost
DB_PORT = 27017
DB_NAME = "Spotify"
SPOTIFY_TOKEN_OWNER = ''
```
#### Initialization environment
```
$ pip install -r requirements.txt  
$ docker compose config  # Check docker-compose.yml output with environment variables
$ docker compose up -d  # Start MongoDB
```

#### Retrieve data
1. Retrieve singer name list on your own or refer to __getArtist.py__
2. Save data in __.txt__
3. Edit __getData.py__ and uncomment 1st part, replace filePath with yours
```
if __name__ == '__main__':
    filePath = '/home/ellie/mineProject/spotify/files/source/20231206/missingArtist.txt'
    collName = getArtistId(filePath)

    # infoType = 'artist'
    # sourceTab = 'rap_ID'
    # newTabName = 'rapper_information'
    # InfoFromSpotify(infoType, sourceTab, newTabName)

    # infoType = 'album'
    # sourceTab = 'rapper_information'
    # newTabName = 'rapper_album_information'
    # InfoFromSpotify(infoType, sourceTab, newTabName)

    # infoType = 'trackGen'
    # sourceTab = 'rapper_album_information'
    # newTabName = 'rapper_track_general_information'
    # InfoFromSpotify(infoType, sourceTab, newTabName)
```

4. Execute getData.py and retrieve singers' Spotify ID
```
python getData.py
```

5. Edit __getData.py__ and comment 1st part, uncomment 2nd part.  __Repeat "Step 4" to retrieve artist data from Spotify__
```
if __name__ == '__main__':
    # filePath = '/home/ellie/mineProject/spotify/files/source/20231206/missingArtist.txt'
    # collName = getArtistId(filePath)

    infoType = 'artist'
    sourceTab = 'rap_ID'
    newTabName = 'rapper_information'
    InfoFromSpotify(infoType, sourceTab, newTabName)

    # infoType = 'album'
    # sourceTab = 'rapper_information'
    # newTabName = 'rapper_album_information'
    # InfoFromSpotify(infoType, sourceTab, newTabName)

    # infoType = 'trackGen'
    # sourceTab = 'rapper_album_information'
    # newTabName = 'rapper_track_general_information'
    # InfoFromSpotify(infoType, sourceTab, newTabName)
```

6. Follow same operation in __Step 5__ for retrieving __album information (uncomment part 3)__ and __track information (uncomment part 4)__


## Website
### Function Display

1. Execute __flaskforUse.py__ to start the web
```
python flaskforUse.py
```
2. Access website on __http://[server IP]:5000__

### At Front Page
* Check singer popularity and followers data
* Login Spotify account for personal information

#### Search artist
http://[server IP]:5000/__artist/[Singer's name]__  --->  Ex: http://127.0.0.1:5000/artist/Kendrick Lamar

#### List albums of certain singer and check detailed track information
http://[server IP]:5000/__album/[Singer's name]__   --->  Ex: http://127.0.0.1:5000/album/Kendrick Lamar

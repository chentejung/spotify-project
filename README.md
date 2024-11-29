# Spotify-project

## Getting started
* Create a Spotify app to obtain the Client ID and Secret
  * Go to https://developer.spotify.com/documentation/web-api and log in with your Spotify account.
  * Follow the steps in the "Getting Started" guide to create an app and obtain the Client ID and Secret.
* Install Docker

###### .env sample
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

#### Retrieve data steps
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

5. Edit __getData.py__ and comment 1st part, uncomment 2nd part
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

import os
import requests
from googlesearch import search
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from DB import Spotify
import backendFunc
import random
import time


'''
search Artist Spotify ID
'''
# decide if this function can be modualized??
def getArtistId(filePath):
    genre = filePath.replace('files/source/', '').split('/')[0]
    with open(filePath, 'r') as f:
        content = f.read().splitlines()#[32:]
    colName = ['artist_ID_url', 'playlist_ID_url']
    tempList = []
    collName = f'{genre}_ID'
    # collName = f'rap_ID'

    '''start searching'''
    for idx1, name in enumerate(content):
        smallist = []
        print(idx1)
        try:
            result = search(f'{name} spotify', sleep_interval= random.randint(3,13), num_results=2)

            # so far filter is no use, need to modify
            filter1 = 'https://open.spotify.com/artist'
            filter2 = 'https://open.spotify.com/playlist'

            # save the first 2 results only
            for idx2, element in enumerate(result):
                if idx2 < 2:
                    if element.find(filter1) or element.find(filter2):
                        smallist.append(element)
                else:
                    continue
            dict1 = {'id': name, colName[0]: smallist[0], colName[1]: smallist[1]}
            tempList.append(dict1)

            if len(tempList) > 20:
                # save ID into DB
                _table = Spotify(collName)
                _table.insert_many(tempList)
                tempList = []
                # print('Save spotify artist ID completed!')

            elif (len(tempList) < 20) and (idx1+1 == len(content)):
                _table = Spotify(collName)
                _table.insert_many(tempList)

        except Exception as e:
            _table = Spotify(collName)
            _table.insert_many(tempList)

            print('Save last batch before error!')
            print(e)
            break

    print('Search and save ID completed!')
    return collName


'''
search through Spotify API
'''
def InfoFromSpotify(srcType, srcTab, newTabName):
    if srcType == 'artist': 
        _table = Spotify(srcTab)

        # remove duplicate and garbage data
        srcCol = 'id'
        df1 = pd.DataFrame(_table.aggregate_number_search(srcCol))
        print(df1.shape[0])
        startRow = 2
        # print(df1)
        df1 = df1.iloc[startRow:]
        totalNum = df1.shape[0]
        url = f'https://api.spotify.com/v1/artists'
        trashData = []

        '''check missing artist, re-search'''
        # list1 = df1['_id'].values.tolist()
        # with open('/home/ellie/mineProject/spotify/files/source/rap/20231128/artistlist20231128.txt', 'r') as f:
        #     content = f.read().splitlines()
        # list2 = list(dict.fromkeys(content))
        # list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
        
        # from saveFile import saveTxt
        # saveTxt(list_dif, 'files/source', 'missingArtist.txt', 'w')


    elif srcType == 'album':
        table1 = Spotify(srcTab)
        srcCol = ['name', 'id']
        df1 = pd.DataFrame(table1.get_collection_search_specific_columns(srcCol))
        print(df1)
        totalNum = df1.shape[0]
        url = f'https://api.spotify.com/v1/artists'

        nextList = 0
        # nextList = 2

    elif srcType == 'trackGen':
        table1 = Spotify(srcTab)
        srcCol = 'items.id'
        startRow = 1
        dfList = pd.DataFrame(table1.aggregate_number_search(srcCol))['_id'][startRow:].values.tolist()   # retrieve album ID for tracks search
        flatList = [item for sublist in dfList for item in sublist]  # flatten list in list situation
        df1 = pd.Series(flatList).drop_duplicates().reset_index(drop=True)
        # print(df1)
        totalNum = df1.shape[0]
        print(totalNum)
        url = f'https://api.spotify.com/v1/albums'

        nextList = 0



    '''search information with Spotify API'''
    try:
        srcID = os.getenv("SPOTIFY_TOKEN_OWNER")
        collName = 'spotify_token'
        type, token = backendFunc.checkToken(collName, srcID)
        headers = {'Authorization': f"{type} {token}"}

        count = 0
        # count = 789
        templist = []
        while count < totalNum:
            time.sleep(random.randint(1,5))
            if srcType == 'artist':
                name = df1['_id'][startRow]
                print(name)
                idGet = _table.get_collection_search_by_id_name(name)['artist_ID_url']
                id1 = idGet.split('/')[-1]
                result1 = idGet.replace(id1, '')

                if result1 != 'https://open.spotify.com/artist/':
                    trashData.append(name)
                    count+=1
                    startRow+=1
                    continue
                else:
                    srcUrl = f'{url}/{id1}'

            elif srcType == 'album':
                id = df1['id'][count]
                name = df1['name'][count]
                if nextList == 0:
                    srcUrl = f'{url}/{id}/albums?limit=50&offset=0'
                elif nextList == 2:
                    srcUrl = 'https://api.spotify.com/v1/artists/0e3TXa6cyJQl5vE6DFHfjT/albums?include_groups=album,single,compilation,appears_on&offset=100&limit=50'

            elif srcType == 'trackGen':
                id = df1[count]
                if nextList == 0:
                    srcUrl = f'{url}/{id}/tracks?limit=50&offset=0'
                elif nextList == 2:
                    srcUrl = ''

            '''start API search'''
            print(srcUrl)
            response = backendFunc.requestUrl(srcUrl, headers)
            
            # handle token expired scenario
            if response.status_code == 401:
                type, token = backendFunc.checkToken(collName, srcID)
                headers = {'Authorization': f"{type} {token}"}
                continue

            else:
                resSave = response.json()
                templist.append(resSave)
                if len(templist) == 20:
                    newTable = Spotify(newTabName)
                    newTable.insert_many(templist)
                    templist = []
                    print(f'Save data batch {count} !')

                elif (len(templist) < 20) and ((count+1) == totalNum):
                    newTable = Spotify(newTabName)
                    newTable.insert_many(templist)
                    print(f'Save last batch!')
                    break

                if 'startRow' in locals(): 
                    startRow+=1

                # if there is next url for continuous search, continue search
                if "nextList" in locals():
                    nextUrl = resSave['next']
                    if (nextUrl != 'null') and (nextUrl != None):
                        nextList=1
                        srcUrl = nextUrl
                        continue
                    else:
                        nextList=0
                        count+=1

        # save trash data for remove
        if srcType == 'artist':
            from saveFile import saveTxt
            trashData.append(f'"Total people searched": {totalNum}, "Total_missing": {len(templist)}')
            saveTxt(trashData, 'files', 'trashRapperList.txt', 'w')

    except Exception as e:
        print(e)



if __name__ == '__main__':
    # filePath = '/home/ellie/mineProject/spotify/files/source/20231206/missingArtist.txt'
    # collName = getArtistId(filePath)

    # infoType = 'artist'
    # sourceTab = 'rap_ID'
    # newTabName = 'rapper_information'
    # InfoFromSpotify(infoType, sourceTab, newTabName)

    # infoType = 'album'
    # sourceTab = 'rapper_information'
    # newTabName = 'rapper_album_information'
    # InfoFromSpotify(infoType, sourceTab, newTabName)

    infoType = 'trackGen'
    sourceTab = 'rapper_album_information'
    newTabName = 'rapper_track_general_information'
    InfoFromSpotify(infoType, sourceTab, newTabName)
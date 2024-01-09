import pandas as pd
import numpy as np
from DB import Spotify
import backendFunc
import os
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


'''return artist popularity sort'''

def sortPopularity(sorItem):
    if sorItem == 'followers':
        sort2 = 'popularity'
    elif sorItem == 'popularity':
        sort2 = 'followers'

    collName = 'rapper_information'
    _table = Spotify(collName)
    dfPop = pd.DataFrame(_table.sort_search(sorItem, 'desc'))

    # show top 50 data
    dfshow = dfPop[:50]

    sortName = dfshow['name'].str.replace(',', '-').to_list()
    if sorItem == 'followers':
        sortData = dfshow[sorItem].apply(lambda x: x['total']).to_list()
    elif sorItem == 'popularity':
        sortData = dfshow[sorItem].to_list()


    '''get genre data'''
    show1 = 'genres'
    showtmp = dfshow[show1].to_list()
    showtmp2 = [item for sublist in showtmp for item in sublist]
    showSer = pd.Series(showtmp2).value_counts()
    showName = list(showSer.index)
    showData = list(showSer)
    # print(sort2Data)

    # value to return
    titleList = [sorItem, sort2, show1]
    dataList = dict(zip(sortName, sortData))
    genreList = dict(zip(showName, showData))
    # print(genreList)

    return titleList, dataList, genreList



'''
show track data in the album, sort by popularity
'''

def trackData(albumID):
    collName = 'rapper_track_general_information'
    table = Spotify(collName)
    query = {"$regex":f"{albumID}"}
    df1 = pd.DataFrame(table.get_collection_search_query('href', query)['items'])  #retrieve each track's api from DB
    # print(df1)

    # request track information through API
    srcID = os.getenv("SPOTIFY_TOKEN_OWNER")
    collName = 'spotify_token'
    type, token = backendFunc.checkToken(collName, srcID)
    headers = {'Authorization': f"{type} {token}"}

    list1 = []
    for i in df1['href']:
        res = backendFunc.requestUrl(i, headers, 'json')
        list1.append(res)
    df2 = pd.DataFrame.from_records(list1)
    col = ['Track Name', 'Artists', 'Artist Number', 'Popularity', 'Duration (minutes)']
    list2 = []

    '''retrieve data from API call'''
    for j in range(df2.shape[0]):
        tmpSer = df2.iloc[j]

        if len(list2) == 0:
            albumName = tmpSer['album']['name']
            imgUrl = tmpSer['album']['images'][1]['url']
        singList = []
        for w in tmpSer['artists']:
            singList.append(w['name'])
        numArt = len(tmpSer['artists'])
        songLen = round((tmpSer['duration_ms']) / 60000, 2)
        list2.append({
            col[0]: tmpSer['name'],
            col[1]: singList,
            col[2]: numArt,
            col[3]: tmpSer['popularity'],
            col[4]: songLen
        })

    dfshow = pd.DataFrame.from_dict(list2)
    dfshow = dfshow.sort_values(by='Popularity', ascending=False)
    dfDict = dfshow.to_dict('records')
    # print(dfDict)

    return albumName, imgUrl, col, dfDict



    

if __name__ == '__main__':
    # sort = 'followers'
    # sortPopularity(sort)
    albumID = '1GG6U2SSJPHO6XsFiBzxYv'
    trackData(albumID)
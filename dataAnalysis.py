import pandas as pd
import numpy as np
from DB import Spotify
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
    

# if __name__ == '__main__':
#     sort = 'followers'
#     sortPopularity(sort)
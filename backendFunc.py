import os
import requests
from dotenv import load_dotenv
load_dotenv()
import json
import pandas as pd
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import socks
import socket
from requests_tor import RequestsTor
from fake_useragent import UserAgent



def checkToken(tokenTable, name):
    from DB import Spotify
    # retrieve token from db
    _table = Spotify(tokenTable)
    infoToken = _table.get_collection_search_by_id_name(name)
    if infoToken:
        tokenGetime = infoToken['Token Retrieve date']
        tokenfromDB = infoToken['access_token']
        typefromDB = infoToken['token_type']

        # check if token expires
        timegap = timedelta(hours=1)
        timeNow = datetime.now()
        if (timeNow - tokenGetime) > timegap:
            res1 = getToken(name)
            newToken = res1['access_token']

            # update db info
            #tokenTable.update_one('access_token', tokenfromDB, newToken)
            _table.delete_one_by_id_name(name)
            _table.insert_one(res1)
            return typefromDB, newToken
        else:
            return typefromDB, tokenfromDB
    else:
        res = getToken(name)
        _table.insert_one(res)

        # should rerun this if-else and get token only from DB, need to change code
        accToken = res['access_token']
        authType = res['token_type']
        return authType, accToken


# get access token and token_type
def getToken(idName):
    tokenUrl = "https://accounts.spotify.com/api/token"
    headers1 = {'Content-Type': 'application/x-www-form-urlencoded',}
    accessData = {'grant_type': 'client_credentials', 'client_id': os.getenv('CLIENT_ID'),
                'client_secret': os.getenv('CLIENT_SECRET')}
    response1 = requests.post(tokenUrl, headers=headers1, params=accessData).json()
    response1['Token Retrieve date'] = datetime.now()
    response1['id'] = idName
    return response1


# for html request use
def requestUrl(srcUrl, headers = None, resType = None):
    user_agent = UserAgent()
    if headers is None:
        headers = {
            'user-agent': user_agent.random
        }
    else:
        headers['user-agent'] = user_agent.random

    '''code for using tor'''
    # socks.set_default_proxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr='127.0.0.1', port=9050)
    # socket.socket = socks.socksocket
    # rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)
    # r = rt.get(srcUrl, headers=headers)
    # return r
    # print(r.text)

    r = requests.get(srcUrl, headers=headers)
    if resType == 'soup':
        soup = BeautifulSoup(r.content, 'lxml')
        return soup
    elif resType == 'json':
        return r.json()
    else:
        return r
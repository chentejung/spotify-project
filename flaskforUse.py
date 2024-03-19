from DB import Spotify
import os
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from flask import Flask, render_template, redirect, request, url_for, session
from authlib.integrations.flask_client import OAuth
# from authlib.common.security import generate_token
import dataAnalysis
from genius1 import findLyrics

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/", methods=['POST', 'GET'])
def hello():
    text = "Hello, World! Searching for music?"
    text2 = "Or login your Spotify discover some of your music taste🫶🏻"
    if request.method == 'POST':
        if 'srcFilter' in request.form:
            srcItem = request.form['srcFilter']
            return redirect(url_for('showStats', srcFilter=srcItem))
        else:
            session['client_id'] = request.form['clientId']
            session['client_secret'] = request.form['clientSecret']
            return redirect(url_for('spotifyOauth'))
    else:
        return render_template('welcomepage.html', text=text, text2=text2)

@app.route("/stats/<string:srcFilter>")
def showStats(srcFilter):
    title, srcData, genreData = dataAnalysis.sortPopularity(srcFilter)
    return render_template('stats1.html', value1=title, value2=srcData, value3=genreData)

@app.route("/login")
def spotifyOauth():
    global spotifyLogin
    spotifyLogin = OAuth(app).register(
    name='spotify',
    client_id=session.get('client_id'),
    client_secret=session.get('client_secret'),
    access_token_url='https://accounts.spotify.com/api/token',
    access_token_params=None,
    authorize_url='https://accounts.spotify.com/authorize',
    authorize_params=None,
    client_kwargs={'scope': 'user-read-private user-read-email'},
)

    callback_uri = url_for('callback', _external=True)
    return spotifyLogin.authorize_redirect(callback_uri)


@app.route("/callback")
def callback():
    # retrieve access token back
    tokenResp = spotifyLogin.authorize_access_token()
    session['apiToken'] = tokenResp['access_token']
    session['refreshToken'] = tokenResp['refresh_token']
    return redirect(url_for('userInfo'))

@app.route("/user")
def userInfo():
    # retrieve user info and show analysis
    userInfo = dataAnalysis.userProfile(session.get('apiToken'))
    return render_template('userProfile.html', userInfo=userInfo)


@app.route("/artist/<string:name>")
def query_artist(name):
    if name:
        try:
            info = Spotify('rapper_information').get_collection_search_query('name', name)
            # choose 320*320
            src = info['images'][1]['url']
            return render_template('index.html', artist=info, img=src)
        except:
            return 'No artist found!'

@app.route("/album/<string:name>")
def query_ablum(name):
    res = dataAnalysis.ablumData(name)
    if res == 0:
        return 'No album information found!'
    else:
        return render_template('index2v2.html', artistName = res[0], table_data = res[1], colname = res[2])
        

@app.route('/tracks/<string:artName>/<string:albName>')  # fisrt one is artist's name, second one is album name
def trackinfoGen(artName, albName):
    res = dataAnalysis.trackDataGen(artName, albName)
    if res == 0:
        return 'No track information yet!'
    else:
        return render_template('trackInfo1.html', albumName = res[0], albumID = res[1], table_data = res[2], colname = res[3], artName = res[4])
        

@app.route("/tracks/detail/<string:albumID>")
def trackDetail(albumID):
    albName, imgUrl, colName, list = dataAnalysis.trackData(albumID)
    return render_template('trackInfo2.html', albumName = albName, imgUrl = imgUrl, table_data = list, colname = colName)


@app.route("/tracks/lyrics/<string:artName>/<string:tracName>")
def lyricsShow(artName, tracName):
    res = findLyrics(artName, tracName)
    if res == 0:
        return 'No lyrics information found!'
    else:
        return render_template('trackLyrics.html', table_data = res, tracName = tracName)
        


app.run(port=5000, debug=True, host='0.0.0.0')
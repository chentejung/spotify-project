from DB import Spotify
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from flask import Flask, render_template, redirect, request, url_for, jsonify, make_response
import dataAnalysis
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello():
    text = "Hello, World! Searching for music?"
    if request.method == 'POST':
        srcItem = request.form['srcFilter']
        return redirect(url_for('showStats', srcFilter=srcItem))
    else:
        return render_template('welcomepage.html', text=text)

@app.route("/stats/<string:srcFilter>")
def showStats(srcFilter):
    title, srcData, genreData = dataAnalysis.sortPopularity(srcFilter)
    return render_template('stats1.html', value1=title, value2=srcData, value3=genreData)

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
    if name:
        try:
            # columns=['Album_Name', 'Type', 'Total_tracks','Release_date', 'Artists', 'Available_markets','External_urls']
            columns=['Album_cover', 'Album_Name', 'Type', 'Release_date', 'Total_tracks', 'Artists','External_urls']

            # search album info using artist name and ID, for specific
            name1 = 'rapper_album_information'
            name2 = 'rapper_information'
            table1 = Spotify(name1)
            table2 = Spotify(name2)

            artistID = table2.get_collection_search_query('name', name)['id']
            query = {'items.artists.name': name, 'items.artists.id': artistID}
            df = pd.DataFrame(table1.get_collection_search_query_multiple_conditions(query, 'and'))
            if not df.empty:
                templist1 = []
                for i in df['items']:
                    for j in i:
                        artisList = []
                        for idx, x in enumerate(j['artists']):
                            if name in x.values():
                                len1 = len(j['artists'])
                                for y in range(len1):
                                    artisList.append(j['artists'][y]['name'])
                                templist1.append({columns[0]: j['images'][0]['url'], 
                                                columns[1]: j['name'], 
                                                columns[2]: j['album_type'], 
                                                columns[3]: j['release_date'], 
                                                columns[4]: j['total_tracks'], 
                                                columns[5]: artisList, 
                                                columns[6]: j['external_urls']['spotify']})
            # print(templist1)
            
            dfshow = pd.DataFrame.from_dict(templist1)

            # remove duplicated data and sort by release date in descending order
            dfshow['Release_date'] = pd.to_datetime(dfshow['Release_date'], format='%Y%m%d', errors='ignore')
            dfshow = dfshow.loc[dfshow.astype(str).drop_duplicates().index].sort_values(by='Release_date', ascending=False).reset_index(drop=True)
            dfDict = dfshow.to_dict('records')

            return render_template('index2v2.html', table_data = dfDict, colname = columns)
                
            # return render_template('index2.html', tables=[dfshow.to_html(classes='data', header="false")])

        except:
            return 'No album information found!'
        

@app.route('/album/tracks/<string:name>')  # name should be album name
def trackinoGen(name):
    if name:
        try:
            collName1 = 'rapper_album_information'
            collName2 = 'rapper_track_general_information'
            table1 = Spotify(collName1)
            table2 = Spotify(collName2)

            query1 = {'items.name': name}
            df1 = pd.DataFrame(table1.aggregate_number_search('items.id', 'count', query1))
            df2 = df1.loc[0]
            index1 = df2['name'].index(name)
            albumID = df2['_id'][index1]
            # print(albumID)
            
            # albumID = '3C2aiQ7oAB7shCeH4uXmcC'
            query2 = {"$regex":f"{albumID}"}
            res = table2.get_collection_search_query('href', query2)
            # print(res)
            templist = []
            for i in res['items']:
                singerlist = []
                for j in i['artists']:
                    singerlist.append(j['name'])
                templist.append([i['name'], singerlist])
            # print(templist)
            return templist

        except:
            return 'No track information yet!'
        


app.run(port=5000, debug=True)
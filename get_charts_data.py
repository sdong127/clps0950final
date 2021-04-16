import csv
import pandas as pd
import numpy

charts_corpus = open('songs_artists.txt','w')
songs = []
artists = []
with open('charts.csv', 'r') as file:
    charts = csv.reader(file)
    for row in charts:
        songs.append(row[2] + ' ')
        artists.append(row[3] + ' ')
    file.close()

charts_series = pd.Series(data=songs,index=artists)
artist_list = charts_series.index
song_list = charts_series.values

charts_corpus.writelines(artist_list)
charts_corpus.writelines(song_list)
charts_corpus.close()

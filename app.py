from flask import Flask,render_template, request, redirect, url_for
import spacy
import pandas as pd
import numpy as np
from contractions import CONTRACTION_MAP
import re
import csv
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from datetime import date, timedelta


app = Flask(__name__)

options = [0, 1, 2]


@app.route('/', methods=['GET','POST'])
def homepage():
    return render_template('homepage.html', options=options)


def dropdown():
    selectValue = request.form.get('options')
    print(selectValue)
    return selectValue

def artist_dropdown():
    selectValue2 = request.form.get('artist_options')
    print(selectValue2)
    return selectValue2

artist_options = [0, 1, 2]

def saturday_date(date_search):
    date_search = date_search.split('-')
    new_date = date(int(date_search[0]), int(date_search[1]), int(date_search[2]))
    new_date_weekday = new_date.weekday()
    my_saturday_change = new_date_weekday - 5
    my_sat_delta = my_saturday_change + 7
    if my_sat_delta == 7:
        date_search = str(new_date)
    else:
        this_saturday = new_date - timedelta(days=my_sat_delta)
        date_search = str(this_saturday)
    return date_search

@app.route('/song/', methods=['POST'])
def type_search():
    search_option = dropdown()
    song_artist = request.form['song_artist']
    date_search = request.form['date_search']
    rank_search = request.form['rank_search']
    print(song_artist)
    print(date_search)
    print(rank_search)
    if date_search == True:
        print(date_search)
        date_input = saturday_date(date_search)
        print(date_input)
    # norp_option = dropdown2()
    else:
        return
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
        return render_template('song.html', song_artist=song_artist, search_option=search_option,
                               artist_options=artist_options, charts=data, date_search=date_search,
                               rank_search=rank_search, date_input=date_input)

    # return redirect(url_for('result', name=song_name))

@app.route('/artist/', methods=['POST'])
def artist_search():
    artist_option = artist_dropdown()
    song_artist = request.form['song_artist']
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
    return render_template('artist.html', song_artist=song_artist, artist_option=artist_option, charts=data)

# @app.route('/song/', methods=['POST'])
# def song_search():
#     date_search = request.form['date_search']
#     rank_search = request.form['rank_search']
#     with open('charts.csv', 'r') as file:
#         charts = csv.reader(file)
#         data = list(charts)
#     return render_template('song.html', date_search=date_search, rank_search=rank_search, charts=data)

if __name__ == '__main__':
    app.run(debug=True)









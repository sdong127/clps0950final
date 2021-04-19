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

@app.route('/song/', methods=['POST'])
def type_search():
    search_option = dropdown()
    song_artist = request.form['song_artist']
    print(song_artist)
    # norp_option = dropdown2()
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
        return render_template('song.html', song_artist=song_artist, search_option=search_option, artist_options=artist_options, charts=data)

    # return redirect(url_for('result', name=song_name))

@app.route('/artist/', methods=['POST'])
def artist_search():
    artist_option = artist_dropdown()
    song_artist = request.form['song_artist']
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
    return render_template('artist.html', song_artist=song_artist, artist_option=artist_option, charts=data)

# @app.route('/date/', methods=['POST'])
# def song_search():
#     with open('charts.csv', 'r') as file:
#         charts = csv.reader(file)
#         data = list(charts)
#     return render_template

if __name__ == '__main__':
    app.run(debug=True)









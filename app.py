from flask import Flask,render_template, request, redirect, url_for
import spacy
import pandas as pd
import numpy as np
from contractions import CONTRACTION_MAP
import re
import csv

app = Flask(__name__)
options = [0, 1, 2]
norp = ['None', 'Naive', 'Partial']

@app.route('/', methods=['GET'])
def homepage():
    print('hello')
    return render_template('homepage.html', options=options, norp=norp)


def dropdown():
    selectValue = request.form.get('options')
    print(selectValue)
    return selectValue

def dropdown2():
    selectValue2 = request.form.get('norp')
    print(selectValue2)
    return selectValue2

@app.route('/song/', methods=['POST'])
def type_search():
    search_option = dropdown()
    song_name = request.form['song_artist']
    print(song_name)
    norp_option = dropdown2()
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
        return render_template('song.html', norp_option=norp_option, song_name=song_name, search_option=search_option, charts=data)

    # return redirect(url_for('result', name=song_name))

# @app.route('/song/', methods=['POST'])
# def n_or_p():
#     norp_option = dropdown2()
#     print('hi again')
#     with open('charts.csv', 'r') as file:
#         charts = csv.reader(file)
#         data = list(charts)
#         return render_template('song.html', norp_option=norp_option, charts=data)

    # song_name = request.form['nm']
    # return redirect(url_for('result', name=song_name))

if __name__ == '__main__':
    app.run(debug=True)









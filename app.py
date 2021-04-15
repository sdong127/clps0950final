from flask import Flask,render_template, request, redirect, url_for
import csv
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
import spacy
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from bs4 import BeautifulSoup
from contractions import CONTRACTION_MAP
import re
from collections import Counter



app = Flask(__name__)
options = [0, 1, 2, 3]
norp = ['None', 'Naive', 'Partial']

@app.route('/', methods=['GET'])
def homepage():
    print('hello')
    return render_template('homepage.html', options=options, norp=norp)


def dropdown():
    selectValue = request.form.get('options')
    print(selectValue)
    return selectValue

@app.route('/song/', methods=['POST'])
def search():
    search_option = dropdown()
    print('hi')
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
        return render_template('song.html', search_option=search_option, charts=data)


if __name__ == '__main__':
    app.run(debug=True)









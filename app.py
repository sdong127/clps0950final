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


@app.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html', options=options, norp=norp)

options = ['1', '2', '3']
norp = ['Naive', 'Partial']

# @app.route('/', methods=['POST'])
# def options():
#     selectValue = request.form.get('options')
#     return redirect(url_for('search'),selectValue=selectValue)
#
#
# @app.route('/search', methods=['GET'])
# def search():
#     search_option = options()
#     with open('charts.csv', 'r') as file:
#         charts = csv.reader(file)
#         data = list(charts)
#         return render_template('song.html', search_option=search_option, charts=data)

if __name__ == '__main__':
    app.run()









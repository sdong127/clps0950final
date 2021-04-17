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

norp = ['None', 'Naive', 'Partial']


## spell checking pieces ##
def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def simple_stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


## all together ##
def normalize_search(search, html_stripping=True, text_lower_case=True, special_char_removal=True, remove_digits=True,
                     fixed=True):
    search_input = search.split()
    normalized_search = []
    # normalize each document in the corpus
    for word in search_input:
        # strip HTML
        if html_stripping:
            word = strip_html_tags(word)
        if text_lower_case:
            word = word.lower()
        word = re.sub(r'[\r|\n|\r\n]+', ' ', word)
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            word = special_char_pattern.sub(" \\1 ", word)
            word = remove_special_characters(word, remove_digits=remove_digits)
        word = re.sub(' +', ' ', word)
        if fixed:
            word = correction(word)
        normalized_search = [*normalized_search, word]
    list_to_str = str(' '.join([str(item) for item in normalized_search]))
    return list_to_str


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
    normalize_input = normalize_search(song_name)
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
        return render_template('song.html', normalize_input=normalize_input,norp_option=norp_option, song_name=song_name, search_option=search_option, charts=data)

    # return redirect(url_for('result', name=song_name))

@app.route('/partialsong/', methods=['POST'])
def partial_song_redo():
    clarify = request.form['clarify']
    return render_template('partial_song_redo.html',clarify=clarify)

if __name__ == '__main__':
    app.run(debug=True)









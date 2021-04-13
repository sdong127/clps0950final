from flask import Flask,render_template
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

nlp = spacy.load('en_core_web_sm')

# app = Flask(__name__)
#
#
# @app.route('/', methods=['GET'])
# def homepage():
#     return render_template('homepage.html')
#
#
# if __name__ == '__main__':
#     app.run()


### asking the user to run again ###
def search_again():
    again_input = input('Would you like to search for another song, artist, or date? Type Yes or No: ')
    if again_input == 'Yes':
        intro()
    elif again_input == 'No':
        print('Thank you for using the Billboard Song Search! Have a nice day :)')
    else:
        print('Sorry, didn\'t understand that. Please try again.')
        search_again()

### NAIVE SONG SEARCH ###
def naive_song_search(song_input):
    found = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            if song_input == row[2]:
                print('On ' + row[0] + ' ' + song_input + ' ranked at #' + row[1] + ' on the Billboard Hot 100 Chart.')
                found = True
        if not found:
            print('Sorry, we couldn\'t find your song.')
        search_again()

### PARTIAL SONG SEARCH ###
def partial_song_search(song_input):
    partial_title = song_input.lower().split(' ')
    song_list = []
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            song_title = row[2].lower().split(' ')
            check = all(word in song_title for word in partial_title)
            if check is True:
                song_list.append(row[2])
        song_series = pd.Series(data=song_list)
        unique_series = pd.Series(song_series.unique())
        pd.options.display.max_columns = None
        pd.options.display.max_rows = None
        print(unique_series)
        correction_input = input('Did you mean one of these songs? Type Yes or No: ')
        if correction_input == 'Yes':
            index_input = input('Enter the corresponding number to the song you meant: ')
            actual_song = unique_series[int(index_input)]
            naive_song_search(actual_song)
        else:
            search_again()

### NAIVE ARTIST SEARCH ###
def naive_artist_search(artist_input):
    found = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        choice_input = input('Do you want to see 1. all of this artist\'s song rankings or '
                             '2. just the highest rankings for each unique song? Type 1 or 2: ')
        if choice_input == '1':
            print(artist_input + '\'s songs: ')
            for row in charts:
                if artist_input == row[3]:
                    print('\'' + row[2] + '\'' + ' ranked ' + row[1] + ' on the Billboard Charts on ' + row[0])
                    found = True
            if not found:
                print('Sorry, we couldn\'t find your song.')
        elif choice_input == '2':
            print(artist_input + '\'s songs: ')
            song_dict = {}
            for row in charts:
                if artist_input == row[3]:
                    if row[2] in song_dict.keys():
                        song_dict[row[2]][0].append(row[1])
                        song_dict[row[2]][1].append(row[0])
                        found = True
                    else:
                        song_dict[row[2]] = ([row[1]], [row[0]])
                        found = True
            if not found:
                return ('Sorry, we couldn\'t find your song.')

            for key in song_dict:
                ranks = []
                indices = []
                for index, rank in enumerate(song_dict[key][0]):
                    ranks.append(rank)
                    indices.append(index)
                top_rank = min(ranks)
                top_date_index = ranks.index(min(ranks))
                (top_rank, rank_date) = (top_rank, song_dict[key][1][top_date_index])
                print('\'' + key + '\'' + ' ranked ' + top_rank + ' on the Billboard Charts on ' + rank_date)
        search_again()

### PARTIAL ARTIST SEARCH ###
def partial_artist_search(artist_input):
    partial_name = artist_input.lower().split(' ')
    artist_list = []
    lakshmi = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            artist_name = row[3].lower().split(' ')
            # print(artist_name)
            check = all(word in artist_name for word in partial_name) ## error here with boolean
            if check is True:
                artist_list.append(row[3])
                lakshmi = True
                # print(artist_list)
        if not lakshmi:
            print('sorry')
            return
        artist_series = pd.Series(data=artist_list)
        unique_series = pd.Series(artist_series.unique())
        pd.options.display.max_rows = None
        pd.options.display.max_columns = None
        print(unique_series)
        correction_input = input('Did you mean one of these artists? Type Yes or No: ')
        if correction_input == 'Yes':
            index_input = input('Enter the corresponding number to the artist you meant: ')
            actual_artist = unique_series[int(index_input)]
            naive_artist_search(actual_artist)
        else:
            list_to_str = normalize_search(artist_input)
            # if list_to_str == artist_input:
            #     print('you spelled it right')
            # else:
                clarify = input('Did you mean ' + list_to_str + '? Enter Yes/No')
                if clarify == 'Yes':
                    partial_artist_search(list_to_str)
                else:
                    print('Sorry, we didn\'t recognize your search. Please try again!')
            search_again()



### searching by date ###
def date_search(date_input): # YYYY-MM-DD
    found = False
    date_input = date_input.split('-')
    # print(date_input)
    new_date = date(int(date_input[0]), int(date_input[1]), int(date_input[2]))
    # print(new_date)
    new_date2 = new_date.weekday()
    # print(new_date2)
    my_saturday_change = new_date2 - 5
    # print(my_saturday_change)
    my_sat_delta = my_saturday_change + 7
    # print(my_sat_delta)
    date_input_old = new_date - timedelta(days=my_sat_delta)
    date_input = str(date_input_old)
    # print(date_input)
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        print('Would you like to search for?\n'
                '1. all songs that ranked that week or\n'
                '2. the #1 song at this date or\n'
                '3. the song at a specific rank\n')
        all_or_rank = input('Enter the corresponding number to the option you want: ')
        if all_or_rank == '1':
            for row in charts:
                if date_input == row[0]:
                    print(row[2] + ' by ' + row[3] + ' was ranked ' + '#' + row[1] + '.')
                    found = True
            if not found:
                print('Sorry, we couldn\'t find your song.')
            search_again()
        elif all_or_rank == '2':
            for row in charts:
                if date_input == row[0]:
                    if row[1] == '1':
                        print(row[2] + ' by ' + row[3] + ' was ranked #1.')
                        found = True
            if not found:
                print('Sorry, we couldn\'t find your song.')
            search_again()
        elif all_or_rank == '3':
            rank_input = input('What rank from this day would you like to see? Enter a number 1-100: ')
            for row in charts:
                if date_input == row[0]:
                    if row[1] == rank_input:
                        print(row[2] + ' by ' + row[3] + ' was ranked #' + rank_input)
                        found = True
            if not found:
                print('Sorry, we couldn\'t find your song.')
            search_again()

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
def normalize_search(search, html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=True, fixed=True):
    search_input = search.split()
    print(search_input)
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
            # print(word)
        normalized_search = [*normalized_search, word]
    list_to_str = str(' '.join([str(item) for item in normalized_search]))
    # print(type(list_to_str))
    return list_to_str

## starting the search ##

def intro():
    print('Welcome to the Billboard Song Search by team HASH!\n'
          'You have access to weekly Billboard charts starting from August 4th, 1958, to March 13th, 2021.')
    print('What would you like to search?\n'
          '1. Search by song: the ranks achieved by a certain song on the Billboard charts\n' #song_search
          '2. Search by date: what song achieved what rank on a specific day\n' #time_search not done yet
          '3. Search by artist: songs by a certain artist that made the charts and when') #artist_search not done yet
    type_input = input('Enter 1, 2, or 3')
    if type_input == '1':
        search_input = input('What type of search would you like to do?\n'
                             'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                             'A partial search is one in which you can search any keywords, case insensitive.\n'
                             'Type Naive or Partial to get started: ')
        if search_input == 'Naive':
            song_input = input('Enter a song name: ')
            naive_song_search(song_input)
        elif search_input == 'Partial':
            song_input = input('Enter a song name: ')
            list_to_str = normalize_search(song_input)
            if list_to_str == song_input:
                partial_song_search(song_input)
            else:
                clarify = input('Did you mean ' + list_to_str + '? Enter Yes/No')
                if clarify == 'Yes':
                    partial_song_search(list_to_str)
                else:
                    print('Sorry, we didn\'t recognize your search. Please try again!')
                    intro()
        else:
            print('Please try again.')
            search_input = input('What type of search would you like to do?\n'
                                 'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                                 'A partial search is one in which you can search any keywords, case insensitive.\n'
                                 'Type Naive or Partial to get started: ')
    elif type_input == '2':
        date_input = input(
            'What Saturday are you interested in finding songs? Please enter it in the format YYYY-MM-DD: ')
        date_search(date_input)

        #search by date functions
    elif type_input == '3': #search by artist
        search_input = input('What type of search would you like to do?\n'
                             'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                             'A partial search is one in which you can search any keywords, case insensitive.\n'
                             'Type Naive or Partial to get started: ')
        if search_input == 'Naive':
            artist_input = input('Enter an artist name: ')
            naive_artist_search(artist_input)
        elif search_input == 'Partial':
            artist_input = input('Enter an artist name: ')
            partial_artist_search(artist_input)
    else:
        print('Please try again.')
        intro()

intro()








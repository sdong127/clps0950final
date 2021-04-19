import csv
import pandas as pd
from datetime import date
from datetime import timedelta
import re
from bs4 import BeautifulSoup
import nltk
from collections import Counter
import sys


################################ SPELL CHECKER ################################


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



################################ SEARCH FUNCTIONALITY ################################


### asking the user to search again ###
def search_again():
    again_input = input('Would you like to search for another song, artist, or date? Enter Yes or No: ')
    if again_input == 'Yes' or again_input == 'yes':
        return intro()
    elif again_input == 'No' or again_input == 'no':
        print('Thank you for using the Billboard Song Search! Have a nice day :)')
        sys.exit()
    else:
        print('Sorry, we didn\'t understand that. Please try again.')
        return search_again()

### NAIVE SONG SEARCH ###
def naive_song_search(song_input):
    found_naive_song = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            if song_input == row[2]:
                print('On ' + row[0] + ' ' + song_input + ' ranked at #' + row[1] + ' on the Billboard Hot 100 Chart.')
                found_naive_song = True
        if not found_naive_song:
            print('Sorry, we couldn\'t find your song.')
    return search_again()


partial_song_counter = 0
### PARTIAL SONG SEARCH ###
def partial_song_search(song_input):
    partial_title = song_input.lower().split(' ')
    song_list = []
    found_partial_song = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            song_title = row[2].lower().split(' ')
            check = all(word in song_title for word in partial_title)
            if check is True:
                song_list.append(row[2])
                found_partial_song = True
        global partial_song_counter
        if not found_partial_song and partial_song_counter == 0:
            normalize_song = normalize_search(song_input)
            clarify = input('Did you mean ' + '\'' + normalize_song + '\'' + '? Enter Yes or No: ')
            if clarify == 'Yes' or clarify == 'yes':
                partial_song_counter+=1
                return partial_song_search(normalize_song)
            elif clarify == 'No' or clarify == 'no':
                print('Sorry, we couldn\'t find your song. Please try again.')
                return search_again()
            else:
                print('Sorry, we didn\'t recognize that. Please try again.')
                return search_again()
        song_series = pd.Series(data=song_list)
        unique_series = pd.Series(song_series.unique())
        pd.options.display.max_columns = None
        pd.options.display.max_rows = None
        print(unique_series)
        if not unique_series.empty:
            correction_input = input('Did you mean one of these songs? Enter Yes or No: ')
            if correction_input == 'Yes' or correction_input == 'yes':
                index_input = input('Enter the corresponding number to the song you meant: ')
                actual_song = unique_series[int(index_input)]
                return naive_song_search(actual_song)
            elif correction_input == 'No' or correction_input == 'no':
                print('Sorry, we couldn\'t find your song. Please try again.')
            else:
                print('Sorry, we didn\'t understand that. Please try again.')
        else:
            print('Sorry, we couldn\'t find your song. Please try again.')
    partial_song_counter = 0
    return search_again()

### NAIVE ARTIST SEARCH ###
def naive_artist_search(artist_input):
    found_naive_artist = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            if artist_input == row[3]:
                found_naive_artist = True
        file.close()
    if not found_naive_artist:
        print('Sorry, we couldn\'t find your artist. Please try again.')
        return search_again()
    choice_input = input('Do you want to see \n1. all of this artist\'s song rankings or \n'
                             '2. just the highest rankings for each unique song? \nType 1 or 2: ')
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        if choice_input == '1':
            print(artist_input + '\'s songs: ')
            for row in charts:
                if artist_input == row[3]:
                    print('\'' + row[2] + '\'' + ' ranked ' + row[1] + ' on the Billboard Charts on ' + row[0])
        elif choice_input == '2':
            song_dict = {}
            for row in charts:
                if artist_input == row[3]:
                    if row[2] in song_dict.keys():
                        song_dict[row[2]][0].append(row[1])
                        song_dict[row[2]][1].append(row[0])
                    else:
                        song_dict[row[2]] = ([row[1]], [row[0]])
            print(artist_input + '\'s songs: ')
            for key in song_dict:
                ranks = []
                indices = []
                for index, rank in enumerate(song_dict[key][0]):
                    ranks.append(rank)
                    indices.append(index)
                top_rank = min(ranks)
                top_date_index = ranks.index(min(ranks))
                (top_rank, rank_date) = (top_rank, song_dict[key][1][top_date_index])
                print('\'' + key + '\'' + ' ranked ' + top_rank + ' on the Billboard Charts on ' + rank_date + '.')
        else:
            print('Sorry, we didn\'t understand that. Please try again.')
    return search_again()


partial_artist_counter = 0
### PARTIAL ARTIST SEARCH ###
def partial_artist_search(artist_input):
    partial_name = artist_input.lower().split(' ')
    artist_list = []
    found_partial_artist = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            artist_name = row[3].lower().split(' ')
            # print(artist_name)
            check = all(word in artist_name for word in partial_name)
            if check is True:
                artist_list.append(row[3])
                found_partial_artist = True
        global partial_artist_counter
        if not found_partial_artist and partial_artist_counter == 0:
            normalize_artist = normalize_search(artist_input)
            clarify = input('Did you mean ' + '\'' + normalize_artist + '\'' + '? Enter Yes or No: ')
            if clarify == 'Yes' or clarify == 'yes':
                partial_artist_counter+=1
                partial_artist_search(normalize_artist)
            elif clarify == 'No' or clarify == 'no':
                print('Sorry, we couldn\'t find your artist. Please try again.')
                return search_again()
            else:
                print('Sorry, we didn\'t recognize that. Please try again.')
                return search_again()
        artist_series = pd.Series(data=artist_list)
        unique_series = pd.Series(artist_series.unique())
        pd.options.display.max_rows = None
        pd.options.display.max_columns = None
        print(unique_series)
        if not unique_series.empty:
            correction_input = input('Did you mean one of these artists? Enter Yes or No: ')
            if correction_input == 'Yes' or correction_input == 'yes':
                index_input = input('Enter the corresponding number to the artist you meant: ')
                actual_artist = unique_series[int(index_input)]
                return naive_artist_search(actual_artist)
            elif correction_input == 'No' or correction_input == 'no':
                print('Sorry, we couldn\'t find your artist. Please try again.')
                return search_again()
            else:
                print('Sorry, we didn\'t recognize that. Please try again.')
                return search_again()
        else:
            print('Sorry, we couldn\'t find your artist. Please try again.')
            return search_again()
    partial_artist_counter = 0



### DATE SEARCH ###
def date_search(date_input): # YYYY-MM-DD
    found_date = False
    date_input = date_input.split('-')
    # print(date_input)
    new_date = date(int(date_input[0]), int(date_input[1]), int(date_input[2]))
    # print(new_date)
    new_date_weekday = new_date.weekday()
    # print(new_date_weekday)
    my_saturday_change = new_date_weekday - 5
    # print(my_saturday_change)
    my_sat_delta = my_saturday_change + 7
    # print(my_sat_delta)
    if my_sat_delta == 7:
        date_input = str(new_date)
    elif my_sat_delta == 8:
        this_saturday = new_date - timedelta(days=my_saturday_change)
        date_input = str(this_saturday)
    else:
        this_saturday = new_date - timedelta(days=my_sat_delta)
        date_input = str(this_saturday)
    #print(new_date_input)
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            if date_input == row[0]:
                found_date = True
        file.close()
    if not found_date:
        print('Sorry, we couldn\'t find the chart for the date you inputted. '
              'You have access to weekly Billboard charts starting from January 6th, 1962, to April 10th, 2021. '
              'Please try again.')
        return search_again()

    print('Would you like to search for:\n'
          '1. all the songs that ranked this week or\n'
          '2. the #1 song during this week or\n'
          '3. what song was at a specific rank this week (you will input the rank you are interested in)\n')
    all_or_rank = input('Enter the corresponding number to the option you want: ')

    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        if all_or_rank == '1':
            for row in charts:
                if date_input == row[0]:
                    print(row[2] + ' by ' + row[3] + ' was ranked ' + '#' + row[1] + '.')
        elif all_or_rank == '2':
            for row in charts:
                if date_input == row[0]:
                    if row[1] == '1':
                        print(row[2] + ' by ' + row[3] + ' was ranked #1.')
        elif all_or_rank == '3':
            rank_input = input('What rank from this day would you like to see? Enter a number 1-100: ')
            for row in charts:
                if date_input == row[0]:
                    if row[1] == rank_input:
                        print(row[2] + ' by ' + row[3] + ' was ranked #' + rank_input + '.')
        else:
            print('Sorry, we didn\'t understand that. Please try again.')
    return search_again()


## starting the search ##

def intro():
    print('Welcome to the Billboard Song Search by team HASH!\n'
          'You have access to weekly Billboard charts starting from January 6th, 1962, to April 10th, 2021.')
    print('What would you like to search?\n'
          '1. Search by song: the ranks achieved by a certain song on the Billboard charts\n'
          '2. Search by date: the song data of the chart at a certain week\n'
          '3. Search by artist: songs by a certain artist that made the charts and when')
    type_input = input('Enter 1, 2, or 3: ')
    if type_input == '1':
        search_input = input('What type of search would you like to do?\n'
                             'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                             'A partial search is one in which you can search any keywords, case insensitive.\n'
                             'Type Naive or Partial to get started: ')
        if search_input == 'Naive' or search_input == 'naive':
            song_input = input('Enter a song name: ')
            return naive_song_search(song_input)
        elif search_input == 'Partial' or search_input == 'partial':
            song_input = input('Enter a song name: ')
            return partial_song_search(song_input)
        else:
            print('Sorry, we didn\'t understand that. Please try again.')
            return intro()
    elif type_input == '2':
        date_input = input('What date would you like to search?\n'
                           'You have access to weekly Billboard charts starting from January 6th, 1962, to April 10th, 2021.\n'
                           'Please enter the date in the format YYYY-MM-DD: ')
        return date_search(date_input)
        #search by date functions
    elif type_input == '3': #search by artist
        search_input = input('What type of search would you like to do?\n'
                             'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                             'A partial search is one in which you can search any keywords, case insensitive.\n'
                             'Type Naive or Partial to get started: ')
        if search_input == 'Naive' or search_input == 'naive':
            artist_input = input('Enter an artist name: ')
            return naive_artist_search(artist_input)
        elif search_input == 'Partial' or search_input == 'partial':
            artist_input = input('Enter an artist name: ')
            return partial_artist_search(artist_input)
        else:
            print('Sorry, we didn\'t understand that. Please try again.')
            return intro()
    else:
        print('Sorry, we didn\'t understand that. Please try again.')
        return intro()

intro()

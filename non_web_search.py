import csv
import pandas as pd
from datetime import date, timedelta
import re
from bs4 import BeautifulSoup
from collections import Counter
import sys


################################ SPELL CHECKER ################################


### functions for normalizing search queries from DJ Sarkar ###

def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

def words(text): return re.findall(r'\w+', text.lower())



### spell checker pieces from Peter Norvig ###

WORDS = Counter(words(open('big.txt').read()))
# 'dictionary' of words to refer to

def P(word, N=sum(WORDS.values())):
# probablity of input word
    return WORDS[word] / N

def correction(word):
# most probable spelling correction for input word
    return max(candidates(word), key=P)

def candidates(word):
# generates possible spelling corrections for input word
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
# returns the subset of words that appear in the dictionary of WORDS
    return set(w for w in words if w in WORDS)

def edits1(word):
# all edits that are one edit away from input word
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
# all edits that are two edits away from input word
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))



### using all the normalizing and spell checking functions together ###
def normalize_search(search, html_stripping=True, text_lower_case=True, special_char_removal=True, remove_digits=True,
                     fixed=True):
# normalizes and spell checks seach input

    # split search_input into a list of words
    search_input = search.split()
    # initiate list of normalized words
    normalized_search = []

    # normalize each word in search_input
    for word in search_input:
        # strip HTML
        if html_stripping:
            word = strip_html_tags(word)
        # change letters to lower case
        if text_lower_case:
            word = word.lower()
        word = re.sub(r'[\r|\n|\r\n]+', ' ', word)
        # remove special characters
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            word = special_char_pattern.sub(" \\1 ", word)
            word = remove_special_characters(word, remove_digits=remove_digits)
        word = re.sub(' +', ' ', word)
        # spell check the word
        if fixed:
            word = correction(word)

        # add each corrected word to normalized_search list
        normalized_search = [*normalized_search, word]
    # convert normalized_search into a string
    list_to_str = str(' '.join([str(item) for item in normalized_search]))
    return list_to_str



################################ SEARCH FUNCTIONALITY ################################


def search_again():
# asking the user to search again
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
# searches for song_input in charts exactly as it was inputted
    found_naive_song = False

    # open csv file with charts data
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)

        # loop through each row of the charts
        for row in charts:
            # check if song_input is in the row
            if song_input == row[2]:
                print('On ' + row[0] + ' ' + song_input + ' by ' + row[3] + ' ranked at #' + row[1] + ' on the Billboard Hot 100 Chart.')
                found_naive_song = True

        if not found_naive_song:
            print('Sorry, we couldn\'t find your song.')

    # allow user to search again
    return search_again()



### PARTIAL SONG SEARCH ###

# initiate global variable for counting number of times partial_song_search has run
partial_song_counter = 0

def partial_song_search(song_input):
# normalizes and spell checks song_input, then checks if song_input or part of song_input is in the charts

    # split song_input into list of words
    partial_title = song_input.lower().split(' ')
    # initialize possible list of songs
    song_list = []
    found_partial_song = False

    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)

        for row in charts:
            # split song in row into list of words
            song_title = row[2].lower().split(' ')
            # check if all the words in partial_title are in song_title
            check = all(word in song_title for word in partial_title)
            if check is True:
                # append song in row to song_list
                song_list.append(row[2])
                found_partial_song = True

        # call global variable partial_song_counter
        global partial_song_counter
        # make sure song input is not already in charts and user has not already searched the same input
        if not found_partial_song and partial_song_counter == 0:
            # normalize song_input
            normalize_song = normalize_search(song_input)

            clarify = input('Did you mean ' + '\'' + normalize_song + '\'' + '? Enter Yes or No: ')
            if clarify == 'Yes' or clarify == 'yes':
                # add 1 to partial_song_counter if user has already clarified their input
                partial_song_counter+=1
                # call partial_song_search again
                return partial_song_search(normalize_song)
            elif clarify == 'No' or clarify == 'no':
                print('Sorry, we couldn\'t find your song. Please try again.')
                return search_again()
            else:
                print('Sorry, we didn\'t recognize that. Please try again.')
                return search_again()

        # convert song_list into series
        song_series = pd.Series(data=song_list)
        # sort out just the unique songs
        unique_series = pd.Series(song_series.unique())
        # display all columns and rows in console
        pd.options.display.max_columns = None
        pd.options.display.max_rows = None
        print(unique_series)

        if not unique_series.empty:
            correction_input = input('Did you mean one of these songs? Enter Yes or No: ')
            if correction_input == 'Yes' or correction_input == 'yes':
                index_input = input('Enter the corresponding number to the song you meant: ')
                # find the song the user meant by having them input the index of the corresponding song in unique_series
                actual_song = unique_series[int(index_input)]
                # set partial_song_counter to 0 again in case user searches again
                partial_song_counter = 0
                # do a naive search on actual_song
                return naive_song_search(actual_song)
            elif correction_input == 'No' or correction_input == 'no':
                print('Sorry, we couldn\'t find your song. Please try again.')
            else:
                print('Sorry, we didn\'t understand that. Please try again.')
        else:
            print('Sorry, we couldn\'t find your song. Please try again.')

    # set partial_song_counter to 0 again in case user searches again
    partial_song_counter = 0
    return search_again()



### NAIVE ARTIST SEARCH ###
def naive_artist_search(artist_input):
# searches for artist_input in charts exactly as it was inputted
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
                    # print all of the artist's song rankings everytime they show up in the charts
                    print('\'' + row[2] + '\'' + ' ranked ' + row[1] + ' on the Billboard Charts on ' + row[0])
        elif choice_input == '2':
            # initiate dictionary to hold unique songs
            song_dict = {}
            for row in charts:
                if artist_input == row[3]:
                    # if song in row already exists in song_dict, append its rank and date to the key's tuple of lists
                    if row[2] in song_dict.keys():
                        song_dict[row[2]][0].append(row[1])
                        song_dict[row[2]][1].append(row[0])
                    else:
                        # if song doesn't already exist in song_dict, add it as a key and append its rank and date as a tuple of lists
                        song_dict[row[2]] = ([row[1]], [row[0]])

            print(artist_input + '\'s songs: ')
            # loop through songs in song_dict
            for key in song_dict:
                # initiate list of ranks
                ranks = []
                # initiate list of indices for list of ranks
                indices = []

                # loop through song_dict keys' ranks
                for index, rank in enumerate(song_dict[key][0]):
                    ranks.append(rank)
                    indices.append(index)
                # get top rank for the song

                top_rank = min(ranks)
                # get the index of the top rank in ranks list
                top_date_index = ranks.index(min(ranks))
                # create tuple for top rank and that rank's date
                (top_rank, rank_date) = (top_rank, song_dict[key][1][top_date_index])

                # print all artist's top ranking unique songs
                print('\'' + key + '\'' + ' ranked #' + top_rank + ' on the Billboard Charts on ' + rank_date + '.')
        else:
            print('Sorry, we didn\'t understand that. Please try again.')
    return search_again()



### PARTIAL ARTIST SEARCH ###

# initialize global variable for counting number of times partial_artist_search has run
partial_artist_counter = 0

def partial_artist_search(artist_input):
# normalizes and spell checks artist_input, then checks if artist_input or part of artist_input is in the charts

    # split artist_input into a list of words
    partial_name = artist_input.lower().split(' ')
    # initalize possible list of artists
    artist_list = []
    found_partial_artist = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            # split artist name in row into list of words
            artist_name = row[3].lower().split(' ')
            # check if all words in partial_name are in artist_name
            check = all(word in artist_name for word in partial_name)
            if check is True:
                # add artist name to artist_list
                artist_list.append(row[3])
                found_partial_artist = True

        # call global variable partial_artist_counter
        global partial_artist_counter
        # print(found_partial_artist)
        # print(partial_artist_counter)

        # make sure artist input was not already in charts and user has not already searched the same input
        if not found_partial_artist and partial_artist_counter == 0:
            # normalize artist_input
            normalize_artist = normalize_search(artist_input)

            clarify = input('Did you mean ' + '\'' + normalize_artist + '\'' + '? Enter Yes or No: ')
            if clarify == 'Yes' or clarify == 'yes':
                # add 1 to partial_artist_counter if user has already clarified their input
                partial_artist_counter+=1
                # call partial_artist_search again on normalize_artist
                partial_artist_search(normalize_artist)
            elif clarify == 'No' or clarify == 'no':
                print('Sorry, we couldn\'t find your artist. Please try again.')
                return search_again()
            else:
                print('Sorry, we didn\'t recognize that. Please try again.')
                return search_again()

        # create series for artist_list
        artist_series = pd.Series(data=artist_list)
        # get unique artist names only
        unique_series = pd.Series(artist_series.unique())
        # display all rows and columns in console
        pd.options.display.max_rows = None
        pd.options.display.max_columns = None
        print(unique_series)

        if not unique_series.empty:
            correction_input = input('Did you mean one of these artists? Enter Yes or No: ')
            if correction_input == 'Yes' or correction_input == 'yes':
                index_input = input('Enter the corresponding number to the artist you meant: ')
                # get the artist the user meant using the index corresponding to the correct artist
                actual_artist = unique_series[int(index_input)]
                # set partial_artist_counter to 0 again in case user searches again
                partial_artist_counter = 0
                # do a naive search on actual_artist
                return naive_artist_search(actual_artist)
            elif correction_input == 'No' or correction_input == 'no':
                print('Sorry, we couldn\'t find your artist. Please try again.')
            else:
                print('Sorry, we didn\'t recognize that. Please try again.')
        else:
            print('Sorry, we couldn\'t find your artist. Please try again.')

    # set partial_artist_counter to 0 again in case user searches again
    partial_artist_counter = 0
    return search_again()



### DATE SEARCH ###
def date_search(date_input):
# takes in date in format YYYY-MM-DD

    # split date_input to list of [YYYY,MM,DD]
    date_input = date_input.split('-')
    # convert date_input into date object
    new_date = date(int(date_input[0]), int(date_input[1]), int(date_input[2]))
    # find the weekday of new_date
    new_date_weekday = new_date.weekday()
    # find how far new_date_weekday is from saturday (hot 100 chart is published every saturday)
    my_saturday_change = new_date_weekday - 5
    # add 7 to my_sat_delta to find how many days we need to subtract from date_input
    my_sat_delta = my_saturday_change + 7

    # check if date_input is on a saturday
    if my_sat_delta == 7:
        date_input = str(new_date)
    # check if date_input is on a sunday
    elif my_sat_delta == 8:
        # find the saturday of the week of date_input
        this_saturday = new_date - timedelta(days=my_saturday_change)
        date_input = str(this_saturday)
    else:
        # find the saturday of the week of date_input
        this_saturday = new_date - timedelta(days=my_sat_delta)
        date_input = str(this_saturday)

    found_date = False
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            # check if date_input exists in row
            if date_input == row[0]:
                found_date = True
        file.close()
    if not found_date:
        print('Sorry, we couldn\'t find the chart for the date you inputted.\n'
              'You have access to weekly Billboard charts starting from January 6th, 1962, to April 10th, 2021.\n'
              'Please try again.')
        return search_again()

    # ask user what they want to see from the date they inputted
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
                    # print all the songs on the chart for this week
                    print(row[2] + ' by ' + row[3] + ' was ranked ' + '#' + row[1] + '.')
        elif all_or_rank == '2':
            for row in charts:
                if date_input == row[0]:
                    if row[1] == '1':
                        # print only the song that ranked #1
                        print(row[2] + ' by ' + row[3] + ' was ranked #1.')
        elif all_or_rank == '3':
            found_rank = False
            rank_input = input('What rank from this day would you like to see? Enter a number 1-100: ')
            for row in charts:
                if date_input == row[0]:
                    # find the rank in the chart
                    if row[1] == rank_input:
                        print(row[2] + ' by ' + row[3] + ' was ranked #' + rank_input + '.')
                        found_rank = True
            if not found_rank:
                print('Sorry, we didn\'t understand that. Please try again.')
                return search_again()
        else:
            print('Sorry, we didn\'t understand that. Please try again.')
    return search_again()




def intro():
# starting the search
    print('Welcome to the Billboard Song Search by team HASH!\n'
          'You have access to weekly Billboard charts starting from January 6th, 1962, to April 10th, 2021.')
    print('What would you like to search?\n'
          '1. Search by song: the ranks achieved by a certain song on the Billboard charts\n'
          '2. Search by date: the song data of the chart at a certain week\n'
          '3. Search by artist: songs by a certain artist that made the charts and when')
    type_input = input('Enter 1, 2, or 3: ')

    # search by song
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

    # search by date
    elif type_input == '2':
        date_input = input('What date would you like to search?\n'
                           'You have access to weekly Billboard charts starting from January 6th, 1962, to April 10th, 2021.\n'
                           'Please enter the date in the format YYYY-MM-DD: ')
        return date_search(date_input)

    # search by artist
    elif type_input == '3':
        search_input = input('What type of search would you like to do?\n'
                             'A naive search is one in which you have to search the exact name with the correct capitalization.\n'
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

# run the non web search!
intro()

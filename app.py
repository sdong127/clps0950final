from flask import Flask
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'


# if __name__ == '__main__':
#     app.run()

#name = input("Enter your name:")
#print("Hello", name + "!")


# my_data = open('charts.csv','r')
# charts = my_data.read()
#
# print(charts)



### NAIVE SONG SEARCH ###
def naive_song_search(song_input):
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            if song_input == row[2]:
                print('On ' + row[0] + ' ' + song_input + ' ranked at #' + row[1] + ' on the Billboard Hot 100 Chart.')
                again_input = input('Would you like to search for another song? Type Yes or No: ')
                if again_input == 'Yes':
                    intro()
                else:
                    print('Thank you for using the Billboard Song Search! Have a nice day :)')
            else:
                again_input = input('Sorry, we couldn\'t find that song. Would you like to try again? Type Yes or No: ')
                if again_input == 'Yes':
                    intro()
                else:
                    print('Thank you for using the Billboard Song Search! Have a nice day :)')

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
            fail_input = input('Sorry, want to try again? Type Yes or No: ')
            if fail_input == 'Yes':
                intro()
            else:
                print('Thank you for using the Billboard Song Search! Have a nice day :)')

### NAIVE ARTIST SEARCH ###
def naive_artist_search(artist_input):
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        print(artist_input + '\'s songs: ')
        for row in charts:
            if artist_input == row[3]:
                print('\'' + row[2] + '\'' + ' ranked ' + row[1] + ' on the Billboard Charts on ' + row[0])

### PARTIAL ARTIST SEARCH ###
def partial_artist_search(artist_input):
    partial_name = artist_input.lower().split(' ')
    artist_list = []
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            artist_name = row[3].lower().split(' ')
            check = all(word in artist_name for word in partial_name)
            if check is True:
                artist_list.append(row[3])
        artist_series = pd.Series(data=artist_list)
        unique_series = pd.Series(artist_series.unique())
        pd.options.display.max_rows = None
        pd.options.display.max_columns = None
        print(unique_series)
        correction_input = input('Did you mean one of these artists? Type Yes or No: ')
        if correction_input == 'Yes':
            index_input = input('Enter the corresponding number to the artist you meant: ')
            actual_song = unique_series[int(index_input)]
            naive_artist_search(actual_song)
        else:
            fail_input = input('Sorry, want to try again? Type Yes or No: ')
            if fail_input == 'Yes':
                intro()
            else:
                print('Thank you for using the Billboard Song Search! Have a nice day :)')


def intro():
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
            partial_song_search(song_input)
        else:
            print('Please try again.')
            search_input = input('What type of search would you like to do?\n'
                                 'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                                 'A partial search is one in which you can search any keywords, case insensitive.\n'
                                 'Type Naive or Partial to get started: ')
    # elif type_input == '2':
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








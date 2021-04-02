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



### NAIVE SEARCH ###


def naive_search(song_input):
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        for row in charts:
            if song_input == row[2]:
                print('On ' + row[0] + ' ' + song_input + ' ranked at #' + row[1] + ' on the Billboard Hot 100 Chart.')

### PARTIAL SEARCH ###
def partial_search(song_input):
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
        print(unique_series)
        correction_input = input('Did you mean one of these songs? Type Yes or No: ')
        if correction_input == 'Yes':
            index_input = input('Enter the corresponding number to the song you meant: ')
            actual_song = unique_series[int(index_input)]
            naive_search(actual_song)
        else:
            fail_input = input('Sorry, want to try again? Type Yes or No: ')
            if fail_input == 'Yes':
                intro()
            else:
                print('Thank you for using the Billboard Song Search! Have a nice day :)')


def intro():
    search_input = input('What type of search would you like to do?\n'
                         'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                         'A partial search is one in which you can search any keywords, case insensitive.\n'
                         'Type Naive or Partial to get started: ')
    if search_input == 'Naive':
        song_input = input('Enter a song name: ')
        naive_search(song_input)
    elif search_input == 'Partial':
        song_input = input('Enter a song name: ')
        partial_search(song_input)
    else:
        print('Please try again.')
        search_input = input('What type of search would you like to do?\n'
                             'A naive search is one in which you have to search the exact title with the correct capitalization.\n'
                             'A partial search is one in which you can search any keywords, case insensitive.\n'
                             'Type Naive or Partial to get started: ')

intro()








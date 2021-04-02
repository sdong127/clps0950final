from flask import Flask
#import csv
import numpy as np

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# if __name__ == '__main__':
#     app.run()

#name = input("Enter your name:")
#print("Hello", name + "!")


# my_data = open('charts.csv','r')
# charts = my_data.read()
#
# print(charts)



import csv

song_input = input('Enter a song name: ')

with open('charts.csv', 'r') as file:
    charts = csv.reader(file)
    for row in charts:
        if song_input == row[2]:
            print('On ' + row[0] + ' ' + song_input + ' ranked at #' + row[1] + ' on the Billboard Hot 100 Chart.')


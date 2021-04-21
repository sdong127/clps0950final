from flask import Flask, render_template, request
import csv
from datetime import date, timedelta

################################ FLASK APP ################################


# initialize global variable to hold user input for song/artist
song_artist = ''

# create Flask object
app = Flask(__name__)
# add jinja extension to facilitate code in html
app.jinja_env.add_extension('jinja2.ext.do')

# create options dropdown list
options = [0, 1, 2]


@app.route('/', methods=['GET','POST'])
def homepage():
# render homepage of website
    return render_template('homepage.html', options=options)

def dropdown():
# store user's homepage dropdown selection for song/artist search
    selectValue = request.form.get('options')
    return selectValue

# create artist_options dropdown list
artist_options = [0, 1, 2]

def artist_dropdown():
# store user's dropdown selection for artist search
    selectValue2 = request.form.get('artist_options')
    return selectValue2


def saturday_date(date_input):
# get the saturday of the week of date_input

    # split date_input into list of [YYYY,MM,DD]
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
    return date_input


@app.route('/song/', methods=['POST'])
# homepage routes to new page with url ending /song/
def type_search():
# homepage search function for song/artist/date, renders song.html

    # call global variable song_artist so we can use it in artist_search()
    global song_artist

    # store homepage dropdown value
    search_option = dropdown()
    # get user input for song/artist
    song_artist = request.form['song_artist']
    # get user input for date
    date_search = request.form['date_search']
    # get user input for rank
    rank_search = request.form['rank_search']

    # check if user searched for date
    if date_search:
        # run saturday_date to find saturday of user's input date
        date_input = saturday_date(date_search)
    if not date_search:
        date_input = None

    # open charts file to make data accessible to song.html
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
        return render_template('song.html', song_artist=song_artist, search_option=search_option,
                               artist_options=artist_options, charts=data, date_search=date_search,
                               rank_search=rank_search, date_input=date_input)

@app.route('/artist/', methods=['POST'])
# /song/ page routes to /artist/ page
def artist_search():
# function runs on song page if user searches for artist, renders artist.html
    ## import pdb; pdb.set_trace()

    # store artist_option dropdown value
    artist_option = artist_dropdown()

    # open charts file to make data accessible to artist.html
    with open('charts.csv', 'r') as file:
        charts = csv.reader(file)
        data = list(charts)
    return render_template('artist.html', song_artist=song_artist, artist_option=artist_option, charts=data)


# run Flask app
if __name__ == '__main__':
    app.run(debug=True)









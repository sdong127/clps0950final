from datetime import date
from datetime import timedelta

date_input = input('Enter a date, YYYY-MM-DD: ')
def dateSearch(date_input): #YYYY-MM-DD
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
    my_saturday = new_date - timedelta(days = my_sat_delta)
    print(my_saturday)
    # make date_input into a string
    # use .weekday to figure what day of the week it is
    # give it a number
    # use that number and .deltatime to subtract the date to the last saturday
    # make that our new date_input
dateSearch(date_input)
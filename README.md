### **Team HASH CLPS0950 Final, Brown University: Billboard Song Search by Haley Seo and Shirley Dong**

#### Billboard Song Search is a program that parses through Dhruvil Dave's "Billboard The Hot 100 Songs" dataset, available on Kaggle: [Link](https://www.kaggle.com/dhruvildave/billboard-the-hot-100-songs)
> The dataset contains information about songs that made the weekly top 100 according to Billboard starting from August 4th, 1958. Due to a discrepancy in the data, our program runs based on the dataset starting from 1962. 
#### Our program, Billboard Song Search, gives a user the ability to look through the dataset and find specific pieces of information, such as: 
1. Search by song: the ranks achieved by a certain song on the Billboard charts 
2. Search by date: the song data of the chart at a certain week
3. Search by artist: songs by a certain artist that made the charts and when

#### A naive and partial search are incorporated into the song and artist search functionalities described above, as well as a spell corrector. The date search functionality configures the input date to the most recent Saturday, which is the base day for the dataset. 

#### A website version of our program is available, which was created using Flask.

#### To run the full version of Billboard Song Search, please run non_web_search.py in any Python text reader. If you would like to run a more compact version of our program in a website format, please run app.py. The compact version allows only for naive searches.

---

#### Toolboxes/Add-ons to be downloaded:
- import csv
- import pandas as pd
- from datetime import date, timedelta
- import re
- from bs4 import BeautifulSoup
- from collections import Counter
- import sys
- from flask import Flask, render_template, request

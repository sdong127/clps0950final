# from spellchecker import SpellChecker
#
# spell = SpellChecker()
#
# misspelled = spell.unknown(['somehting', 'is', 'happening', 'here'])
#
# for word in misspelled:
#     print(spell.correction(word))
#     print(spell.candidates(word))
# en_core_web_sm
# # #
# # # python -m spacy download en_core_web_sm

import spacy
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
import re
from bs4 import BeautifulSoup
from contractions import CONTRACTION_MAP
import unicodedata2

nlp = spacy.load('en_core_web_sm')
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)
tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')
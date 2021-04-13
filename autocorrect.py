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
# import unicodedata2

## RUN THIS IF YOU HAVE TROUBLE WITH DOWNLOADING NLTK STOPWORDS DUE TO SSL CERTIFICATE ERROR
# install_certifi.py
#
# sample script to install or update a set of default Root Certificates
# for the ssl module.  Uses the certificates provided by the certifi package:
#       https://pypi.python.org/pypi/certifi
# import os
# import os.path
# import ssl
# import stat
# import subprocess
# import sys
# STAT_0o775 = ( stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
#              | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP
#              | stat.S_IROTH |                stat.S_IXOTH )
# def main():
#     openssl_dir, openssl_cafile = os.path.split(
#         ssl.get_default_verify_paths().openssl_cafile)
#     print(" -- pip install --upgrade certifi")
#     subprocess.check_call([sys.executable,
#         "-E", "-s", "-m", "pip", "install", "--upgrade", "certifi"])
#     import certifi
#     # change working directory to the default SSL directory
#     os.chdir(openssl_dir)
#     relpath_to_certifi_cafile = os.path.relpath(certifi.where())
#     print(" -- removing any existing file or link")
#     try:
#         os.remove(openssl_cafile)
#     except FileNotFoundError:
#         pass
#     print(" -- creating symlink to certifi certificate bundle")
#     os.symlink(relpath_to_certifi_cafile, openssl_cafile)
#     print(" -- setting permissions")
#     os.chmod(openssl_cafile, STAT_0o775)
#     print(" -- update complete")
# if __name__ == '__main__':
#     main()



nlp = spacy.load('en_core_web_sm')
#nlp_vec = spacy.load('en_vecs', parse = True, tag=True, #entity=True)
# tokenizer = ToktokTokenizer()
# stopword_list = nltk.corpus.stopwords.words('english')
# stopword_list.remove('no')
# stopword_list.remove('not')

# removing html tags ##
def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    stripped_text = soup.get_text()
    return stripped_text

# print(strip_html_tags('<html><h2>Some important text</h2></html>'))

## removing accented characters ##

# def remove_accented_chars(text):
#     text = unicodedata2.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
#     return text

# print(remove_accented_chars('Sómě Áccěntěd těxt'))

## expanding out contractions ##
# def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
#     contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
#                                       flags=re.IGNORECASE | re.DOTALL)
#
#     def expand_match(contraction):
#         match = contraction.group(0)
#         first_char = match[0]
#         expanded_contraction = contraction_mapping.get(match) \
#             if contraction_mapping.get(match) \
#             else contraction_mapping.get(match.lower())
#         expanded_contraction = first_char + expanded_contraction[1:]
#         return expanded_contraction
#
#     expanded_text = contractions_pattern.sub(expand_match, text)
#     expanded_text = re.sub("'", "", expanded_text)
#     return expanded_text


# print(expand_contractions("Y'all can't expand contractions I'd think"))

## removing special characters ##

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text

# print(remove_special_characters("Well this was fun! What do you think? 123#@!", remove_digits=True))

## stemming ##

def simple_stemmer(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])
    return text

# print(simple_stemmer("My system keeps crashing his crashed yesterday, ours crashes daily"))

## lemmatization ##
#
# def lemmatize_text(text):
#     text = nlp(text)
#     text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
#     return text

#print(lemmatize_text("My system keeps crashing! his crashed yesterday, ours crashes daily"))

## removing stopwords ##

# def remove_stopwords(text, is_lower_case=False):
#     tokens = tokenizer.tokenize(text)
#     tokens = [token.strip() for token in tokens]
#     if is_lower_case:
#         filtered_tokens = [token for token in tokens if token not in stopword_list]
#     else:
#         filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
#     filtered_text = ' '.join(filtered_tokens)
#     return filtered_text

# print(remove_stopwords("The, and, if are stopwords, computer is not"))

import re
from collections import Counter

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
            # print(word)
        # remove accented characters
        # if accented_char_removal:
        #     word = remove_accented_chars(word)
        # expand contractions
        # if contraction_expansion:
        #     word = expand_contractions(word)
        # lowercase the text
        if text_lower_case:
            word = word.lower()
            # print(word)
        # remove extra newlines
        word = re.sub(r'[\r|\n|\r\n]+', ' ', word)
        # lemmatize text
        # if text_lemmatization:
        #     word = lemmatize_text(word)
        # remove special characters and\or digits
        if special_char_removal:
            # insert spaces between special characters to isolate them
            special_char_pattern = re.compile(r'([{.(-)!}])')
            word = special_char_pattern.sub(" \\1 ", word)
            word = remove_special_characters(word, remove_digits=remove_digits)
            # print(word)
            # remove extra whitespace
        word = re.sub(' +', ' ', word)
        # remove stopwords
        # if stopword_removal:
        #     word = remove_stopwords(word, is_lower_case=text_lower_case)
        if fixed:
            word = correction(word)
            # print(word)

        normalized_search = [*normalized_search, word]
    # print(normalized_search)
        # print(type(normalized_search))

    # print(type(search_output))
    list_to_str = ' '.join([str(item) for item in normalized_search])
    print(list_to_str)
    # return list_to_str


# ## TEST EXAMPLE CASE WITH NEWS ARTICLES ##
#
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os
# # %matplotlib inline
#
# seed_urls = ['https://inshorts.com/en/read/technology',
#              'https://inshorts.com/en/read/sports',
#              'https://inshorts.com/en/read/world']
#
# def build_dataset(seed_urls):
#     news_data = []
#     for url in seed_urls:
#         news_category = url.split('/')[-1]
#         data = requests.get(url)
#         soup = BeautifulSoup(data.content, 'html.parser')
#
#         news_articles = [{'news_headline': headline.find('span',
#                                                          attrs={"itemprop": "headline"}).string,
#                           'news_article': article.find('div',
#                                                        attrs={"itemprop": "articleBody"}).string,
#                           'news_category': news_category}
#
#                          for headline, article in
#                          zip(soup.find_all('div',
#                                            class_=["news-card-title news-right-box"]),
#                              soup.find_all('div',
#                                            class_=["news-card-content news-right-box"]))
#                          ]
#         news_data.extend(news_articles)
#
#     df = pd.DataFrame(news_data)
#     df = df[['news_headline', 'news_article', 'news_category']]
#     return df
#
# news_df = build_dataset(seed_urls)
# news_df.head(10)
#
# # combining headline and article text
# news_df['full_text'] = news_df['news_headline'].map(str)+ '. ' + news_df['news_article']
#
# # pre-process text and store the same
# news_df['clean_text'] = normalize_corpus(news_df['full_text'])
# norm_corpus = list(news_df['clean_text'])
#
# # show a sample news article
# article = news_df.iloc[1][['full_text', 'clean_text']].to_dict()
# print(article)
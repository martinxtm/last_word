# coding: utf-8
import urllib2
from lxml.html import parse
import time
from collections import Counter
import re, string
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
import random


def get_statements():
    # get statement links from file:
    f = open('links.txt')
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    # get statements from links and xpath selector:
    statements = []
    for url in start_urls:
        request = urllib2.Request(url)
        opener = urllib2.build_opener()
        request.add_header('User-Agent', 'martinocker@gmx.de')
        response = opener.open(request)

        tree = parse(response)
        statements.append(str(tree.xpath('//*[@id="body"]/p[6]/text()')))
        # throttle to not fire too many requests at the same time
        time.sleep(0.2)
    return statements

def savefile(statements):
    # save statements into file:
    f = open('statements.txt', 'w+')
    for items in statements:
        f.write(items + '\n')
    f.close()

def loadfile():
    # load statements from file:
    f = open('statements.txt')
    statements = [url.strip() for url in f.readlines()]
    f.close()
    return statements


def wordFreq():
    # clean the statements and calculate word frequencies
    stopwords = stopwords.words ('english')

    def split_text(text):
        # help function to take out unnecessary rubbish (e.g. punctuation, numbers, etc.)
        newtext = re.sub('[^A-Za-z0-9\.]+', ' ', text)
        return re.split("[%s\s]" %re.escape(string.punctuation), newtext)

    # get list of words from list of statements
    wordsRaw = map(lambda t: t, [w for words in statements for w in split_text(words)])

    # filter stopwords
    words = filter(lambda w: len (w) != 0 and w not in stopwords, wordsRaw)
    return Counter(words)


def create_wordcloud(wordFreq):
    # create the wordcloud from the word frequencies

    def dict_to_tuple(dictdata):
        # write the dictionary into a list object
        tupledata = []
        for key, val in dictdata.items():
            tupledata.append([key, val])
        return tupledata

    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        # greyscale
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

    # create wordcloud
    wc = WordCloud(max_words=100, width=2400, height=1200, margin=10)
    ws = dict_to_tuple(wordFreq)
    wc.generate_from_frequencies(ws)

    # change color to greyscale
    wc.recolor(color_func=grey_color_func, random_state=3)

    wc.to_file("lastwords.png")
    # show
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

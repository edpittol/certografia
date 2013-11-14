# coding: utf-8

from nltk.tokenize import wordpunct_tokenize
from sqlalchemy import create_engine
import hunspell
import string
import os
import sys
import sqlite3
import inspect

dataDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/data'
hobj = hunspell.HunSpell(dataDir + '/vero/pt_BR.dic', dataDir + '/vero/pt_BR.aff')

bigramsEngine = create_engine('sqlite:///' + dataDir + '/bigrams.sqlite3')

def minEditDist(target, source):    
    n = len(target)
    m = len(source)

    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + insertCost(target[i-1])

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + deleteCost(source[j-1])

    for i in range(1,n+1):
        for j in range(1,m+1):
           distance[i][j] = min(distance[i-1][j]+1,
                                distance[i][j-1]+1,
                                distance[i-1][j-1]+substCost(source[j-1],target[i-1]))
    return distance[n][m]

def insertCost(target) :
    return 1

def deleteCost(source) :
    return 1

def substCost(target,source):
    if target == source: 
        return 0
    else: 
        return 2

def correctText(text):
    words = wordpunct_tokenize(text)

    before = False
    correctWords = []
    for word in words :
        correct = correctWord(word, before)
        correctWords.append(correct)
        before = correct[0]

    return correctWords

def correctWord(word, before=False):
    """
    Correct a word and return the corrected word, the original word and the 
    method. If the word is incorrect and the function doesn't get correct
    the corrected word is False.

    Methods:
    0 - if the don't apply a method
    1 - bigram model
    2 - mimimun edit distance

    Keyword arguments:
    word -- the word to be corrected 
    before -- the before word, used to language model (default False)
    """

    word = word.lower()
    correct = False
    method = 0
    suggests = []

    for punct in string.punctuation:
        if word.find(punct) >= 0:
            correct = word

    if not correct:
        # fix some bugs
        if word == u'\u2044' :
            word = unicode('/')

        encodeError = False

        try:
            wordEncoded = word.encode('iso-8859-1')
        except UnicodeEncodeError:
            encodeError = True

        if not encodeError:
            if word in string.punctuation or hobj.spell(wordEncoded):
                correct = word
            else:
                suggests = [suggestWord.decode('iso-8859-1').lower() for suggestWord in hobj.suggest(wordEncoded)]

    if suggests:
        if before and before not in string.punctuation:
            row = bigramsEngine.execute(" \
                SELECT word2 \
                FROM bigrams \
                WHERE word1 LIKE '" + before + "' AND word2 IN ('" + "', '".join(suggests) + "') \
                ORDER BY score DESC").fetchone()

            if row:
                correct = row[0]
                method = 1

        if not correct:
            method = 2
            distanceSelected = sys.maxint
            for suggest in suggests:
                distance = minEditDist(suggest, word)
                if distance < distanceSelected:
                    correct = suggest
                    distanceSelected = distance

    return (correct, word, method)

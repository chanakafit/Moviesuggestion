# -*- coding: utf-8 -*-
import json
import numpy as np
import re
from nltk.corpus import stopwords


def extractFromFile(fname):
    file = open(fname, 'r')
    array =  file.read()
    data  = json.loads(array)
    
    # remove element that doesn't have the Title or Plot fields
    data = [item for item in data if 'Title' in item and 'Plot' in item]

    return data

def formatTitle(data):
    titles = []
    for movie in data:
        titles.append(movie['Title'])
    return titles

def clean(word):
    #word = word.lower()
    word = re.sub('[!@#$?.,:;"()]', '', word)
    return word

def formatWords(data):
    words = []
    for movie in data:
        plot = movie['Plot'].lower()
        #word_list = plot.split()
        # remove 
        word_list = re.findall(r'\w+', plot, flags = re.UNICODE | re.LOCALE) 
        # remove the stopwords
        word_list = filter(lambda x: x not in stopwords.words('english'), word_list)
        for word in word_list:
            #word = clean(word)
            if word not in words:
                words.append(word)

    print 'There is ', len(words), ' words in the list.'
    return words

def generateMatrix(data, words):
    matrix = []
    for word in words:
        line = []
        for movie in data:
            count = 0
            word_list = movie['Plot'].split()
            for w in word_list:
                w = clean(w)
                if w == word:
                    count = count + 1
            line.append(count)
        matrix.append(line)
    return matrix


if __name__ == '__main__':

    # THIS SCRIPT CREATE THE DATASTRUCTURE WITH THE WORDS
    # FOUND IN THE PLOT DESCRIPTION OF EACH MOVIE
    
    #dataset = [1, 3, 5, 10, 50, 100]#, 3393]
    #dataset = [3393]
    dataset = [50]

    for n in dataset:
        fname = 'data2/moviedescriptions' + str(n) + '.json'
        movies_data = extractFromFile(fname)

        movies_titles = formatTitle(movies_data)
        #print movies_titles
        # format : movies = ["asdf", "asdfsadf", ...]

        movies_words = formatWords(movies_data)
        #for m in movies_words:
        #    print m

        movies_matrix = generateMatrix(movies_data, movies_words)
        #matrix = np.array(movies_matrix)
        #for m in matrix:
        #    print m
        #print matrix
        # format : matrix = np.array([
                #    [0,0,0,12,2,0],  # valeurs pour le 1er mot
                #    [0,0,0,12,2,0],  # valeurs pour le 2e mot
                #    [0,0,0,12,2,0]
                #    ])
                      # valeur pour un film

        output = {}
        output['titles'] = movies_titles
        output['words'] = movies_words
        output['matrix'] = movies_matrix
        
        output_fname = 'data3/data' + str(n) + '.json'
        with open(output_fname, 'w') as outfile:
            json.dump(output, outfile)

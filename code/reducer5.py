#!/usr/bin/python3
import sys
import re

counter = 0
def getLabelsAndVocabulary(line):
    labels = []
    words = []
    tokens = line.split(sep = '\t')
    # print('tokens = ', tokens)
    tmp = tokens[0].split(',')
    # print('labels = ', tmp)
    for c in tmp:
        labels.append(c.strip())

    idx_begin = tokens[1].index("\"")
    idx_end = tokens[1].rindex("\"")
    document = tokens[1][idx_begin+1:idx_end]
    wrds = re.findall('\\w+', document)
    # translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    # document = document.translate(translator)
    # document = document.split()
    for d in wrds:
        # d = re.sub(r'[^\w\s]','', d)
        d = d.lower()
        # if d not in stopwords:
        words.append(d)
    # print('labels = ', labels)
    return set(labels), words

# input comes from STDIN (standard input)
for line in sys.stdin:
    labels, words = getLabelsAndVocabulary(line)
    counter += 1
    for word in words:
        print('{}\t2\t{}'.format(word, counter), *list(labels), sep = '\t')

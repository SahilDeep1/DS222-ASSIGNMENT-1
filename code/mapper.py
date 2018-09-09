#!/usr/bin/python3
import sys
import re
from collections import defaultdict

# words per class i.e count words for class 'c'
words_per_class = defaultdict(lambda:0)
# frequency of occurence of class 'c'
classFreq = defaultdict(lambda:0)
# frequency of occurence of 'Any'/All class/es
anyClassFreq = 0

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
    return set(labels), words

# input comes from STDIN (standard input)
for line in sys.stdin:
    labels, words = getLabelsAndVocabulary(line)
    for label in labels:
        classFreq[label] += 1
        for word in words:
            # class:word and its count
            print('{}:{}\t{}'.format(label, word, 1))
            words_per_class[label] += 1

length = len(words_per_class)
total_freq = 0
for k in words_per_class:
    print(k + '_WC', str(words_per_class[k]), sep = '\t')
for k in classFreq:
    total_freq += classFreq[k]
    print(k, str(classFreq[k]), sep = '\t')
print('AnyClassFreq', total_freq, sep = '\t')

import os
import random
import time
import re
import numpy as np
import codecs
import math
import time
import string
from collections import defaultdict

stopwords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

TRAINING_FILE_PATH = '/scratch/ds222-2017/assignment-1/DBPedia.full/full_train.txt'
VALIDATION_FILE_PATH = '/scratch/ds222-2017/assignment-1/DBPedia.full/full_devel.txt'
TEST_FILE_PATH = '/scratch/ds222-2017/assignment-1/DBPedia.full/full_test.txt'

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

def trainNB(path):
    f = open(path, 'r')
    lines = f.readlines()
    # Count number of unique classes(50)
    classes = set()
    # count unique words in training data
    unique_words = set()
    # words per class i.e count words for class 'c'
    words_per_class = defaultdict(lambda:0)
    # count occurences of class 'c' and word 'w'
    cwcounter = defaultdict(lambda:0)
    # frequency of occurence of class 'c'
    classFreq = defaultdict(lambda:0)
    # frequency of occurence of 'Any'/All class/es
    anyClassFreq = 0

    for l in lines:
        labels, words = getLabelsAndVocabulary(l)
        # print(l)
        # print(labels, words)
        for w in words:
            unique_words.add(w)
            for lbl in labels:
                words_per_class[lbl] += 1
                cwcounter[(lbl, w)] += 1
        for tmp in labels:
            classes.add(tmp)
            classFreq[tmp] += 1
            anyClassFreq += 1
    qx = 1.0/len(unique_words)
    # print('unique_words = ', len(unique_words))

    return qx, anyClassFreq, classFreq, classes, words_per_class, cwcounter

def predict(words, qx, anyClassFreq, classFreq, classes, words_per_class, cwcounter, m = 1):
    qy = 1.0/len(classes)
    lprb = []
    contender_classes = []
    for c in sorted(classes):
        logprb = 0.0
        debug_counter = 0
        for w in words:
            logprb += math.log((cwcounter[(c, w)] + m*qx)/(words_per_class[c] + m))
            debug_counter += 1
        logprb += math.log((classFreq[c] + m*qy)/(anyClassFreq + m))
        # logprb += math.log((classFreq[c])/(anyClassFreq))
        lprb.append(logprb)
        contender_classes.append(c)
    # print('classes = ', contender_classes)
    # print('logprob = ', lprb)
    idx = lprb.index(max(lprb))
    # print('idx = ', idx)
    # print(lprb)
    return lprb[idx], contender_classes[idx], debug_counter


def testNB(path, qx, anyClassFreq, classes, words_per_class, cwcounter):
    f = open(path, 'r')
    lines = f.readlines()
    errors = 0
    correct = 0
    total = 0

    for l in lines:
        trueClass, words = getLabelsAndVocabulary(l)
        # print(words)
        log_prb, predictedClass, debug_counter = predict(words, qx, anyClassFreq, classFreq, classes, words_per_class, cwcounter)
        if predictedClass in trueClass:
            correct +=1
        else:
            errors +=1
        print(log_prb, predictedClass, debug_counter, *trueClass, sep = '\t')
            # print('Incorrect', total + 1, "  = ", l, trueClass, words, 'classified as ', predictedClass)
        total += 1
        # if total % 5000 == 0:
        #     print('Correct = ', correct, 'Total predictions = ', total)
        #     print('Accuracy = ', correct/total)
    assert (total == errors + correct)
    assert (total == len(lines))

    accuracy = correct/total
    return accuracy

print('Training...')
t1 = time.time()
qx, anyClassFreq, classFreq, classes, words_per_class, cwcounter = trainNB(TRAINING_FILE_PATH)
t2 = time.time()
time_to_train = t2 - t1
print('Training time = ', time_to_train, 'seconds')
# print('qx = ', qx)
# print('qy = ', 1.0/len(classes))
# print('anyClassFreq = ', anyClassFreq)
# print('classFreq = ', classFreq)
# print('classes = ', classes)
# print('words_per_class = ', words_per_class)
# print('cwcounter = ', cwcounter)
msgs1 = ['Testing on Training Data', 'Testing on Dev Data', 'Testing on Test Data']
msgs2 = ['Testing Time on Training Data', 'Testing Time on Validation Data', 'Testing Time on Test Data']
msgs3 = ['Accuracy on Training Data', 'Accuracy on Dev Data', 'Accuracy on Test Data']
paths = [TRAINING_FILE_PATH, VALIDATION_FILE_PATH, TEST_FILE_PATH]
for i in range(3):
    t1 = time.time()
    print(msgs1[i])
    accuracy = testNB(paths[i], qx, anyClassFreq, classes, words_per_class, cwcounter)
    t2 = time.time()
    time_to_test = t2 - t1
    print(msgs2[i], time_to_test, 'seconds')
    print(msgs3[i], accuracy)

# print('Testing')
# print('anyClassFreq = ', anyClassFreq)
# t1 = time.time()
# accuracy = testNB(TEST_FILE_PATH, qx, anyClassFreq, classes, words_per_class, cwcounter)
# t2 = time.time()
# time_to_test = t2 - t1
# print('Time to test = ', time_to_test, 'seconds')
# print('Accuracy = ', accuracy)

#!/usr/bin/python3
import sys

# current word fetched
last_word = None
unique_counts = 0

for line in sys.stdin:
    word = line.strip()
    if last_word == word:
        continue
    else:
        if last_word is not None:
            unique_counts += 1
        last_word = word

if last_word == word:
    unique_counts += 1
print('UniqueWordsVocabulary', unique_counts, sep = '\t')

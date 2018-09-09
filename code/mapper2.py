#!/usr/bin/python3
import sys

for line in sys.stdin:
    line = line.strip()
    label_word, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue
    if ':' not in label_word:
        continue
    label, word = label_word.split(':', 1)
    print('{}\t{}:{}'.format(word, label, count))

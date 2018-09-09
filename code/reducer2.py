#!/usr/bin/python3
import sys

# current word fetched
last_key = None

def printList(word, l):
    # print('word = ', word, ' list = ', l)
    print(word, 1, sep='\t', end='\t')
    print(*l, sep=' ')

ll = []
for line in sys.stdin:
    line = line.strip()
    word, label_count = line.split('\t', 1)
    # print('word = ', word, 'label_count = ', label_count)
    if last_key == word:
        ll.append(label_count)
    else:
        if last_key is not None:
            printList(last_key, ll)
        ll.clear()
        ll.append(label_count)
        last_key = word

if last_key == word:
    printList(last_key, ll)

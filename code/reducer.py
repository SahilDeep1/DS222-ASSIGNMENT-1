#!/usr/bin/python3
import sys

# current label_word
cw = None
# current label_word count
cw_counter = 0

label_word = None

for line in sys.stdin:
    line = line.strip()
    label_word, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue
    if cw == label_word:
        cw_counter += count
    else:
        if cw:
            print('{}\t{}'.format( cw, cw_counter))
        cw_counter = count
        cw = label_word

if cw == label_word:
    print('{}\t{}'.format(cw, cw_counter))

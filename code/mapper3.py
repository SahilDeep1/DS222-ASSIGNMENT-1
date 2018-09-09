#!/usr/bin/python3
import sys

for line in sys.stdin:
    line = line.strip()
    label, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue
    if ':' in label:
        continue
    print(label, count, sep = '\t')

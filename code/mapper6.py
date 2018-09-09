#!/usr/bin/python3
import sys

last = None
lastInfo = None

for line in sys.stdin:
    line = line.strip()
    word, op_id, tmp = line.split('\t', 2)
    # print(word, op_id, tmp)
    if op_id == '2':
        if word != last:
            # The given test example word was "never" seen in training
            f, lbls = tmp.split('\t', 1)
            try:
                e_id = int(f)
            except ValueError:
                continue
            # This indicates that we have no "training" knowledge about this word
            print('{}\t{}\t{}'.format(e_id, word, ''), lbls, sep = '\t')
            last = None
            lastInfo = None
            continue
        f, lbls = tmp.split('\t', 1)
        try:
            e_id = int(f)
        except ValueError:
            continue
        # print('e_id = ', e_id)
        print('{}\t{}\t{}'.format(e_id, last, lastInfo), lbls, sep = '\t')
    elif (op_id == '1'):
        last = word
        lastInfo = tmp
    else:
        assert False

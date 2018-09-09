#!/usr/bin/python3
import sys
import math

words_per_class = {}
classFreq = {}

logPrb_per_class = {}

last_id = None

m = 1

anyClassFreq = 0
uniqueWordsCount = 0

total_count = 0
correct = 0
wrongly_classified = 0
unique_classes = 0
qx = None
qy = None
classes = set()

# def resetDS():
#     logPrb_per_class.clear()
#     for c in classes:
#         logPrb_per_class[c] = 0

def predict(table):
    prob = []
    contender_classes = []
    for k in sorted(classes):
        old_value = table.get(k, 0)
        new_value = old_value + math.log((classFreq.get(k, 0) + m*qy)/(anyClassFreq + m))
        table[k] = new_value
        prob.append(new_value)
        contender_classes.append(k)

    # print(prob)
    idx = prob.index(max(prob))
    return prob[idx], contender_classes[idx]

def load_params(path):
    global unique_classes
    global uniqueWordsCount
    global qx
    global qy
    global anyClassFreq
    global classes
    f = open(path, 'r')
    for line in f:
        line = line.strip()
        key, count = line.split('\t')
        try:
            count = int(count)
        except ValueError:
            continue
        if key == 'AnyClassFreq':
            anyClassFreq = count
            continue
        if key == 'UniqueWordsVocabulary':
            uniqueWordsCount = count
            continue
        if key[-3:] == '_WC':
            words_per_class[key[:-3]] = count
        else:
            classFreq[key] = count
            classes.add(key)
    assert (len(classFreq) == len(words_per_class))
    unique_classes = len(classFreq)
    qx = 1.0/uniqueWordsCount
    qy = 1.0/unique_classes
    f.close()

load_params('/home/sahildeep/1/output/params.txt')

#print('uniqueWordsCount = ', uniqueWordsCount, 'unique_classes = ', unique_classes, 'words_per_class = ', words_per_class, 'classFreq = ', classFreq, 'anyClassFreq =', anyClassFreq, 'qx = ', qx, 'qy = ', qy)

# debug_counter = 0
for line in sys.stdin:
    line = line.strip()
    c_id, word, tmp, tc = line.split('\t', 3)
    if c_id != last_id:
        if last_id is not None:
            logProbability, predictedClass = predict(logPrb_per_class)
            if predictedClass in trueClass:
                correct += 1
            else:
                wrongly_classified += 1
            # print(last_id, logProbability, predictedClass, debug_counter, *trueClass, sep = '\t')
            print(last_id, logProbability, predictedClass, *trueClass, sep = '\t')
            # debug_counter = 0
            logPrb_per_class.clear()

    # debug_counter += 1
    last_id = c_id
    trueClass = tc.split('\t')
    label_count = tmp.split(' ')
    # print('label_count =', label_count)
    tmp_set = set(classes)
    for e in label_count:
        # print('e =',e)
        if e == '':
            continue
        label, count = e.split(':', 1)
        try:
            count = int(count)
        except ValueError:
            assert False
            continue
        tmp_set.remove(label)
        old_value = logPrb_per_class.get(label, 0)
        new_value = old_value + math.log((count + m*qx)/(words_per_class.get(label, 0) + m))
        logPrb_per_class[label] = new_value
    for e in tmp_set:
        count = 0
        old_value = logPrb_per_class.get(e, 0)
        new_value = old_value + math.log((count + m*qx)/(words_per_class.get(e, 0) + m))
        logPrb_per_class[e] = new_value

if len(logPrb_per_class) != 0:
    logProbability, predictedClass =  predict(logPrb_per_class)
    if predictedClass in trueClass:
        correct += 1
    else:
        wrongly_classified += 1
    # print(logProbability, predictedClass, debug_counter, *trueClass, sep = '\t')
    print(last_id, logProbability, predictedClass, *trueClass, sep = '\t')

total_count = correct + wrongly_classified
print('total_count = ', total_count)
accuracy = correct/total_count
print('Accuracy = ', accuracy)

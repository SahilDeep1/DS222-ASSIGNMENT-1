####################################Training Phase #############################
export LC_ALL=C
# Get count for each label-word combination
cat /home/kartik/DBPedia.full/full_train.txt | python3 mapper.py | sort -k 1,1 | python3 reducer.py > /home/kartik/out_train.txt
# Get all labels(and counts) for each word
cat /home/kartik/out_train.txt | python3 mapper2.py | sort -k 1,1 | python3 reducer2.py > /home/kartik/c_prime.txt
# Get classifier general params
cat /home/kartik/out_train.txt | python3 mapper3.py > /home/kartik/classifier_params.txt
# Get the unique words
cat ~/c_prime.txt | cut -f1 | sort | python3 reducer4.py >> /home/kartik/classifier_params.txt



################################# Testing phase ##################################
# Convert testing data to <word id>
cat /home/kartik/DBPedia.full/full_test.txt | python3 mapper5.py > /home/kartik/out_test.txt
# Merge c_prime and out_test to get <id word labels>. Use numeric sort
# cat /home/kartik/c_prime.txt /home/kartik/out_test.txt | sort -k 1,1 -k 2,2 | python3 mapper6.py | sort -n -k 1,1 > /home/kartik/h3
cat /home/kartik/c_prime.txt /home/kartik/out_test.txt | sort -k 1,1 -k 2,2 | python3 mapper6.py | sort -n -k 1,1 | python3 reducer6.py > /home/kartik/result

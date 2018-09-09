# DS222-ASSIGNMENT-1

To run naive bayes in local mode use


$cd code

$python3 nb_inmemory.py
In nb_inmemory the paths are specified as 

TRAINING_FILE_PATH='/scratch/ds222-2017/assignment-1/DBPedia.full/full_train.txt'

VALIDATION_FILE_PATH='/scratch/ds222-2017/assignment-1/DBPedia.full/full_devel.txt'

TEST_FILE_PATH='/scratch/ds222-2017/assignment-1/DBPedia.full/full_test.txt'

Change them as per requirement

output log will be generated in out_nb_inmemory.log
#############################################################################################################################################


Now coming to the implementation in distributed setting

$cd code

Thereafter we can run it using the following


make t=<HDFS path of the file to be tested(training is done on full_train.txt)> nr=<# of reducers>

Above command will run both training and testing and put the final result in the folder final_output

If you want to do only training:


make train nr=<# of reducers>

if you have already done training and want to run testing now

make test t=/user/ds222/assignment-1/DBPedia.full/full_test.txt nr=<# of reducers>

Change the path accordingly when you test on training, development and test respectively i.e change the files from full_test.txt ,
full_devel.txt or full_train.

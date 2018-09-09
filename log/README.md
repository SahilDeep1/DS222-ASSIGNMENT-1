To run naive bayes in local mode use
cd code
$python3 nb_inmemory.py

output log will be generated in out_nb_inmemory.log
#############################################################################################################################################


Now coming to the implementation in distributed setting
$cd code

Thereafter we can run it using the following
make t=<HDFS path of the file to be tested(training is done on full_train.txt)> nr=<# of reducers>

Above command will run both training and testing and put the final result in the folder final_output

If you want to do only training:
make train nr=<nos of reducers>

if you have already done training and want to run testing now

make test t=/user/ds222/assignment-1/DBPedia.full/full_test.txt nr=<nos of reducers>

Change the path accordingly when you test on training, development and test respectively i.e change the files from full_test.txt full_devel.txt or full_train.

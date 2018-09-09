echo "Training Part 1"
rm -f interim/*
hadoop fs -rmr /user/sahildeep/1/output/interim

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=4 -file "/home/sahildeep/1/code/mapper.py" -mapper "mapper.py" -file "/home/sahildeep/1/code/reducer.py" -reducer "reducer.py" -input "/user/ds222/assignment-1/DBPedia.full/full_train.txt" -output "/user/sahildeep/1/output/interim"

hadoop fs -get /user/sahildeep/1/output/interim/part-* interim

echo "Training Part 2"
rm -f c_prime/*
hadoop fs -rmr /user/sahildeep/1/output/c_prime

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=4 -file "/home/sahildeep/1/code/mapper2.py" -mapper "mapper2.py" -file "/home/sahildeep/1/code/reducer2.py" -reducer "reducer2.py" -input "/user/sahildeep/1/output/interim/part-*" -output "/user/sahildeep/1/output/c_prime"

hadoop fs -get /user/sahildeep/1/output/c_prime/part-* c_prime

echo "Training Part 3"
rm -f classifier_params/*
hadoop fs -rmr /user/sahildeep/1/output/classifier_params

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=0 -file "/home/sahildeep/1/code/mapper3.py" -mapper "mapper3.py" -input "/user/sahildeep/1/output/interim/part-*" -output "/user/sahildeep/1/output/classifier_params"

hadoop fs -get /user/sahildeep/1/output/classifier_params/part-* classifier_params

# hadoop fs -cat "/user/sahildeep/1/output/classifier_params/part-*" > /home/sahildeep/classifier_params.txt


# Here reducers must be exactly 1 since we are counting the number of unique words
echo "Training Part 4"
rm -f vocabulary_count/*
hadoop fs -rmr /user/sahildeep/1/output/vocabulary_count

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=1 -input "/user/sahildeep/1/output/c_prime/part-*" -output "/user/sahildeep/1/output/vocabulary_count" -mapper "cut -f1" -file "/home/sahildeep/1/code/reducer4.py" -reducer "reducer4.py"

hadoop fs -get /user/sahildeep/1/output/vocabulary_count/part-* vocabulary_count

# Create the final params.txt file
echo "Creating classifier params"
rm -f /home/sahildeep/1/output/params.txt
hadoop fs -cat "/user/sahildeep/1/output/classifier_params/part-*" "/user/sahildeep/1/output/vocabulary_count/part-*" > /home/sahildeep/1/output/params.txt

# Upload the file
hadoop fs -rmr /user/sahildeep/1/output/params.txt
hadoop fs -put "/home/sahildeep/1/output/params.txt" "/user/sahildeep/1/output/"


############################### Testing Starts Now #####################

echo "Testing Part 1"
rm -f test_interim/*
hadoop fs -rmr /user/sahildeep/1/output/test_interim

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=1 -input "/user/ds222/assignment-1/DBPedia.full/full_test.txt" -output "/user/sahildeep/1/output/test_interim" -mapper "cat" -reducer "reducer5.py" -file "/home/sahildeep/1/code/reducer5.py"

hadoop fs -get /user/sahildeep/1/output/test_interim/part-* test_interim
# 1 Reducer to get the merged output in 1 file
# This step has a bug
echo "Testing Part 2"
rm -f test_merged/*
hadoop fs -rmr /user/sahildeep/1/output/test_merged

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=1 -input "/user/sahildeep/1/output/test_interim/part-*" -input "/user/sahildeep/1/output/c_prime/part-*" -output "/user/sahildeep/1/output/test_merged" -mapper "cat" -reducer "sort -k 1,1 -k 2,2"

hadoop fs -get /user/sahildeep/1/output/test_merged/part-* test_merged

# Run the final classifiaction
echo "Running Final .."
rm -f prediction/*
hadoop fs -rmr /user/sahildeep/1/output/prediction

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.output.key.comparator.class="org.apache.hadoop.mapred.lib.KeyFieldBasedComparator" -D mapred.text.key.comparator.options=-n -D mapred.reduce.tasks=6 -input "/user/sahildeep/1/output/test_merged/part-*" -output "/user/sahildeep/1/output/prediction" -mapper "mapper6.py" -file "/home/sahildeep/1/code/mapper6.py" -reducer "reducer6.py" -file "/home/sahildeep/1/code/reducer6.py"
hadoop fs -get /user/sahildeep/1/output/prediction/part-* prediction

rm -f final_output/*
hadoop fs -rmr /user/sahildeep/1/output/final_output

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D mapred.reduce.tasks=1 -input "/user/sahildeep/1/output/prediction/part-*" -output "/user/sahildeep/1/output/final_output" -mapper "cat" -reducer "sort -k 1,1 -n"

hadoop fs -get /user/sahildeep/1/output/final_output/part-* final_output

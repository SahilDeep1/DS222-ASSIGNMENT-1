HADOOP_STREAMIN_CMD=hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar 
INTERIM_PATH=/user/sahildeep/1/output/interim
C_PRIME_PATH=/user/sahildeep/1/output/c_prime
CLASSIFIER_PARAMS_PATH=/user/sahildeep/1/output/classifier_params
VOCABULARY_PATH=/user/sahildeep/1/output/vocabulary_count
PARAMS_FILE=/home/sahildeep/1/output/params.txt
TEST_INTERIM_PATH=/user/sahildeep/1/output/test_interim
TEST_MERGED_PATH=/user/sahildeep/1/output/test_merged
TEST_PREDICTION_PATH=/user/sahildeep/1/output/prediction
FINAL_OUTPUT_PATH=/user/sahildeep/1/output/final_output


run: train test

train:
	@echo "Training Pipe 1"
	hadoop fs -rm -r -f $(INTERIM_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.reduce.tasks=${nr} -file "/home/sahildeep/1/code/mapper.py" -mapper "mapper.py" -file "/home/sahildeep/1/code/reducer.py" -reducer "reducer.py" -input "/user/ds222/assignment-1/DBPedia.full/full_train.txt" -output $(INTERIM_PATH)

	@echo "Training Pipe 2"
	hadoop fs -rm -r -f $(C_PRIME_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.reduce.tasks=${nr} -file "/home/sahildeep/1/code/mapper2.py" -mapper "mapper2.py" -file "/home/sahildeep/1/code/reducer2.py" -reducer "reducer2.py" -input $(INTERIM_PATH)/part-* -output $(C_PRIME_PATH)

	@echo "Training Pipe 3"
	hadoop fs -rm -r -f $(CLASSIFIER_PARAMS_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.reduce.tasks=0 -file "/home/sahildeep/1/code/mapper3.py" -mapper "mapper3.py" -input $(INTERIM_PATH)/part-* -output $(CLASSIFIER_PARAMS_PATH) 

	@echo "Training Pipe 4"
	hadoop fs -rm -r -f $(VOCABULARY_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.reduce.tasks=1 -input $(C_PRIME_PATH)/part-* -output $(VOCABULARY_PATH) -mapper "cut -f1" -file "/home/sahildeep/1/code/reducer4.py" -reducer "reducer4.py" 

	@echo "Creating classifier params"
	rm -f $(PARAMS_FILE)
	hadoop fs -cat $(CLASSIFIER_PARAMS_PATH)/part-* $(VOCABULARY_PATH)/part-* > $(PARAMS_FILE)

test: 
	@echo "Testing Pipe 1"
	hadoop fs -rm -r -f $(TEST_INTERIM_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.reduce.tasks=1 -input $(t) -output $(TEST_INTERIM_PATH) -mapper "cat" -reducer "reducer5.py" -file "/home/sahildeep/1/code/reducer5.py" 

	echo "Testing Pipe 2"
	rm -f test_merged/*
	hadoop fs -rm -r -f $(TEST_MERGED_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.reduce.tasks=1 -input $(TEST_INTERIM_PATH)/part-* -input $(C_PRIME_PATH)/part-* -output $(TEST_MERGED_PATH) -mapper "cat" -reducer "sort -k 1,1 -k 2,2" 

	@echo "Running Final Predictions"
	hadoop fs -rm -r -f $(TEST_PREDICTION_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.output.key.comparator.class="org.apache.hadoop.mapred.lib.KeyFieldBasedComparator" -D mapred.text.key.comparator.options=-n -D mapred.reduce.tasks=6 -input $(TEST_MERGED_PATH)/part-* -output $(TEST_PREDICTION_PATH) -mapper "mapper6.py" -file "/home/sahildeep/1/code/mapper6.py" -reducer "reducer6.py" -file "/home/sahildeep/1/code/reducer6.py" 

	rm -f final_output/*
	hadoop fs -rm -r -f $(FINAL_OUTPUT_PATH)
	$(HADOOP_STREAMIN_CMD) -D mapred.reduce.tasks=1 -input $(TEST_PREDICTION_PATH)/part-* -output $(FINAL_OUTPUT_PATH) -mapper "cat" -reducer "sort -k 1,1 -n" 
	hadoop fs -get $(FINAL_OUTPUT_PATH)/part-* final_output

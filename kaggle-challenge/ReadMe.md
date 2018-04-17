


## Other Attempts
Apart from the two results we submitted above, we also tried other approaches.
But these were not chosen due to increase in computation time.

#####Using Cosine Similarity :: 

**Parallelism** : We make many processeses which loop over all the distinct ForUSerID in test-data (127304 iterations in tottal). To not overwhelm the memory, we perform a bunch of computation parallely and then after joining all the processes , start the next set of test-
data points.

**Batch computation** : To reduce computation time, we read all UserID to be rated for 1 ForUserID (i) in the test data. Then we get all ratings from train-data for all UserIDs who have actually rated for i. We then obtain a rating-hot vector for these 2 lists and find cosine-distance. This will give us the similarity metric between 2 UsersID. We do a dot product with the given ratings to obtain the final rating.

**SubSampling** : When we read the list of UserIDs from train-data, we take the top 25 ones to make computation faster. 

We did not submit this because this was taking ~6hrs to compute and validation accuracy was'nt that good.
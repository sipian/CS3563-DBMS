# Our idea : `relation_user_user.py`

### Assumptions

+ Assume that the friendship is directed, which means that if (u, i) is in the friendship graph, then it is not necessary that (i, u) will be present.

+ Assume that the phrase "x is a friend of y" means "x" has given "y" a rating.

### Algorithm

+ Given a pair (u, i), we find out all the users who are friends with "i".
+ Now obtain the ratings given by these users to "i" and the number of ratings given in all per user.
+ For every user who is a friend of "i", weigh the rating given to "i" proportionally to the number of ratings given by that user.
    + This is in some-sense a feedback oriented system.
+ Perform the same thing, but with "u" instead of "i". Here we are interested in the friends of "u", rather than the people who have "u" as a friend.
+ Now take the weighted ratings, and weigh these ratings by the connections of each side - number of people who have "i" as a friend and number of friends of "u" respectively.
+ This will give the final rating.

# Our idea : `hybrid_user_user.py`

### Algorithm

+ This is the essentially the first part of the algorithm, where we don't consider the user side of the rating, both only the item side. (Step 1 to 3)
+ All terminology remains the same.

# Other Attempts : `parallel-cosine-similarity-user-user.py`
+ Apart from the two results we submitted above, we also tried other approaches.
+ But these were not chosen due to increase in computation time.

### Using Cosine Similarity

+ **Parallelism** : We make many processeses which loop over all the distinct `ForUserID` in test-data (127304 iterations in total). To not overwhelm the memory, we perform a bunch of computation in parallel and then after joining all the processes, start the next set of test-data points.
+ **Batch computation** : To reduce computation time, we read all `UserId` to be rated for 1 `ForUserId` (i) in the test data. Then we get all ratings from train-data for all `UserId`s who have actually rated for i. We then obtain a rating-hot vector for these 2 lists and find cosine-distance. This will give us the similarity metric between 2 `UserId`s. We do a dot product with the given ratings to obtain the final rating.
+ **Sub-sampling** : When we read the list of `UserId`s from train-data, we take the top 25 ones to make computation faster. 

_We did not submit this because this was taking ~6hrs to compute and validation accuracy wasn't that good._

#### How to run
+ Since postgres can have problem of being run by postgres user, [this](http://suite.opengeo.org/docs/latest/dataadmin/pgGettingStarted/firstconnect.html#allowing-local-connections) can be used to allow to run from normal user. 
+ Also it is recommended to run the python program with `sudo`.
+ If there is an error message of `train_user_ratings.csv` file not found, the relative path for all the `.csv` can be changed to an absolute path in the Python code.

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

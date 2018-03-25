/* Assumption Role table has a new role as singer */

/* Question 1 */
SELECT RESULT2.PersonName, RESULT1.counters FROM
    (
    SELECT F.PersonID, count(*) AS counters FROM 
        ((SELECT PictureID, PersonID FROM ROLE WHERE role = 'Singer' AND ismovie = True) AS ROLET
        INNER JOIN
        (SELECT PictureID FROM AWARDS WHERE winner = True AND awardorganization = 'oscar' ) AS AWARDST
        ON
        ROLET.PictureId = AWARDST.PictureId) AS F
        GROUP BY F.PersonID
    ) AS RESULT1
    INNER JOIN
    (
    SELECT PersonName, PersonID FROM PERSON
    ) AS RESULT2
    ON
    RESULT1.PersonId = RESULT2.PersonID;

/* Question 2 */
SELECT RESULT2.PersonName, RESULT1.counters FROM
    (
    SELECT F.PersonID, count(*) AS counters FROM 
        ((SELECT PictureID, PersonID FROM ROLE WHERE role = 'Director' AND IsMovie = True) AS ROLET
        INNER JOIN
        (SELECT PictureID FROM RATING WHERE averagerating > 5) AS RATINGT
        ON
        ROLET.PictureId = RATINGT.PictureId) AS F
        GROUP BY F.PersonID
    ) AS RESULT1
    INNER JOIN
    (
    SELECT PersonName, PersonID FROM PERSON
    ) AS RESULT2
    ON
    RESULT1.PersonId = RESULT2.PersonID;

/* Question 3 */
SELECT RESULT2.PersonName, RESULT1.max_avg_of_avg FROM
    (
    SELECT RESULTINTER.PersonID, max(RESULTINTER.avg_of_avg) as max_avg_of_avg FROM
        (
        SELECT F.PersonID, avg(F.averageRating) AS avg_of_avg FROM 
            ((SELECT PictureID, PersonID FROM ROLE WHERE role = 'Director' AND IsMovie = True) AS ROLET
            INNER JOIN
            (SELECT * FROM RATING) AS RATINGT
            ON
            ROLET.PictureId = RATINGT.PictureId) AS F
            GROUP BY F.PersonID
        ) AS RESULTINTER GROUP BY RESULTINTER.PersonID
    ) AS RESULT1
    INNER JOIN
    (
    SELECT PersonName, PersonID FROM PERSON
    ) AS RESULT2
    ON
    RESULT1.PersonID = RESULT2.PersonID;

/* Question 4 */
WITH MOVIES AS (SELECT * FROM PICTURE WHERE IsMovie = True)
    SELECT PrimaryTitle, StartYear as Year, Duration FROM
    MOVIES WHERE (StartYear, Duration) IN
        (
        SELECT StartYear, min(Duration) FROM
            MOVIES GROUP BY StartYear
        ) ORDER BY PrimaryTitle, StartYear;

/* Question 5 */
WITH MOVIES AS (SELECT * FROM PICTURE WHERE IsMovie = True),
     GENREJOIN AS (SELECT PrimaryTitle, Genre, Duration FROM 
                   (
                   MOVIES
                   INNER JOIN
                   GENRES
                   ON
                   GENRES.PictureID = MOVIES.PictureID)
                  )
    SELECT PrimaryTitle, Genre, Duration FROM
    GENREJOIN WHERE (Genre, Duration) IN
        (
        SELECT Genre, min(Duration) FROM
            GENREJOIN GROUP BY Genre
        ) ORDER BY PrimaryTitle, Genre;

/* Question 6 */
WITH ADULT_RATINGS AS (SELECT * FROM
                       (
                       (SELECT PictureID, PrimaryTitle, IsMovie FROM PICTURE WHERE Adult = True) AS ADULTPICS
                       INNER JOIN
                       (SELECT PictureID, averageRating FROM RATING) AS RATS
                       ON
                       ADULTPICS.PictureID = RATS.PictureID) 
                      )
    (SELECT PrimaryTitle, averageRating, IsMovie from ADULT_RATINGS WHERE IsMovie = True ORDER BY averageRating DESC LIMIT 1)
    UNION
    (SELECT PrimaryTitle, averageRating, IsMovie from ADULT_RATINGS WHERE IsMovie = False ORDER BY averageRating DESC LIMIT 1);

/* Question 7 */
WITH GENRE_JOIN AS (SELECT PICINFO.PictureID, PICINFO.PrimaryTitle, PICINFO.IsMovie, RATINFO.averageRating, G.Genre FROM
                    (SELECT PictureID, PrimaryTitle, IsMovie FROM PICTURE) AS PICINFO
                    INNER JOIN
                    (SELECT PictureID, averageRating FROM RATING) AS RATINFO
                    ON
                    RATINFO.PictureID = PICINFO.PictureID
                    INNER JOIN
                    GENRES AS G ON G.PictureID = RATINFO.PictureID),
     GENRE_GROUP_MAX AS (SELECT A.Genre, A.averageRating, A.PrimaryTitle, A.IsMovie FROM
                         GENRE_JOIN AS A
                         LEFT OUTER JOIN GENRE_JOIN AS B
                         ON A.Genre = B.Genre AND A.averageRating < B.averageRating WHERE B.Genre IS NULL)
     (SELECT PrimaryTitle, averageRating, Genre, IsMovie from GENRE_GROUP_MAX WHERE IsMovie = True)
     UNION
     (SELECT PrimaryTitle, averageRating, Genre, IsMovie from GENRE_GROUP_MAX WHERE IsMovie = False) ORDER BY Genre;

/* Question 9 */
/* Assumption: Interpretation of award winning actor as an actor who has won any award for movies*/
WITH MOVIE_ACTOR AS (SELECT PersonID, PictureID FROM ROLE WHERE IsMovie = True AND Role = 'Actor'),
     AWARD_WINNING_ACTOR AS (SELECT A.PersonID, A.PictureID FROM
                                (SELECT PersonID, PictureID FROM MOVIE_ACTOR
                                 INTERSECT
                                 (SELECT PersonID, PictureID FROM AWARDS WHERE Winner = True AND LOWER(AwardName) LIKE '%actor%')
                                ) AS A),
     MOVIES_WITH_AWARDEES AS (SELECT A.PersonID, A.PictureID FROM
                                (MOVIE_ACTOR AS A
                                 INNER JOIN
                                 AWARD_WINNING_ACTOR AS B ON B.PersonID = A.PersonID)),
     GENRE_JOIN AS (SELECT PICINFO.PictureID, G.Genre, PICINFO.PrimaryTitle, PICINFO.GrossBoxOffice FROM
                    (SELECT PictureID, GrossBoxOffice, PrimaryTitle FROM
                     PICTURE WHERE IsMovie = True AND GrossBoxOffice IS NOT NULL) AS PICINFO
                    INNER JOIN
                    GENRES AS G ON G.PictureID = PICINFO.PictureID),
     GENRE_GROUP_MAX AS (SELECT A.PictureID, A.PrimaryTitle, A.Genre, A.GrossBoxOffice FROM
                         GENRE_JOIN AS A
                         LEFT OUTER JOIN GENRE_JOIN AS B
                         ON A.Genre = B.Genre AND A.GrossBoxOffice < B.GrossBoxOffice WHERE B.Genre IS NULL)
     SELECT DISTINCT GGM.Genre, MWA.PictureID, GGM.PrimaryTitle, P.PersonName, GGM.GrossBoxOffice FROM
            GENRE_GROUP_MAX AS GGM
            INNER JOIN MOVIES_WITH_AWARDEES AS MWA
            ON GGM.PictureID = MWA.PictureID
            INNER JOIN PERSON AS P
            ON MWA.PersonID = P.PersonID;

/* Question 12 */

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
    (SELECT PrimaryTitle, averageRating from ADULT_RATINGS WHERE IsMovie = True ORDER BY averageRating DESC LIMIT 1)
    UNION
    (SELECT PrimaryTitle, averageRating from ADULT_RATINGS WHERE IsMovie = False ORDER BY averageRating DESC LIMIT 1);

/* Question 7 */
WITH PICINFO_RATS_JOIN AS (SELECT * FROM
                            ((SELECT PictureID, PrimaryTitle FROM PICTURE) AS PICINFO
                             INNER JOIN
                             (SELECT PictureID, averageRating FROM RATING) AS RATS
                             ON
                             PICINFO.PictureID = RATS.PictureID
                            )),
    GENRE_JOIN AS (SELECT * FROM
                        PICINFO_RATS_JOIN INNER JOIN GENRES ON PICINFO_RATS_JOIN.PictureID = GENRES.PictureID)
    SELECT A.Genre, A.averageRating, A.PrimaryTitle FROM
        GENRE_JOIN AS A
        INNER JOIN (
                   SELECT Genre, max(averageRating) as averageRating
                   FROM GENRE_JOIN
                   GROUP BY Genre
                   ) AS B ON A.Genre = B.Genre AND A.averageRating = B.averageRating;

Assume table is F
select a.*
from F a
LEFT OUTER JOIN F b
on a.genre = b.genre AND a.rating < b.rating
where b.genre IS NULL;


/* QUESTION 8 */

WITH DURATION_TABLE AS (
    SELECT PictureID, PrimaryTitle, coalesce(EndYear::real, 2018)-StartYear Duration
    FROM PICTURE
    WHERE StartYear IS NOT NULL AND IsMovie=FALSE
)
SELECT PrimaryTitle
FROM DURATION_TABLE
ORDER BY Duration DESC
LIMIT 1

/*  QUESTION 11 */

Assume role table has rows for singer as a role  

WITH AWARD_WINNING_SINGERS AS (SELECT A.PersonID,A.Year FROM
        (SELECT Year, PersonID FROM AWARDS WHERE AwardOrganization = 'grammy' AND Winner = True AND Year IS NOT NULL) AS A
        INNER JOIN 
        (SELECT PersonID FROM ROLE WHERE Role = 'singer') AS B
        ON
        A.PersonID = B.PersonID)

SELECT F.PersonName, 2018-F.BirthYear
FROM (
    SELECT E.PersonName, E.BirthYear, E.Year - E.BirthYear Duration
    FROM (
        AWARD_WINNING_SINGERS
        INNER JOIN
        (SELECT  PersonID, PersonName, BirthYear FROM PERSON WHERE BirthYear IS NOT NULL) AS C
        ON AWARD_WINNING_SINGERS.PersonID = C.PersonID) AS E
        ORDER BY Duration DESC
        LIMIT 1
    ) AS F

/* Question 17 
WITH PERSONNAMETABLE AS (SELECT PersonID, PersonName FROM PERSON),
     DIRECTORTABLE AS (SELECT PersonID, PictureID FROM ROLE WHERE role = 'Director' and IsMovie = True),
     PICTUREGROSSTABLE AS (SELECT PictureID, PrimaryTitle FROM PICTURE WHERE IsMovie = True and GrossBoxOffice > 2000000)
     SELECT RES.PersonName, RES.PrimaryTitle, RES.Genre FROM
        (
                ------ need to wrap this up ------
*/
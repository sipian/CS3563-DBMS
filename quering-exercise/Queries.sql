/* Assumption Role table has a new role as singer */

/* Question 1 */
WITH SINGER_INFO AS (SELECT PictureID, PersonID FROM ROLE WHERE Role = 'Singer' AND IsMovie = True),
     OSCAR_WINNERS AS (SELECT PictureID FROM AWARDS WHERE Winner = True AND AwardOrganization = 'oscar'),
     SINGERS_IN_AWARDEES AS (SELECT DISTINCT * FROM SINGER_INFO AS SI INNER JOIN OSCAR_WINNERS AS OW ON SI.PictureID = OW.PictureID)
     SELECT RESULT2.PersonName AS PersonName, RESULT1.counters as MovieCount FROM
            (SELECT SIA.PersonID, count(*) AS counters FROM SINGERS_IN_AWARDEES AS SIA GROUP BY SIA.PersonID) AS RESULT1
             INNER JOIN
            (SELECT PersonName, PersonID FROM PERSON) AS RESULT2
             ON RESULT1.PersonID = RESULT2.PersonID;
             
/* Question 2 */
WITH DIRO_INFO AS (SELECT PictureID, PersonID FROM ROLE WHERE Role = 'Director' AND IsMovie = True),
     BAD_MOVIES AS (SELECT PictureID FROM RATING WHERE averageRating < 5),
     DIRO_FOR_BAD_MOVIES AS (SELECT DISTINCT * FROM DIRO_INFO AS DI INNER JOIN BAD_MOVIES AS BM ON DI.PictureID = BM.PictureID)
     SELECT RESULT2.PersonName AS Director, RESULT1.counters as BadMoviesDirected FROM 
            (SELECT DFBM.PersonID, count(*) AS counters FROM DIRO_FOR_BAD_MOVIES AS DFBM GROUP BY DFBM.PersonID) AS RESULT1
             INNER JOIN
            (SELECT PersonName, PersonID FROM PERSON) AS RESULT2
             ON RESULT1.PersonID = RESULT2.PersonID;

/* Question 3 */
WITH DIRO_INFO AS (SELECT PictureID, PersonID FROM ROLE WHERE Role = 'Director' AND IsMovie = True),
     MOVIE_INFO AS (SELECT PictureID, averageRating FROM RATING),
     DIRO_MOVIE_RATINGS AS (SELECT DISTINCT * FROM DIRO_INFO AS DI INNER JOIN MOVIE_INFO AS MI ON DI.PictureID = MI.PictureID)
     SELECT RESULT2.PersonName AS RatingBestDirector, RESULT1.avg_of_avg AS AvgOfAvgRating FROM
            (SELECT DMR.PersonID, avg(DMR.averageRating) AS avg_of_avg FROM
                DIRO_MOVIE_RATINGS AS DMR GROUP BY DMR.PersonID ORDER BY avg_of_avg DESC LIMIT 1) AS RESULT1
                INNER JOIN
            (SELECT PersonName, PersonID FROM PERSON) AS RESULT2
             ON RESULT1.PersonID = RESULT2.PersonID;

/* Question 4 */
WITH MOVIES AS (SELECT * FROM PICTURE WHERE IsMovie = True)
    SELECT PrimaryTitle, StartYear as Year, Duration FROM
    MOVIES WHERE (StartYear, Duration) IN
        (
        SELECT StartYear, min(Duration) FROM
            MOVIES GROUP BY StartYear
        ) ORDER BY StartYear;

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
        SELECT Genre, MAX(Duration) FROM
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

/* Question 9 */
/* Assumption: Interpretation of award winning actor as an actor who has won any award for movies */
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

/* QUESTION 10 (Syntax Error till now, working on it*/

/* Assuming new table: director_experience
     personid, mentorid, start year , end year //calculate duration as default value link in group
-> assume asst.director in role table
*/
WITH EXPERIENCE AS ( SELECT PersonID,StartYear,EndYear FROM DIRECTOR_EXPERIENCE WHERE endYear-startYear > 5),
    ROLES_ASSTDIR AS (SELECT * FROM ROLE WHERE Role = 'asst.director'),
    OSCAR_WINNER_MOVIE AS (SELECT pictureid,year FROM AWARDS WHERE AwardOrganization = 'Oscar' AND IsMovie = True)
    SELECT  RESULT2.PersonName FROM
        (
        SELECT FROM
            (
                (SELECT * FROM ROLES_ASSTDIR) AS ROLET
                INNER JOIN
                (SELECT * FROM OSCAR_WINNER_MOVIE) AS   OSCART
                ON
                ROLET.pictureID = OSCAR.pictureID
            ) AS F
            INNER JOIN
            (SELECT * FROM EXPERIENCE) AS RESULTINTER
            ON
            RESULTINTER.PersonID = F.PersonID
            WHERE
            RESULTINTER.startYear <= F.year
            AND
            RESULTINTER.endYear >= F.year           
        ) AS RESULT1
        INNER JOIN
        (
        SELECT PersonName,PersonID FROM PERSON
        ) AS RESULT2
        ON
        RESULT1.PersonID = RESULT2.PersonID;


/* Question 11 */
/* Assume role table has rows for singer as a role  */
WITH AWARD_WINNING_SINGERS AS (SELECT A.PersonID,A.Year FROM
        (SELECT Year, PersonID FROM AWARDS WHERE LOWER(AwardOrganization) = 'grammy' AND Winner = True AND Year IS NOT NULL) AS A
        INNER JOIN 
        (SELECT PersonID FROM ROLE WHERE Role = 'Singer') AS B
        ON
        A.PersonID = B.PersonID)

    SELECT E.PersonName, E.Year-E.BirthYear AS age_when_won_grammy
    FROM (
        AWARD_WINNING_SINGERS
        INNER JOIN
        (SELECT  PersonID, PersonName, BirthYear FROM PERSON WHERE BirthYear IS NOT NULL) AS C
        ON AWARD_WINNING_SINGERS.PersonID = C.PersonID
        ) AS E
    ORDER BY (E.Year - E.BirthYear) ASC
    LIMIT 1

/* Question 12 */
WITH GRAMMY_WINNERS AS (
                        SELECT A.PersonID, A.Year FROM
                        (SELECT PersonID, Year FROM
                         AWARDS WHERE Winner = True AND AwardOrganization = 'grammy') AS A
                         INNER JOIN
                        (SELECT DISTINCT PersonID FROM
                         ROLE WHERE Role = 'Singer') AS B
                         ON A.PersonID = B.PersonID)
     SELECT DISTINCT P.PersonName, GW.Year FROM (GRAMMY_WINNERS AS GW INNER JOIN PERSON AS P ON GW.PersonID = P.PersonID) ORDER BY GW.Year;

/* Question 13 */
WITH MOVIES AS (SELECT * FROM PICTURE WHERE IsMovie = True),
     MIN_GROSS_BOX AS ( SELECT StartYear, min(GrossBoxOffice) GrossBoxOffice FROM MOVIES
        GROUP BY StartYear ORDER BY StartYear),
     MAX_GROSS_BOX AS ( SELECT StartYear, max(GrossBoxOffice) GrossBoxOffice FROM MOVIES
        GROUP BY StartYear ORDER BY StartYear)

    SELECT A.StartYear, A.PrimaryTitle AS Movie_With_Miniumum_Gross, A.GrossBoxOffice AS Miniumum_Gross, B.PrimaryTitle AS Movie_With_Maxiumum_Gross, B.GrossBoxOffice AS Maxiumum_Gross, B.GrossBoxOffice - A.GrossBoxOffice AS Difference FROM (
    (SELECT StartYear, PrimaryTitle, GrossBoxOffice FROM
    MOVIES WHERE (StartYear, GrossBoxOffice) IN (SELECT * FROM MIN_GROSS_BOX) ORDER BY StartYear) AS A
    INNER JOIN
    (SELECT StartYear, PrimaryTitle, GrossBoxOffice FROM
    MOVIES WHERE (StartYear, GrossBoxOffice) IN (SELECT * FROM MAX_GROSS_BOX) ORDER BY StartYear) AS B
    ON A.StartYear = B.StartYear
    )

/* Question 16 */
WITH ACTORS AS (SELECT PersonID, IsMovie FROM ROLE WHERE Role = 'Actor'),
     MOVIE_ACTORS AS (SELECT DISTINCT PersonID FROM ACTORS WHERE IsMovie = True),
     TV_ACTORS AS (SELECT DISTINCT PersonID FROM ACTORS WHERE IsMovie = False)
     SELECT P.PersonName FROM
            PERSON AS P
            INNER JOIN
            ((SELECT PersonID FROM MOVIE_ACTORS) INTERSECT (SELECT PersonID FROM TV_ACTORS)) AS COMMONERS
            ON P.PersonID = COMMONERS.PersonID;


/* Question 17 */
WITH DIRO_INFO AS (SELECT PersonID, PictureID FROM ROLE WHERE IsMovie = True AND Role = 'Director'),
     MOVIES_2MIL AS (SELECT PictureID, PrimaryTitle, GrossBoxOffice FROM PICTURE WHERE IsMovie = True AND GrossBoxOffice >= 2000000),
     MOVIES_WITH_GENRES AS (SELECT M2M.PictureID, M2M.PrimaryTitle, M2M.GrossBoxOffice, G.Genre FROM
                                   MOVIES_2MIL AS M2M INNER JOIN GENRES AS G ON M2M.PictureID = G.PictureID),
     DIRO_FOR_M2M AS (SELECT DI.PersonID, DI.PictureID FROM DIRO_INFO AS DI INNER JOIN MOVIES_2MIL AS M2M ON M2M.PictureID = DI.PictureID)
     SELECT P.PersonName AS director, MWG.PrimaryTitle AS primarytitle, MWG.Genre AS genre, MWG.GrossBoxOffice FROM
            MOVIES_WITH_GENRES AS MWG
            INNER JOIN DIRO_FOR_M2M AS DFM
            ON MWG.PictureID = DFM.PictureID
            INNER JOIN PERSON AS P
            ON P.PersonID = DFM.PersonID
            ORDER BY genre;


/* Question 19 */
/* Assume Role table has role has actress */
WITH PEOPLE AS (SELECT PersonName, T1.PersonID, PictureID, Role FROM ((SELECT PictureID, PersonID, Role FROM ROLE WHERE IsMovie = True) AS T1 INNER JOIN
                               (SELECT PersonName,PersonID FROM PERSON) AS T2 ON T1.PersonID = T2.PersonID)
                ),
     ACTOR AS (SELECT * FROM PEOPLE WHERE Role = 'Actor'),
     ACTRESS AS (SELECT * FROM PEOPLE WHERE Role = 'Actress'),
     DIRECTOR AS (SELECT * FROM PEOPLE WHERE Role = 'Director')

SELECT A.PersonName AS actor_name, B.PersonName AS actress_name, C.PersonName AS director_name FROM (
    (ACTOR AS A INNER JOIN ACTRESS AS B ON A.PictureID = B.PictureID)
    INNER JOIN DIRECTOR AS C ON A.PictureID = C.PictureID
    )
GROUP BY (A.PersonID, A.PersonName, B.PersonID, B.PersonName, C.PersonID, C.PersonName)
HAVING COUNT(*) > 3;
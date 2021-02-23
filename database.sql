DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS movies;


CREATE TABLE movies (
    movieId SERIAL PRIMARY KEY,
    title VARCHAR(200),
    genres VARCHAR(200)
);


CREATE TABLE ratings (
    userId INTEGER,
    movieId INTEGER,
    rating FLOAT,
    timestamp INTEGER,
    FOREIGN KEY (movieId) REFERENCES movies (movieId) ON DELETE CASCADE
);



COPY movies (
    movieId SERIAL PRIMARY KEY,
    title VARCHAR(200),
    genres VARCHAR(200)
)
FROM 'data/movies.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;


COPY ratings (
    userId INTEGER,
    movieId INTEGER,
    rating FLOAT,
    timestamp INTEGER,
    FOREIGN KEY (movieId) REFERENCES movies (movieId) ON DELETE CASCADE
)
FROM 'data/ratings.csv'
DELIMITER ','
NULL AS 'NULL'
CSV HEADER;

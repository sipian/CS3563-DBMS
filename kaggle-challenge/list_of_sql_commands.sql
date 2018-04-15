create database Friendship;
\connect Friendship

create table Ratings (
	UserID integer primary key,
	ProfileID integer,
	Rating integer
);

create table Gender (
	UserID integer primary key,
	Gender char(1)
);

COPY person FROM '/tmp/train_user_ratings.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY person FROM '/tmp/gender.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

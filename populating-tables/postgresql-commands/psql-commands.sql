drop database gp2_db;
create database gp2_db;
\connect gp2_db

create table person ( 
	PersonID char(9) primary key,
	PersonName varchar NOT NULL,
	BirthYear real CHECK (BirthYear >= 0),
	DeathYear real CHECK (DeathYear >= 0)
);

create table picture (
	PictureID char(9) primary key,
	IsMovie bool DEFAULT TRUE,
	PrimaryTitle varchar,
	ReleaseTitle varchar ,
	Adult bool DEFAULT FALSE,
	StartYear real CHECK (StartYear >= 0),
	EndYear  real CHECK (EndYear >= 0),
	Duration real CHECK(Duration >= 0),
	Budget real CHECK(Budget >= 0),
	GrossBoxOffice real CHECK(GrossBoxOffice >= 0),
	ParentPicture char(9) references picture(PictureID),
	SeasonNumber real CHECK(SeasonNumber >= 0),
	EpisodeNumber real CHECK(EpisodeNumber >= 0)
);

create table role (
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE,
	PersonID char(9) references person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE,
	Role varchar(15) DEFAULT 'Miscellaneous',
    IsMovie bool DEFAULT FALSE
);

create table awards(
	AwardID varchar(25) NOT NULL,
	AwardName varchar NOT NULL, 
	AwardOrganization varchar NOT NULL, 
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE, 
	PersonID char(9) references person(PersonID) ON DELETE CASCADE ON UPDATE CASCADE, 
	Winner bool DEFAULT FALSE, 
	Year int CHECK(Year >= 0)
);

create table languages ( 
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE, 
	Language varchar(75) DEFAULT 'English'
);

create table production_company ( 
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE,
	CompanyName varchar NOT NULL,
	CompanyID int CHECK(CompanyID >= 0)
);

create table filming_location (
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE,
	CountryName varchar(75) NOT NULL
);

create table release_location (
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE,
	CountryName varchar(75) NOT NULL
);

create table genres (
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE,
	Genre varchar
);

create table rating (
	PictureID char(9) references picture(PictureID) ON DELETE CASCADE ON UPDATE CASCADE,
	averageRating real DEFAULT 0.0,
	numVotes int DEFAULT 0
);


COPY person FROM '/tmp/person.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY picture FROM '/tmp/pictures.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY awards FROM '/tmp/awards.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY languages FROM '/tmp/languages.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY production_company FROM '/tmp/production_comp.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY filming_location FROM '/tmp/filming_location.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY release_location FROM '/tmp/release_location.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY genres FROM '/tmp/genre.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY rating FROM '/tmp/ratings.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

COPY role FROM '/tmp/role.csv' CSV delimiter ',' NULL '\N' ENCODING 'unicode' header;

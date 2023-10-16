-- Créez le schéma "ent"
CREATE SCHEMA ent;

-- Définissez le schéma "ent" comme schéma par défaut
SET search_path TO ent;

CREATE TABLE Users(
    id SERIAL,
    username VARCHAR(32),
    password VARCHAR(200),
    type VARCHAR(32),
    last_name VARCHAR(32),
    first_name VARCHAR(32),
    email VARCHAR(32),
    admin BOOLEAN,
    PRIMARY KEY(id)

);

CREATE TABLE Teachers(
    id SERIAL,
    initital VARCHAR(32),
    desktop VARCHAR(32),
    timetable_manager BOOLEAN,
    id_User BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_User) REFERENCES Users(id)
);

CREATE TABLE Trainings(
    id SERIAL,
    name VARCHAR(32),
    PRIMARY KEY(id)
);

CREATE TABLE Resources(
    id SERIAL,
    name VARCHAR(32),
    PRIMARY KEY(id)
);

CREATE TABLE Promotions(
  	id SERIAL,
  	year INTEGER,
  	id_Training BIGINT,
	PRIMARY KEY(id),
  	FOREIGN KEY(id_Training) REFERENCES Trainings(id)
);

CREATE TABLE TD(
   	id SERIAL,
  	name VARCHAR(32),
   	id_Promotion BIGINT,
  	PRIMARY KEY(id),
  	FOREIGN KEY(id_Promotion) REFERENCES Promotions(id)
  
);

CREATE TABLE TP(
    id SERIAL,
    name VARCHAR(32),
    id_Td BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_Td) REFERENCES TD(id)
);

CREATE TABLE Courses(
    id SERIAL,
    startTime TIME,
    endTime TIME,
    dateCourse DATE,
    control BOOLEAN,
    id_Resource BIGINT,
    id_Tp BIGINT UNIQUE,
    id_Td BIGINT UNIQUE,
    id_Promotion BIGINT UNIQUE,
    id_Teacher BIGINT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_Resource) REFERENCES Resources(id),
    FOREIGN KEY (id_Tp) REFERENCES TP(id),
    FOREIGN KEY (id_Td) REFERENCES TD(id),
    FOREIGN KEY (id_Promotion) REFERENCES Promotions(id),
    FOREIGN KEY (id_Teacher) REFERENCES Teachers(id)
);

CREATE TABLE Degrees(
    id SERIAL,
    name VARCHAR(32),
    id_Training BIGINT, 
    PRIMARY KEY (id),
    FOREIGN KEY (id_Training) REFERENCES Trainings(id)
);

CREATE TABLE Students(
    id SERIAL,
    apprentice BOOLEAN,
    id_User BIGINT,
    id_Td  BIGINT,
    id_Tp  BIGINT,
    id_Promotion BIGINT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_User) REFERENCES Users(id),
    FOREIGN KEY (id_Td) REFERENCES TD(id),
    FOREIGN KEY (id_Tp) REFERENCES TP(id),
    FOREIGN KEY (id_Promotion) REFERENCES Promotions(id)
);

CREATE TABLE Classroom(
    id SERIAL,
    name VARCHAR(32),
    capacity INTEGER,
    equipment VARCHAR(32),
    id_Course BIGINT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_Course) REFERENCES Courses(id)
   
);

CREATE TABLE Absences(
    id_Student BIGINT,
    id_Course BIGINT,
    reason VARCHAR(32),
    justify BOOLEAN,
    PRIMARY KEY (id_Student, id_Course),
    FOREIGN KEY (id_Student) REFERENCES Students(id),
    FOREIGN KEY (id_Course) REFERENCES Courses(id)
);

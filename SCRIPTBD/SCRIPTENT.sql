drop schema if exists ent cascade;
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
    PRIMARY KEY(id)
);

CREATE TABLE Admin (
    id SERIAL ,
    id_User BIGINT, 
    PRIMARY KEY(id),
    FOREIGN KEY (id_User) REFERENCES Users(id) 
);

CREATE TABLE Teachers(
    id SERIAL,
    initital VARCHAR(32),
    desktop VARCHAR(32),
    timetable_manager BOOLEAN,
    id_User BIGINT ,
    PRIMARY KEY(id),
    FOREIGN KEY(id_User) REFERENCES Users(id)
);

CREATE TABLE Degrees(
    id SERIAL,
    name VARCHAR(32),
    PRIMARY KEY(id)
)

CREATE TABLE Trainings(
    id SERIAL,
    name VARCHAR(32),
    id_Degree BIGINT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_Degree) REFERENCES Degrees(id),
    UNIQUE (id_Degree, name)  -- This enforces the uniqueness of the combination
);


CREATE TABLE Promotions(
    id SERIAL,
    year INTEGER,
    id_Degree BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_Degree) REFERENCES Degrees(id),
    CONSTRAINT unique_year_degree_combination UNIQUE (year, id_Degree)
);


CREATE TABLE Resources(
    id SERIAL,
    name VARCHAR(32),
    id_Promotion BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_Promotion) REFERENCES Promotions(id)
);

CREATE TABLE TD(
    id SERIAL,
    name VARCHAR(32),
    id_Promotion BIGINT,
    id_Training BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_Promotion) REFERENCES Promotions(id),
    FOREIGN KEY(id_Training) REFERENCES Trainings(id),
    CONSTRAINT unique_name_promotion_combination UNIQUE (name, id_Promotion)
);


CREATE TABLE TP(
    id SERIAL,
    name VARCHAR(32),
    id_Td BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(id_Td) REFERENCES TD(id),
    CONSTRAINT unique_name_td_combination UNIQUE (name, id_Td)
);

CREATE TABLE Materials(
    id SERIAL,
    equipment VARCHAR(100),
    quantity INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE Classroom(
    id SERIAL,
    name VARCHAR(32),
    capacity INTEGER,
    id_Material BIGINT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_Material) REFERENCES Materials(id)
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
    id_classroom BIGINT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_classroom) REFERENCES Classroom(id),
    FOREIGN KEY (id_Resource) REFERENCES Resources(id),
    FOREIGN KEY (id_Tp) REFERENCES TP(id),
    FOREIGN KEY (id_Td) REFERENCES TD(id),
    FOREIGN KEY (id_Promotion) REFERENCES Promotions(id),
    FOREIGN KEY (id_Teacher) REFERENCES Teachers(id)
);


CREATE TABLE Students (
    id SERIAL,
    apprentice BOOLEAN,
    id_User BIGINT,
    id_Td BIGINT,
    id_Tp BIGINT,
    id_Promotion BIGINT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_User) REFERENCES Users (id),
    FOREIGN KEY (id_Td) REFERENCES TD (id) ON DELETE SET NULL,
    FOREIGN KEY (id_Tp) REFERENCES TP (id) ON DELETE SET NULL,
    FOREIGN KEY (id_Promotion) REFERENCES Promotions (id) ON DELETE SET NULL
);



CREATE TABLE Absences(
    id_Student BIGINT ,
    id_Course BIGINT ,
    reason VARCHAR(32),
    justify BOOLEAN,
    PRIMARY KEY (id_Student, id_Course),
    FOREIGN KEY (id_Student) REFERENCES Students(id),
    FOREIGN KEY (id_Course) REFERENCES Courses(id)
);

CREATE TABLE Historique(
    id SERIAL,
    id_User BIGINT,
    modification VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY (id_User) REFERENCES Users(id)
)


drop schema if exists ent cascade;
-- Créez le schéma "ent"
CREATE SCHEMA ent;

-- Définissez le schéma "ent" comme schéma par défaut
SET search_path TO ent;

CREATE TABLE Roles(
    id SERIAL,
    name VARCHAR(32),
    PRIMARY KEY (id)
);

CREATE TABLE Users(
    id SERIAL,
    username VARCHAR(32),
    password VARCHAR(200),
    last_name VARCHAR(32),
    first_name VARCHAR(32),
    email VARCHAR(32),
    id_Role BIGINT,
    PRIMARY KEY(id),
    isAdmin BOOLEAN,
    FOREIGN KEY(id_Role) REFERENCES Roles(id)
);

CREATE TABLE Teachers(
    id SERIAL,
    initial VARCHAR(32),
    desktop VARCHAR(32),
    id_User BIGINT ,
    PRIMARY KEY(id),
    FOREIGN KEY (id_User) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Degrees(
    id SERIAL,
    name VARCHAR(32),
    PRIMARY KEY(id)
);

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
    level INTEGER CHECK (level >= 1 AND level <= 3),
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
    PRIMARY KEY (id)
);

CREATE TABLE Classroom(
    id SERIAL,
    name VARCHAR(32),
    capacity INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE CONTAINS (
    id_materials BIGINT,
    id_classroom BIGINT,
    quantity INTEGER,
    PRIMARY KEY (id_materials, id_classroom),
    FOREIGN KEY (id_materials) REFERENCES Materials(id),
    FOREIGN KEY (id_classroom) REFERENCES Classroom(id),
    UNIQUE (id_materials, id_classroom)
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
    ine VARCHAR(32),
    nip VARCHAR(32),
    id_User BIGINT ,
    id_Td  BIGINT ,
    id_Tp  BIGINT ,
    id_Promotion BIGINT ,
    PRIMARY KEY (id),
    FOREIGN KEY (id_User) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_Td) REFERENCES TD(id),
    FOREIGN KEY (id_Tp) REFERENCES TP(id),
    FOREIGN KEY (id_Promotion) REFERENCES Promotions(id)
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

CREATE TABLE Logs(
    id SERIAL,
    id_User BIGINT,
    modification VARCHAR(100),
    modification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_User) REFERENCES Users(id)
);


-- Insertion des rôles
INSERT INTO Roles (name) VALUES ('admin');
INSERT INTO Roles (name) VALUES ('user');
INSERT INTO Roles (name) VALUES ('student');
INSERT INTO Roles (name) VALUES ('teacher');

-- Insertion des degrés
INSERT INTO Degrees (name) VALUES ('INFO');
INSERT INTO Degrees (name) VALUES ('GAGO');
INSERT INTO Degrees (name) VALUES ('CLIO');
INSERT INTO Degrees (name) VALUES ('INFOCOM');

-- Insertion des utilisateurs
INSERT INTO Users (username, password, last_name, first_name, email, isAdmin, id_Role) VALUES ('admin', 'password', 'Admin', 'Admin', 'admin@example.com', true, 1);
INSERT INTO Users (username, password, last_name, first_name, email, isAdmin, id_Role) VALUES ('user', 'password', 'User', 'User', 'user@example.com', false, 2);

-- Insertion des enseignants
INSERT INTO Teachers (initial, desktop, id_User) VALUES ('T1', 'Desk1', 1);
INSERT INTO Teachers (initial, desktop, id_User) VALUES ('T2', 'Desk2', 2);

-- Insertion des formations
INSERT INTO Trainings (name, id_Degree) VALUES ('Formation1', 1);
INSERT INTO Trainings (name, id_Degree) VALUES ('Formation2', 2);

-- Insertion des promotions
INSERT INTO Promotions (year, level, id_Degree) VALUES (2023, 1, 1);
INSERT INTO Promotions (year, level, id_Degree) VALUES (2022, 2, 2);

-- Insertion des ressources
INSERT INTO Resources (name, id_Promotion) VALUES ('Ressource1', 1);
INSERT INTO Resources (name, id_Promotion) VALUES ('Ressource2', 2);

-- Insertion des TD
INSERT INTO TD (name, id_Promotion, id_Training) VALUES ('TD1', 1, 1);
INSERT INTO TD (name, id_Promotion, id_Training) VALUES ('TD2', 2, 2);

-- Insertion des TP
INSERT INTO TP (name, id_Td) VALUES ('TP1', 1);
INSERT INTO TP (name, id_Td) VALUES ('TP2', 2);

-- Insertion des matériaux
INSERT INTO Materials (equipment) VALUES ('Ordinateur portable');
INSERT INTO Materials (equipment) VALUES ('Tableau blanc');

-- Insertion des classes
INSERT INTO Classroom (name, capacity) VALUES ('Salle1', 30);
INSERT INTO Classroom (name, capacity) VALUES ('Salle2', 40);

-- Insertion des cours
INSERT INTO Courses (startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom) VALUES ('08:00:00', '10:00:00', '2023-11-15', true, 1, 1, 1, 1, 1, 1);
INSERT INTO Courses (startTime, endTime, dateCourse, control, id_Resource, id_Tp, id_Td, id_Promotion, id_Teacher, id_classroom) VALUES ('10:30:00', '12:30:00', '2023-11-15', true, 2, 2, 2, 2, 2, 2);

-- Insertion des étudiants
INSERT INTO Students (nip, ine, apprentice, id_User, id_Td, id_Tp, id_Promotion) VALUES (123456,789455, true, 2, 1, 1, 1);
INSERT INTO Students (nip, ine, apprentice, id_User, id_Td, id_Tp, id_Promotion) VALUES (789123,123456, false, 1, 2, 2, 2);

-- Insertion des absences
INSERT INTO Absences (id_Student, id_Course, reason, justify) VALUES (1, 1, 'Malade', false);
INSERT INTO Absences (id_Student, id_Course, reason, justify) VALUES (2, 2, 'Raison personnelle', true);

-- Insertion des logs
INSERT INTO Logs (id_User, modification) VALUES (1, 'Modification 1');
INSERT INTO Logs (id_User, modification) VALUES (2, 'Modification 2');



-- Création du déclencheur
CREATE OR REPLACE FUNCTION delete_absences_on_student_delete()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM ent.Absences WHERE id_Student = OLD.id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER delete_absences_trigger
BEFORE DELETE ON ent.Students
FOR EACH ROW
EXECUTE FUNCTION delete_absences_on_student_delete();

CREATE OR REPLACE FUNCTION delete_courses_on_teacher_delete()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM ent.Courses WHERE id_Teacher = OLD.id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER delete_courses_trigger
BEFORE DELETE ON ent.Teachers
FOR EACH ROW
EXECUTE FUNCTION delete_courses_on_teacher_delete();

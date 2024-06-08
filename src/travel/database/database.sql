DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Concelho;
DROP TABLE IF EXISTS Province;
DROP TABLE IF EXISTS Municipio;
DROP TABLE IF EXISTS LocationPortugal;
DROP TABLE IF EXISTS LocationSpain;
DROP TABLE IF EXISTS LocationGibraltar;
DROP TABLE IF EXISTS Connection;
DROP TABLE IF EXISTS Destination;

CREATE TABLE Location(
    name TEXT NOT NULL UNIQUE,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    altitude INTEGER NOT NULL,
    protected_area TEXT,
    island TEXT,
    batch INTEGER NOT NULL,
    PRIMARY KEY (name)
);

CREATE TABLE Concelho(
    concelho TEXT NOT NULL UNIQUE,
    intermunicipal_entity TEXT NOT NULL,
    district TEXT NOT NULL,
    region TEXT NOT NULL,
    PRIMARY KEY (concelho)
);

CREATE TABLE Province(
    province TEXT NOT NULL UNIQUE,
    autonomous_community TEXT NOT NULL,
    PRIMARY KEY (province)
);

CREATE TABLE Municipio(
    municipio TEXT NOT NULL,
    comarca TEXT NOT NULL,
    province TEXT NOT NULL,
    PRIMARY KEY (municipio, province),
    FOREIGN KEY (province) REFERENCES Province(province) ON DELETE CASCADE
);

CREATE TABLE LocationPortugal(
    name TEXT NOT NULL UNIQUE,
    parish TEXT NOT NULL,
    concelho TEXT NOT NULL,
    PRIMARY KEY (name),
    FOREIGN KEY (name) REFERENCES Location(name) ON DELETE CASCADE,
    FOREIGN KEY (concelho) REFERENCES Concelho(concelho) ON DELETE CASCADE
);

CREATE TABLE LocationSpain(
    name TEXT NOT NULL UNIQUE,
    municipio TEXT NOT NULL,
    province TEXT NOT NULL,
    district TEXT,
    PRIMARY KEY (name),
    FOREIGN KEY (name) REFERENCES Location(name) ON DELETE CASCADE,
    FOREIGN KEY (municipio, province) REFERENCES Municipio(municipio, province) ON DELETE CASCADE
);

CREATE TABLE LocationGibraltar(
    name TEXT NOT NULL,
    PRIMARY KEY (name),
    FOREIGN KEY (name) REFERENCES Location(name) ON DELETE CASCADE
);

CREATE TABLE Connection(
    location_a TEXT NOT NULL,
    location_b TEXT NOT NULL,
    means_transport TEXT NOT NULL,
    distance REAL NOT NULL,
    way TEXT,
    cardinal_point TEXT NOT NULL,
    order_a INTEGER NOT NULL,
    order_b INTEGER NOT NULL,
    PRIMARY KEY (location_a, location_b, means_transport),
    FOREIGN KEY (location_a) REFERENCES Location(name) ON DELETE CASCADE,
    FOREIGN KEY (location_b) REFERENCES Location(name) ON DELETE CASCADE
);

CREATE TABLE Destination(
    location_a TEXT NOT NULL,
    location_b TEXT NOT NULL,
    means_transport TEXT NOT NULL,
    starting_point INTEGER NOT NULL,
    destination TEXT NOT NULL,
    PRIMARY KEY (location_a, location_b, means_transport, starting_point, destination),
    FOREIGN KEY (location_a, location_b, means_transport) REFERENCES Connection(location_a, location_b, means_transport) ON DELETE CASCADE
);
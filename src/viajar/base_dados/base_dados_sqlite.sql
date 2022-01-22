DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS concelho;
DROP TABLE IF EXISTS province;
DROP TABLE IF EXISTS municipio;
DROP TABLE IF EXISTS location_portugal;
DROP TABLE IF EXISTS location_spain;
DROP TABLE IF EXISTS location_gibraltar;
DROP TABLE IF EXISTS comarca;
DROP TABLE IF EXISTS connection;
DROP TABLE IF EXISTS destination;

CREATE TABLE Location(
    name TEXT NOT NULL UNIQUE,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    altitude INTEGER NOT NULL,
    extra_info TEXT,
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
    province TEXT NOT NULL,
    PRIMARY KEY (municipio, province),
    FOREIGN KEY (province) references Province(province)
);

CREATE TABLE LocationPortugal(
    name TEXT NOT NULL UNIQUE,
    parish TEXT NOT NULL,
    concelho TEXT NOT NULL,
    PRIMARY KEY (name),
    FOREIGN KEY (name) references Location(name),
    FOREIGN KEY (concelho) references Concelho(concelho)
);

CREATE TABLE LocationSpain(
    name TEXT NOT NULL UNIQUE,
    municipio TEXT NOT NULL,
    province TEXT NOT NULL,
    district TEXT,
    PRIMARY KEY (name),
    FOREIGN KEY (name) references Location(name),
    FOREIGN KEY (municipio, province) references Municipio(municipio, province)
);

CREATE TABLE LocationGibraltar(
    name TEXT NOT NULL,
    major_residential_area TEXT NOT NULL,
    PRIMARY KEY (name, major_residential_area),
    FOREIGN KEY (name) references Location(name)
);

CREATE TABLE Comarca(
    municipio TEXT NOT NULL,
    comarca TEXT NOT NULL,
    province TEXT NOT NULL,
    PRIMARY KEY (comarca, municipio, province),
    FOREIGN KEY (municipio, province) references Municipio(municipio, province)
);

CREATE TABLE Connection(
    location_a TEXT NOT NULL,
    location_b TEXT NOT NULL,
    means_transport TEXT NOT NULL,
    distance REAL NOT NULL,
    extra_info TEXT,
    cardinal_point TEXT NOT NULL,
    order_a INTEGER NOT NULL,
    order_b INTEGER NOT NULL,
    PRIMARY KEY (location_a, location_b, means_transport),
    FOREIGN KEY (location_a) references Location(name),
    FOREIGN KEY (location_b) references Location(name)
);

CREATE TABLE Destination(
    location_a TEXT NOT NULL,
    location_b TEXT NOT NULL,
    means_transport TEXT NOT NULL,
    starting_point INTEGER NOT NULL,
    destination TEXT NOT NULL,
    PRIMARY KEY (location_a, location_b, means_transport, starting_point, destination),
    FOREIGN KEY (location_a, location_b, means_transport) references Connection(location_a, location_b, means_transport)
);
DROP TABLE IF EXISTS local cascade;
DROP TABLE IF EXISTS local_portugal cascade;
DROP TABLE IF EXISTS local_espanha cascade;
DROP TABLE IF EXISTS concelho cascade;
DROP TABLE IF EXISTS comarca cascade;
DROP TABLE IF EXISTS provincia cascade;
DROP TABLE IF EXISTS local_concelho cascade;
DROP TABLE IF EXISTS local_comarca cascade;
DROP TABLE IF EXISTS local_provincia cascade;
DROP TABLE IF EXISTS ligacao cascade;
DROP TABLE IF EXISTS destino cascade;

CREATE TABLE local(
    nome char(100) NOT NULL UNIQUE,
    latitude numeric NOT NULL,
    longitude numeric NOT NULL,
    altitude integer NOT NULL,
    info_extra char(200),
    PRIMARY KEY (nome)
);

CREATE TABLE local_portugal(
    nome char(100) NOT NULL UNIQUE,
    freguesia char(100) NOT NULL,
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local(nome) on delete cascade
);

CREATE TABLE local_espanha(
    nome char(100) NOT NULL UNIQUE,
    municipio char(100) NOT NULL,
    distrito char(100),
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local(nome) on delete cascade
);

CREATE TABLE concelho(
    concelho char(100) NOT NULL UNIQUE,
    entidade_intermunicipal char(100) NOT NULL,
    distrito char(100) NOT NULL,
    regiao char(100) NOT NULL,
    PRIMARY KEY (concelho)
);

CREATE TABLE comarca(
    comarca char(100) NOT NULL UNIQUE,
    PRIMARY KEY (comarca)
);

CREATE TABLE provincia(
    provincia char(100) NOT NULL UNIQUE,
    comunidade_autonoma char(100) NOT NULL,
    PRIMARY KEY (provincia)
);

CREATE TABLE local_concelho(
    nome char(100) NOT NULL UNIQUE,
    concelho char(100) NOT NULL,
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local_portugal(nome) on delete cascade,
    FOREIGN KEY (concelho) references concelho(concelho) on delete cascade
);

CREATE TABLE local_comarca(
    nome char(100) NOT NULL,
    comarca char(100) NOT NULL,
    PRIMARY KEY (nome, comarca),
    FOREIGN KEY (nome) references local_espanha(nome) on delete cascade,
    FOREIGN KEY (comarca) references comarca(comarca) on delete cascade
);

CREATE TABLE local_provincia(
    nome char(100) NOT NULL UNIQUE,
    provincia char(100) NOT NULL,
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local_espanha(nome) on delete cascade,
    FOREIGN KEY (provincia) references provincia(provincia) on delete cascade
);

CREATE TABLE ligacao(
    local_a char(100) NOT NULL,
    local_b char(100) NOT NULL,
    meio_transporte char(50) NOT NULL,
    distancia numeric NOT NULL,
    info_extra char(200),
    ponto_cardeal char(10) NOT NULL,
    ordem_a integer NOT NULL,
    ordem_b integer NOT NULL,
    PRIMARY KEY (local_a, local_b, meio_transporte),
    FOREIGN KEY (local_a) references local(nome) on delete cascade,
    FOREIGN KEY (local_b) references local(nome) on delete cascade
);

CREATE TABLE destino(
    origem char(100) NOT NULL,
    sentido char(100) NOT NULL,
    destino char(100) NOT NULL,
    local_a char(100) NOT NULL,
    local_b char(100) NOT NULL,
    meio_transporte char(100) NOT NULL,
    PRIMARY KEY (origem, sentido, destino),
    FOREIGN KEY (local_a, local_b, meio_transporte) references ligacao(local_a, local_b, meio_transporte) on delete cascade
);

COPY local(nome, latitude, longitude, altitude, info_extra)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\local.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY local_portugal(nome, freguesia)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\local_portugal.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY local_espanha(nome, municipio, distrito)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\local_espanha.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY concelho(concelho, entidade_intermunicipal, distrito, regiao)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\concelho.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY comarca(comarca)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\comarca.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY provincia(provincia, comunidade_autonoma)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\provincia.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY local_concelho(nome, concelho)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\local_concelho.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY local_comarca(nome, comarca)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\local_comarca.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY local_provincia(nome, provincia)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\local_provincia.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY ligacao(local_a, local_b, meio_transporte, distancia, info_extra, ponto_cardeal, ordem_a, ordem_b)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\ligacao.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';

COPY destino(origem, sentido, destino, local_a, local_b, meio_transporte)
FROM 'D:\PycharmProjects\Viajar\src\viajar\base_dados\destino.csv' DELIMITER ';' CSV HEADER ENCODING 'win1252';
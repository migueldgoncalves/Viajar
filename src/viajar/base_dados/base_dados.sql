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
    nome varchar NOT NULL UNIQUE,
    latitude numeric NOT NULL,
    longitude numeric NOT NULL,
    altitude integer NOT NULL,
    info_extra varchar,
    PRIMARY KEY (nome)
);

CREATE TABLE local_portugal(
    nome varchar NOT NULL UNIQUE,
    freguesia varchar NOT NULL,
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local(nome) on delete cascade
);

CREATE TABLE local_espanha(
    nome varchar NOT NULL UNIQUE,
    municipio varchar NOT NULL,
    distrito varchar,
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local(nome) on delete cascade
);

CREATE TABLE concelho(
    concelho varchar NOT NULL UNIQUE,
    entidade_intermunicipal varchar NOT NULL,
    distrito varchar NOT NULL,
    regiao varchar NOT NULL,
    PRIMARY KEY (concelho)
);

CREATE TABLE comarca(
    comarca varchar NOT NULL UNIQUE,
    PRIMARY KEY (comarca)
);

CREATE TABLE provincia(
    provincia varchar NOT NULL UNIQUE,
    comunidade_autonoma varchar NOT NULL,
    PRIMARY KEY (provincia)
);

CREATE TABLE local_concelho(
    nome varchar NOT NULL UNIQUE,
    concelho varchar NOT NULL,
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local_portugal(nome) on delete cascade,
    FOREIGN KEY (concelho) references concelho(concelho) on delete cascade
);

CREATE TABLE local_comarca(
    nome varchar NOT NULL,
    comarca varchar NOT NULL,
    PRIMARY KEY (nome, comarca),
    FOREIGN KEY (nome) references local_espanha(nome) on delete cascade,
    FOREIGN KEY (comarca) references comarca(comarca) on delete cascade
);

CREATE TABLE local_provincia(
    nome varchar NOT NULL UNIQUE,
    provincia varchar NOT NULL,
    PRIMARY KEY (nome),
    FOREIGN KEY (nome) references local_espanha(nome) on delete cascade,
    FOREIGN KEY (provincia) references provincia(provincia) on delete cascade
);

CREATE TABLE ligacao(
    local_a varchar NOT NULL,
    local_b varchar NOT NULL,
    meio_transporte varchar NOT NULL,
    distancia numeric NOT NULL,
    info_extra varchar,
    ponto_cardeal varchar NOT NULL,
    ordem_a integer NOT NULL,
    ordem_b integer NOT NULL,
    PRIMARY KEY (local_a, local_b, meio_transporte),
    FOREIGN KEY (local_a) references local(nome) on delete cascade,
    FOREIGN KEY (local_b) references local(nome) on delete cascade
);

CREATE TABLE destino(
    local_a varchar NOT NULL,
    local_b varchar NOT NULL,
    meio_transporte varchar NOT NULL,
    origem boolean NOT NULL,
    destino varchar NOT NULL,
    PRIMARY KEY (local_a, local_b, meio_transporte, origem, destino),
    FOREIGN KEY (local_a, local_b, meio_transporte) references ligacao(local_a, local_b, meio_transporte) on delete cascade
);
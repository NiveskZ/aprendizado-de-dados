CREATE DATABASE IF NOT EXISTS guia_tur
CHARSET utf8mb4;

USE guia_tur;

CREATE TABLE IF NOT EXISTS pais(
	ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    continente ENUM('Ásia','América','África', 'EUROPA'),
    codigo CHAR(3) NOT NULL
);

CREATE TABLE IF NOT EXISTS estado (
	id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL DEFAULT '',
    sigla CHAR(2) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS cidade (
	id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL DEFAULT '',
    populacao INT(11) NOT NULL DEFAULT '0'
);

CREATE TABLE IF NOT EXISTS ponto_tur (
	id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL DEFAULT '',
    populacao INT(11) NOT NULL DEFAULT '0',
    tipo ENUM('Atrativo','Serviço','Equipamento','Infraestrutura','Instituição','Organização'),
    publicado ENUM('Não', 'Sim') NOT NULL DEFAULT 'Não'
);

CREATE TABLE IF NOT EXISTS coordenada (
	latitude FLOAT(10,6),
    longitude FLOAT(10,6)
);

INSERT INTO pais(nome, continente, codigo)
VALUES
	('Brasil', 'América', 'BRA'),
    ('Índia','Ásia','IDN'),
    ('China','Ásia','CHI'),
    ('Japão','Ásia','JPN');
    
SELECT * FROM pais;

INSERT INTO estado (nome, sigla)
VALUES
	('Maranhão','MA'),
    ('São Paulo', 'SP'),
    ('Santa Catarina', 'SC'),
    ('Rio de Janeiro', 'RJ');
    
SELECT * FROM estado;


INSERT INTO cidade (nome, populacao)
VALUES
	('Sorocaba', 700000),
    ('Déli',26000000),
    ('Xangai',22000000),
    ('Tóquio',38000000); 
    
SELECT * FROM cidade;

INSERT INTO ponto_tur (nome, tipo)
VALUES 
	('Quinzinho de Barros', 'Instituição'),
    ('Parque Estadual do Jalapão', 'Atrativo'),
    ('Torre Eiffel', 'Atrativo'),
    ('Fogo de Chão', 'Serviço');

SELECT * FROM ponto_tur;
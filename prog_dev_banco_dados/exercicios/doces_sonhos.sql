CREATE DATABASE doce_sonhos;

USE doce_sonhos;

CREATE TABLE produtos (
	id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco INT NOT NULL,
    quantidade_estoque INT NOT NULL
);

CREATE TABLE ingredientes (
	id_ingrediente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    unidade VARCHAR(20) NOT NULL
);

CREATE TABLE composicao (
	id_produto INT NOT NULL,
    id_ingrediente INT NOT NULL,
    quantidade_usada DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_produto, id_ingrediente)
);

-- Criar a relação entre as tabelas PRODUTO e INGREDIENTES na tabela COMPOSIÇÃO,
-- id_produto e id_ingrediente as chaves estrangeiras das respectivas tabelas.

ALTER TABLE composicao
ADD CONSTRAINT FK_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto);

ALTER TABLE composicao
ADD CONSTRAINT FK_ingrediente
FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente);

-- Alterar a coluna "PRECO" da tabela "PRODUTOS" para permitir valores decimais com duas casas após a vírgula.

ALTER TABLE produtos
MODIFY preco DECIMAL(7,2) NOT NULL;

-- Adicionar uma nova coluna, "DATA_VALIDADE", à tabela "PRODUTOS" para registrar a data de validade de cada doce.
ALTER TABLE produtos
ADD data_validade DATE DEFAULT (CURRENT_DATE);

-- Excluir a coluna "DESCRICAO" da tabela "PRODUTOS", pois a empresa decidiu centralizar essas informações em outro sistema.

ALTER TABLE produtos
DROP COLUMN descricao;

-- Inserir os seguintes dados nas respectivas tabelas:
ALTER TABLE produtos
MODIFY data_validade DATE AFTER nome;

INSERT INTO produtos
VALUES 
	(0,'Brigadeiro','2024-09-28',5.00,100),
    (0,'Beijinho','2024-09-12',4.00,50),
    (0,'Pudim', '2024-09-20',10.00,20);

SELECT * FROM produtos;

INSERT INTO ingredientes(nome, quantidade, unidade)
VALUES
	('Chocolate',100,'g'),
    ('Leite condensado',395,'g'),
    ('Coco ralado',50,'g'),
    ('Leite',500, 'ml'),
    ('Ovos',3, 'unidade');

SELECT * FROM ingredientes;

SET @id_brigadeiro = (SELECT id_produto from produtos WHERE nome = 'Brigadeiro');
SET @id_beijinho = (SELECT id_produto from produtos WHERE nome = 'Beijinho');
SET @id_pudim = (SELECT id_produto from produtos WHERE nome = 'Pudim');

SET @id_chocolate = (SELECT id_ingrediente from ingredientes WHERE nome = 'Chocolate');
SET @id_condensado = (SELECT id_ingrediente from ingredientes WHERE nome = 'Leite Condensado');
SET @id_coco_ralado = (SELECT id_ingrediente from ingredientes WHERE nome = 'Coco ralado');
SET @id_leite = (SELECT id_ingrediente from ingredientes WHERE nome = 'Leite');
SET @id_ovos = (SELECT id_ingrediente from ingredientes WHERE nome = 'Ovos');

INSERT INTO composicao (id_produto, id_ingrediente, quantidade_usada)
VALUES
	(id_brigadeiro, id_chocolate, 100),
	(id_brigadeiro, id_condensado, 395),
	(id_beijinho, id_condensado, 395),
	(id_beijinho, id_coco_ralado, 50),
	(id_pudim, id_condensado, 395),
	(id_pudim, id_leite, 500),
	(id_pudim, id_ovos, 3);
    
SELECT * FROM composicao;
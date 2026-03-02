CREATE DATABASE loja_store;

USE loja_store;

CREATE TABLE IF NOT EXISTS produto(
	cod INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    categoria ENUM('eletrodomestico', 'brinquedo', 'informática', 'eletroportátil') NOT NULL,
    preco DECIMAL(7,2) NOT NULL,
    estoque INT DEFAULT 0
);

INSERT INTO produto
VALUES (0, 'boneca', 'brinquedo', 39.90, 10);

INSERT INTO produto(nome, categoria, preco)
VALUES ('carrinho', 'brinquedo', 59.90);

UPDATE produto
SET estoque = 20
WHERE cod = 3;

SELECT * FROM produto;


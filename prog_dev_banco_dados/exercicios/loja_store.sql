CREATE DATABASE loja_store;

USE loja_store;

CREATE TABLE IF NOT EXISTS produto(
	cod INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    categoria ENUM('eletrodomestico', 'brinquedo', 'informática', 'eletroportátil') NOT NULL,
    preco DECIMAL(7,2) NOT NULL,
    estoque INT DEFAULT 0
);

ALTER TABLE produto MODIFY preco DECIMAL(8,2) NOT NULL AFTER nome;
ALTER TABLE produto ADD marca VARCHAR(50) NOT NULL;

DESCRIBE produto;

INSERT INTO produto
VALUES (0, 'boneca', 'brinquedo', 39.90, 10);

INSERT INTO produto(nome, categoria, preco)
VALUES ('carrinho', 'brinquedo', 59.90);

UPDATE produto
SET estoque = 20
WHERE cod = 3;

SELECT * FROM produto;

CREATE TABLE IF NOT EXISTS pedido(
	pedido_id INT PRIMARY KEY AUTO_INCREMENT,
    cod_produto INT NOT NULL,
    quantidade INT NOT NULL,
    data_pedido DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (cod_produto) REFERENCES produto(cod)
);

INSERT INTO pedido(cod_produto,quantidade)
VALUES(3,5);

SELECT * FROM pedido;

CREATE TABLE clientes (
	id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    email VARCHAR(100)
);

ALTER TABLE pedido
ADD id_cliente INT,
ADD CONSTRAINT FK_cliente
FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente);

INSERT INTO clientes (nome, email)
VALUES
	('João SIlva', 'joao.silva@email.com'),
    ('Maria Oliveira', 'maria.oliveira@email.com'),
    ('Carlos Souza', 'carlos.souza@email.com'),
    ('Ana Lima', 'ana.lima@email.com');

INSERT INTO produto (nome, preco, marca)
VALUES
	('Camiseta', 29.99, 'Nike'),
    ('Calça Jeans', 79.99, 'Levis'),
    ('Tênis', 99.50, 'Asics'),
    ('Óculos de SOl', 149.99, 'Oakley');

INSERT INTO pedido (id_cliente, cod_produto, quantidade, data_pedido)
VALUES 
	(1, 1, 2, '2024-04-10'),
    (1, 3, 1, '2024-04-12');
    
INSERT INTO pedido (id_cliente, cod_produto, quantidade, data_pedido)
VALUES 
	(3, 1, 3, '2024-04-10'),
    (3, 3, 2, '2024-04-12');
    
SELECT clientes.nome, pedido.cod_produto, pedido.quantidade
FROM clientes
INNER JOIN pedido
ON clientes.id_cliente = pedido.id_cliente;

SET @joaosilva = (SELECT id_cliente FROM clientes WHERE nome = 'João Silva');
SET @mariaoliveira = (SELECT id_cliente FROM clientes WHERE nome = 'Maria Oliveira');
SET @carlossouza = (SELECT id_cliente FROM clientes WHERE nome = 'Carlos Souza');
SET @analima = (SELECT id_cliente FROM clientes WHERE nome = 'Ana Lima');

SET @oculos = (SELECT cod FROM produto WHERE nome = 'Óculos de SOl');
SET @calca = (SELECT cod FROM produto WHERE nome = 'Calça Jeans');

INSERT INTO pedido (id_cliente, cod_produto, quantidade, data_pedido) 
VALUES
	(@joaosilva, @oculos, 2, '2024-04-10');
    
INSERT INTO pedido (id_cliente, cod_produto, quantidade, data_pedido) 
VALUES
	(@mariaoliveira, @oculos, 1, '2024-04-11'),
    (@mariaoliveira, @calca, 1, '2024-04-13');
    
INSERT INTO pedido (id_cliente, cod_produto, quantidade, data_pedido) 
VALUES
	(@carlossouza, @calca, 3, '2024-04-09');
    
INSERT INTO pedido (id_cliente, cod_produto, quantidade, data_pedido) 
VALUES
	(@analima, @oculos, 1, '2024-04-14');
    
SELECT count(DISTINCT cod_produto) FROM pedido;

SELECT sum(quantidade) FROM pedido;

SELECT avg(preco) FROM produto;

SELECT max(preco) FROM produto;

SELECT p.cod, p.nome, sum(pe.quantidade) AS qtd
FROM pedido as pe
JOIN produto as p
ON pe.cod_produto = p.cod
GROUP BY p.cod, p.nome
ORDER BY qtd DESC;

SELECT
	clientes.nome AS NomeCliente,
    produto.nome AS ProdutoCOmprado,
    pedido.quantidade AS Quantidade,
    pedido.data_pedido AS DataPedido
FROM clientes
LEFT JOIN pedido
ON clientes.id_cliente = pedido.id_cliente
LEFT JOIN produto
ON pedido.cod_produto = produto.cod;

-- Clientes que fizeram mais de 2 pedidos

SELECT nome
FROM clientes
WHERE id_cliente IN (
	SELECT id_cliente
    FROM pedido
    GROUP BY id_cliente
    HAVING COUNT(cod_produto) > 2
);

-- 

SELECT nome,
	(
		SELECT COUNT(*)
        FROM pedido
        WHERE pedido.cod_produto = produto.cod
    ) AS TotalPedidos
FROM produto;

-- Clientes que fizeram pelo menos um pedido

SELECT nome
FROM clientes c
WHERE EXISTS (
	SELECT 1
    FROM pedido p
    WHERE p.id_cliente = c.id_cliente
);

CREATE VIEW v_pedidos AS
SELECT
	clientes.nome AS NomeCliente,
    produto.nome AS ProdutoComprado,
    pedido.quantidade AS Quantidade,
    pedido.data_pedido AS DataPedido
FROM clientes
JOIN pedido
ON clientes.id_cliente = pedido.id_cliente
JOIN produto
ON pedido.cod_produto = produto.cod;

CREATE INDEX idx_id_cliente ON clientes(id_cliente);

SHOW INDEX FROM clientes;

EXPLAIN SELECT c.nome, p.cod_produto
FROM clientes c
USE INDEX (idx_id_cliente)
JOIN pedido p
ON c.id_cliente = p.id_cliente
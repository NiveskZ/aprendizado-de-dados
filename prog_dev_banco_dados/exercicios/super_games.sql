CREATE DATABASE IF NOT EXISTS SuperGames; 

USE SuperGames; 

CREATE TABLE localizacao ( 
    id INT PRIMARY KEY AUTO_INCREMENT, 
    secao VARCHAR(50) NOT NULL, 
    prateleira INT NOT NULL 
); 

CREATE TABLE jogo ( 
    cod INT PRIMARY KEY AUTO_INCREMENT, 
    nome VARCHAR(50) NOT NULL, 
    valor DECIMAL(6, 2) NOT NULL, 
    localizacao_Id INT NOT NULL, 
    FOREIGN KEY (localizacao_id) REFERENCES localizacao(id) 
); 

INSERT INTO localizacao
VALUES 
   (0, "Corrida", "001"), 
   (0, "Corrida", "002"), 
   (0, "Aventura", "100"), 
   (0, "Aventura", "101"), 
   (0, "RPG", "150"), 
   (0, "RPG", "151"), 
   (0, "Plataforma", "200"); 


INSERT INTO jogo VALUES 
   (0, "Mario Carro 8", 125.00, 1), 
   (0, "NFS U2 Remake", 150.00, 2), 
   (0, "A Sombra do Colosso", 200.00, 3), 
   (0, "A Lenda do Zeldo: Chorinho do Reino", 299.00, 4),
   (0, "Chrono Break", 205.00, 5),
   (0, "Fakemon Lápis/Caneta: Double Pack", 589.00, 6),
   (0, "Super Mério Broca", 349.00, 7);
   
SELECT jogo.nome, localizacao.prateleira
FROM jogo INNER JOIN localizacao
ON localizacao.id = jogo.localizacao_id
WHERE localizacao.secao = 'Aventura';

SELECT localizacao.secao, jogo.nome
FROM localizacao
LEFT JOIN jogo
ON localizacao.id = jogo.localizacao_id
ORDER BY jogo.nome ASC;


-- O número total de registros na tabela de jogos.
SELECT count(*) FROM jogo;

-- O valor do jogo mais caro.

SELECT nome, valor
FROM jogo
ORDER BY valor DESC
LIMIT 1;

-- O valor do jogo mais barato.
SELECT nome, valor
FROM jogo
ORDER BY valor ASC
LIMIT 1;

-- A média de preço dos jogos de corrida.
SELECT l.secao, avg(j.valor)
FROM jogo AS j
LEFT JOIN localizacao AS l
ON l.id = j.localizacao_id
WHERE l.secao = 'Corrida'
GROUP BY l.secao;

-- E o valor total em estoque na loja.
SELECT sum(valor)
FROM jogo;

-- Adicionar os novos títulos ao banco de dados para que os clientes possam consultá-los.

INSERT INTO localizacao
VALUES 
	(0, "Corrida", "003"),
    (0, "Plataforma", "201"),
    (0, "Aventura", "102"),
    (0, "RPG", "152");
    
INSERT INTO jogo
VALUES
	(0, "CTR", 250.00, 8),
    (0, "Donkey Monkey Country 4", 300.00, 9),
    (0, "Horizonte Esquecido Oeste", 150.00, 10),
    (0, "Final Costume XX", 299.00,11);
    

-- Alterar os preços dos jogos em promoção.

SELECT cod 
FROM jogo 
WHERE nome IN ("A Sombra do Colosso","NFS U2 Remake");

UPDATE jogo
SET valor = valor * 0.5
WHERE cod IN (2, 3);

-- Criar uma tabela chamada Promoção, com um número identificador da promoção e o código do jogo (chave estrangeira da tabela de jogo).
CREATE TABLE promocao (
	id INT PRIMARY KEY AUTO_INCREMENT,
    cod_jogo INT,
    FOREIGN KEY (cod_jogo) REFERENCES jogo(cod)
);

-- Inserir os jogos em promoção na tabela criada. 

INSERT INTO promocao (cod_jogo)
VALUES
	((SELECT Cod FROM jogo WHERE Nome = 'A Sombra do Colosso')),
	((SELECT Cod FROM jogo WHERE Nome = 'NFS U2 Remake'));

-- Implementar uma maneira de selecionar o nome do jogo, o valor e o nome da seção dos títulos em promoção
SELECT jogo.nome, jogo.valor, localizacao.secao
FROM jogo
INNER JOIN localizacao
ON jogo.localizacao_id = localizacao.id
WHERE jogo.cod IN (SELECT cod_jogo FROM promocao);

-- Implementar uma maneira de selecionar os títulos e seus respectivos valores que não estão em promoção,
-- retornando apenas os mais recentes disponíveis na loja

SELECT j.nome, j.valor
FROM jogo AS j
WHERE j.cod NOT IN (SELECT cod_jogo FROM promocao)
ORDER BY j.cod DESC;

CREATE VIEW v_consultaJogos AS
	SELECT localizacao.secao, localizacao.prateleira, jogo.nome, jogo.valor
	FROM localizacao LEFT JOIN jogo
	ON localizacao.Id = jogo.localizacao_Id
	ORDER BY jogo.nome ASC;

SELECT * FROM v_consultaJogos; 
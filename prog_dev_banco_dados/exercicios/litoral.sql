CREATE DATABASE litoral; 

USE litoral; 

CREATE TABLE escuna ( 
    numero INT PRIMARY KEY, 
    nome VARCHAR(30), 
    capitao_cpf CHAR(11) 
); 

CREATE TABLE destino ( 
    id INT PRIMARY KEY AUTO_INCREMENT, 
    nome VARCHAR(30) 
); 

CREATE TABLE passeio ( 
    id INT PRIMARY KEY AUTO_INCREMENT, 
    data DATE, 
    hora_saida TIME, 
    hora_chegada TIME, 
    escuna_numero INT, 
    destino_id INT, 
    FOREIGN KEY(escuna_numero) REFERENCES escuna(numero), 
    FOREIGN KEY(destino_id) REFERENCES destino(id) 
); 

INSERT INTO escuna
	VALUES 
	(12345, "Black Flag","88888888899"), 
	(12346, "Caveira","66666666677"), 
	(12347, "Brazuca","44444444455"), 
	(12348, "Rosa Brilhante 1","12345678900"), 
	(12349, "Tubarão Ocean","22222222233"), 
	(12340, "Rosa Brilhante 2","12345678900"); 

INSERT INTO destino
VALUES 
	(0, "Ilha Dourada"), 
	(0, "Ilha D'areia fina"), 
	(0, "Ilha Encantada"), 
	(0, "Ilha dos Ventos"), 
	(0, "Ilhinha"), 
	(0, "Ilha Torta"), 
	(0, "Ilha dos Sonhos"), 
	(0, "Ilha do Sono"); 

INSERT INTO passeio 
VALUES 
	(0,20180102,080000,140000,12345,1), 
	(0,20180102,070000,170000,12346,8), 
	(0,20180102,080000,140000,12340,3), 
	(0,20180103,060000,120000,12347,2), 
	(0,20180103,070000,130000,12348,4), 
	(0,20180103,080000,140000,12349,6), 
	(0,20180103,090000,150000,12345,5), 
	(0,20180104,070000,160000,12347,1), 
	(0,20180104,070000,170000,12345,3), 
	(0,20180104,090000,130000,12349,7), 
	(0,20180105,100000,180000,12340,8), 
	(0,20180105,090000,130000,12347,7); 

-- Modificar o comando COMMIT para evitar a gravação automática das alterações.
SET AUTOCOMMIT=0;
-- Criar um ponto de restauração no banco de dados.
SAVEPOINT point1;
-- Realizar um teste para reproduzir o mesmo erro cometido pelo funcionário da prefeitura, que consiste em nomear todos os registros com o mesmo nome.
UPDATE destino
SET nome = 'Pequena Ilha do Mar'
WHERE id > 0;

SELECT * FROM destino;
-- Efetuar um teste de utilização do ponto de restauração criado.
ROLLBACK TO SAVEPOINT point1;
SELECT * FROM destino;
-- Registrar as alterações realizadas.
COMMIT;
-- Estabelecer um novo ponto de restauração, pois o anterior será eliminado após a gravação das alterações.
SAVEPOINT point2;

CREATE TABLE vendas ( 

    numero INT PRIMARY KEY AUTO_INCREMENT, 

    destinoId INT NOT NULL, 

    embarque DATE NOT NULL, 

    qtd INT NOT NULL, 

    FOREIGN KEY (destinoId) REFERENCES destino(id) 

); 

ALTER TABLE destino ADD COLUMN valor DECIMAL(5,2);

UPDATE destino SET Valor = 100 WHERE id = 1;
UPDATE destino SET Valor = 120 WHERE id = 2;
UPDATE destino SET Valor = 80 WHERE id = 3;
UPDATE destino SET Valor = 90 WHERE id = 4;
UPDATE destino SET Valor = 100 WHERE id = 5;
UPDATE destino SET Valor = 150 WHERE id = 6;
UPDATE destino SET Valor = 120 WHERE id = 7;
UPDATE destino SET Valor = 180 WHERE id = 8;


CREATE FUNCTION fn_desconto(valor DECIMAL(5,2), qtd INT)
RETURNS DECIMAL(5,2)
DETERMINISTIC
RETURN((valor*qtd)*0.7);

CREATE PROCEDURE proc_desc(VAR_VendasNumero INT)
SELECT (fn_desconto(d.valor, v.qtd)) AS "Valor com desconto", d.nome AS "Destino", v.qtd AS "Passagens", v.embarque
FROM vendas v
INNER JOIN destino d
ON v.destinoId = d.id
WHERE Numero = VAR_VendasNumero;

INSERT INTO vendas
VALUES
	(0,1,"2024-02-03",3),
    (0,7,"2024-02-03",2),
    (0,5,"2024-02-03",1);


CALL proc_desc(1);
CALL proc_desc(2);
CALL proc_desc(3);

SELECT * FROM vendas;

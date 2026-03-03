CREATE DATABASE banco_bank;

USE banco_bank;

CREATE TABLE contas (
	id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50),
    saldo DECIMAL (10,2)
);

INSERT INTO contas
VALUES
	(0, 'conta1', 5000),
    (0, 'conta2', 3000);

SELECT * FROM contas;

START TRANSACTION;

DELETE FROM contas WHERE id = 2;

SAVEPOINT ponto1;

UPDATE contas SET saldo = 20 WHERE id =1;

ROLLBACK TO SAVEPOINT ponto1;
ROLLBACK;
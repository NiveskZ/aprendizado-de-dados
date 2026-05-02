CREATE DATABASE IF NOT EXISTS Loja;
USE Loja;
 
-- Tabela Cliente
CREATE TABLE Cliente (
    id       INT          NOT NULL AUTO_INCREMENT,
    nome     VARCHAR(100) NOT NULL,
    cpf      VARCHAR(14)  NOT NULL,
    telefone VARCHAR(20),
    email    VARCHAR(100),
    PRIMARY KEY (id)
);
 
-- Tabela Produto
CREATE TABLE Produto (
    id         INT           NOT NULL AUTO_INCREMENT,
    descricao  VARCHAR(100)  NOT NULL,
    preco      DECIMAL(10,2) NOT NULL,
    estoque    INT           NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);
 
-- Tabela Pedido
CREATE TABLE Pedido (
    id         INT  NOT NULL AUTO_INCREMENT,
    id_cliente INT  NOT NULL,
    data       DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id)
);
 
-- Tabela ItemPedido
CREATE TABLE ItemPedido (
    id         INT           NOT NULL AUTO_INCREMENT,
    id_pedido  INT           NOT NULL,
    id_produto INT           NOT NULL,
    quantidade INT           NOT NULL,
    preco_unit DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_pedido)  REFERENCES Pedido(id),
    FOREIGN KEY (id_produto) REFERENCES Produto(id)
);
 
-- Tabela ContaReceber
-- Situacao: 1 = Registrada (não paga) | 2 = Cancelada | 3 = Paga
CREATE TABLE ContaReceber (
    id         INT           NOT NULL AUTO_INCREMENT,
    id_cliente INT           NOT NULL,
    id_pedido  INT           NOT NULL,
    vencimento DATE          NOT NULL,
    valor      DECIMAL(10,2) NOT NULL,
    situacao   ENUM('1','2','3') NOT NULL DEFAULT '1',
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id),
    FOREIGN KEY (id_pedido)  REFERENCES Pedido(id)
);

USE Loja;
 
-- Clientes
INSERT INTO Cliente (nome, cpf, telefone, email) VALUES
    ('Ana Paula Souza',    '111.222.333-44', '(11) 98765-4321', 'ana.souza@email.com'),
    ('Bruno Costa Lima',   '222.333.444-55', '(21) 91234-5678', 'bruno.lima@email.com'),
    ('Carla Mendes Rocha', '333.444.555-66', '(31) 99876-5432', 'carla.rocha@email.com');
 
-- Produtos
INSERT INTO Produto (descricao, preco, estoque) VALUES
    ('Notebook Dell Inspiron 15', 3799.90, 10),
    ('Mouse Wireless Logitech',     129.90, 50),
    ('Teclado Mecânico Redragon',   249.90, 30);
 
-- Pedidos (respeitando FK: id_cliente deve existir)
INSERT INTO Pedido (id_cliente, data) VALUES
    (1, '2025-04-10'),
    (2, '2025-04-15'),
    (3, '2025-04-20');
 
-- Itens dos Pedidos (respeitando FK: id_pedido e id_produto devem existir)
INSERT INTO ItemPedido (id_pedido, id_produto, quantidade, preco_unit) VALUES
    (1, 1, 1, 3799.90),
    (2, 2, 2,  129.90),
    (2, 3, 1,  249.90),
    (3, 3, 1,  249.90);
 
-- Contas a Receber
-- situacao '1' = registrada (não paga), '3' = paga
INSERT INTO ContaReceber (id_cliente, id_pedido, vencimento, valor, situacao) VALUES
    (1, 1, '2025-05-10', 3799.90, '1'),
    (2, 2, '2025-05-15',  509.70, '3'),
    (3, 3, '2025-04-25',  249.90, '1');

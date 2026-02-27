-- 1. Visão Geral: Lista dos nomes de todos os produtos e seus preços
SELECT ProductName, UnitPrice 
FROM Product;

-- Lista de Produtos com mais de 50 de custo e menos de 10 unidades
SELECT ProductName, UnitPrice
FROM Product
WHERE UnitPrice > 50 AND UnitsInStock < 10; 

--
SELECT
	CategoryID,
	COUNT(*) AS QtdProdutos,
	AVG(UnitPrice) AS PrecoMedio
FROM Product
GROUP BY CategoryId 
ORDER BY PrecoMedio;

-- Colocando com Nome das categorias
SELECT 
	c.CategoryName,
	COUNT(p.id) AS qtdProdutos,
	AVG(p.UnitPrice) AS PrecoMedio
FROM Category AS c
LEFT JOIN Product as p ON c.Id = p.CategoryId 
GROUP BY c.CategoryName;

-- Quais sao as 3 categorias de produtos que mais geram receita total?

SELECT 
	c.CategoryName,
	SUM(od.UnitPrice * od.Quantity) AS ReceitaTotal
FROM Category AS c 
LEFT JOIN Product AS p 
ON c.Id = p.CategoryId 
LEFT JOIN OrderDetail AS od 
ON p.Id = od.ProductId 
GROUP BY CategoryName
ORDER BY ReceitaTotal DESC
LIMIT 3;

a





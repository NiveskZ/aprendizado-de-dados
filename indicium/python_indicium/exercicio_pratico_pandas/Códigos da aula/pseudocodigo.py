# ter uma lista de pessoas
# saber a idade das pessoas
# definição da idade limite
# passar por cada pessoa da lista
# comparar a idade da pessoa com a idade limite
# caso a idade da pessoa esteja dentro do limite, deixar ela entrar
# se tiver abaixo do limite, cai fora

john = {"nome": "antonio", "idade": 27}
natan = {"nome": "natan", "idade": 15}
juliana = {"nome": "juliana", "idade": 19}
paulo = {"nome": "paulo", "idade": 13}
eric = {"nome": "eric", "idade": 21}

lista_pessoas = [john, natan, juliana, paulo, eric]

idade_limite = 21

for person in lista_pessoas:
    nome_pessoa = person["nome"]
    if person["idade"] > idade_limite:
        print(f"Pode entrar {nome_pessoa}")
    else:
        print("Cai fora")
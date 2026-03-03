
lista_letras = ["a", "b", "c","d","e","f","g","h","i","j","k","l"]

# Loop pela lista de letras retornando os elementos em batches
batch_size = 5
for i in range(0, len(lista_letras), batch_size):
    batch = lista_letras[i:i + batch_size]
    print(batch)

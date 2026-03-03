# Exemplo de ordem de argumentos passados para a função

# Lembrando que no momento de definição da função, definimos os parâmetros
# E na hora de invocar, passamos os argumentos

def complex_op(total, divisor, subtractor):
    return total/divisor-subtractor

print(complex_op(100, 2, 25))

print(complex_op(divisor=2,total=100,subtractor=25))

print(complex_op(2, 100, 25))

# print(complex_op(divisor=2,total=100,25)) # dá erro

# print(complex_op(2,100)) # dá erro

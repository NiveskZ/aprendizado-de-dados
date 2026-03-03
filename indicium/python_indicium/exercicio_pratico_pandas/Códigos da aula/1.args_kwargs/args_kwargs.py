# args - trata série de argumentos em tupla como uma lista
def greet(*args):
    for name in args:
        print(f"Olá, {name}!")

greet("Alice", "Bob", "Charlie")


#kwargs - pega valores como em um dicionário
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

print_info(name="John", age=27, city="Florianópolis")

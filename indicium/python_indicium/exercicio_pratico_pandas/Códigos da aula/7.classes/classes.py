# Classe base
class Mamifero:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return "Barulho específico do mamífero"

    def info(self):
        return f"{self.name} é um {self.__class__.__name__} e tem {self.age} anos."


# Subclasse para Humanos
class Humano(Mamifero):
    def __init__(self, name, age, language):
        super().__init__(name, age)
        self.language = language

    def speak(self):
        return f"Olá! Eu falo {self.language}."


# Subclasse para Cachorros
class Cachorro(Mamifero):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

    def speak(self):
        return "Au-au"



# Example usage
john = Humano("Antônio", 27, "Mandarim")
beethoven = Cachorro("Beethoven", 15, "São Bernardo")

animals = [john, beethoven]

for animal in animals:
    print(animal.info())
    print(animal.speak())
    print("---")


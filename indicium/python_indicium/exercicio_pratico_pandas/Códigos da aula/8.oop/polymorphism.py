# O exemplo de polimorfismo mostra como podemos criar várias formas, obviamente
# A partir da possibilidade de mudar comportamentos entre classes que possuam ->
# Uma mesma base

class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Bark!")

def make_animal_speak(animal):
    animal.speak()

make_animal_speak(Dog())     # Bark!
make_animal_speak(Animal())  # Animal sound

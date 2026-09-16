def vet(name):
    return f"Name of the vet is: {name}"

class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        return (self.name + " says Woof!")

    def eat(self,food):
        return f"{self.name} eats {food}"

    def human_age(self):
        return self.age * 7

    def run(self, distance, speed):
        return f"{self.name} runs {distance} km at {speed} km/h"

    def __str__(self):
        return self.name + " is " + str(self.age) + " years old."


dog1 = Dog("Rex",2)
dog2 = Dog("Cara",13)
print(dog1)
dog1.bark()
print(dog1.run(10,29))
print(dog1.eat("poopi"))
print(dog1.human_age())
print(vet("Dog Hospital"))

print(f"{dog1.bark()} {dog2.bark()}")
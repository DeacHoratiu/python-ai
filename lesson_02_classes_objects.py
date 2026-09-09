import json
# self == this, in java sau javascript
# all methods surrounded by __, like __str__ are Dunder methods

class User:
    def __init__(self, name,age):
        self.name = name
        self.age = age
        self.nationality = "Romanian"

    def to_json(self):
        d1 = {"name": self.name, "age": self.age,"nationality": self.nationality}
        return json.dumps(d1)

    def say_hello(self):
        print(self.name + " says hi!")

    def __str__(self):
        return "" + self.name + " "+ str(self.age) + ", " + self.nationality

if __name__ == "__main__":

    #folosind User() initializam o instanta a clasei User
    sonia = User("Sonia",30)
    dragos = User("Dragos",35)

    print(sonia.to_json())
    print(dragos)
    print(sonia.name)

    sonia.say_hello()

    #structuri de date:
    #list: [10,11,21]
    #dict: {"name":"gusti"}

    #set

    s1 = set([10,30,40,40])
    print(s1)


    #json

    json_text = '{"name": "Jason", "age":25}'
    created_dict = json.loads(json_text)

    print(created_dict["name"])

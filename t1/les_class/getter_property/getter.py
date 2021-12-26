#class must inherit from object in order for properties to work
class Person(object):
    def __init__(self, age = 0):
        print("person constructor called")

        age = int(age)

        if age < 0:
           self._age = 0
        else:
            self._age = age


    @property
    def age(self):
        #print("person age getter called")
        return self._age

    @age.setter
    def age(self, value):
        #print("person age setter called with set value of", value)

        value = int(value)
        if (value < 0):
            self._age = 0
            #you could also raise an error instead. for example:
            #raise ValueError("tried to set Person age to a negative number("+value+")")
        else:
            self._age = value

if __name__ == "__main__":
    print("Test example of Person class with getters and setters")

    p = Person(7)

    print(p.age)

    p.age = 34
    print(p.age)

    p.age = -2
    print(p.age)




#class must inherit from object in order for properties to work
class Person(object):
    def __init__(self, age = 0):
        print("person constructor called")

        age = int(age)

        if age < 0:
           self._age = 0
        else:
            self._age = age

    # if value is None this function works like a get (retreiving the value of age)
    # if value is an int this function works like a set (setting the value of age)
    def age(self, value=None):
        if value is None:
            #print("person age getter called")
            return self._age

            #print("person age setter called with set value of", value)
        else:
            value = int(value)
            if value < 0:
                self._age = 0
                #you could also raise an error instead. for example:
                #raise ValueError("tried to set Person age to a negative number("+value+")")
            else:
                self._age = value

if __name__ == "__main__":
    print("Test example of Person class with getters and setters")

    p = Person(7)

    print(p.age())

    p.age(34)
    print(p.age())

    p.age(-2)
    print(p.age())




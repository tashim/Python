# this solution shows how to use the json module to convert python objects
# into a json text representation, and how to convert a json text representation
# into a python object (Note: it won't necessarily be the exact type, but will retain all the data)
#
# read more at: https://docs.python.org/3/library/json.html
import json

a,b = 0,0

FILENAME = "data.json"

while 1:

    #print("a = {}; b = {}".format(a,b))
    print("a = %d; b = %d" % (a,b))

    print("""
    set (A)
    set (B)
    (S)ave
    (L)oad
    (Q)uit
    
    """)

    option = input("Option: ").upper()

    if option == "A":
        a = int(input("enter new value for A:"))

    elif option == "B":
        b = int(input("enter new value for B:"))

    elif option == "S":
        f = open(FILENAME, "w")
        json.dump([a,b], f)
        f.close()

    elif option == "L":
        f = open(FILENAME, "r")
        print( json.load(f))
        f.close()
        '''
        x = json.load(FILENAME)
        a = x[0]
        b =  x[1]
        '''
    elif option == "Q":
        break

    else:
        print("\ninvalid option!\n")






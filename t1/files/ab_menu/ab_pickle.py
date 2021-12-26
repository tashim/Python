#this solution shows how to use the pickle module to convert python objects into bytes(binary) and
#how to convert it back from bytes to the object
#
# WARNING: using pickle can be dangerous, because it might sending harmful python objects
# read more at: https://docs.python.org/3/library/pickle.html
import pickle

a,b = 0,0

FILENAME = "data.pickle"

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
        f = open(FILENAME, "wb")
        pickle.dump([a,b], f)
        f.close()

    elif option == "L":
        f = open(FILENAME, "rb")
        a,b = pickle.load(f)
        f.close()
        '''
        x = pickle.load(FILENAME)
        a = x[0]
        b =  x[1]
        '''
    elif option == "Q":
        break

    else:
        print("\ninvalid option!\n")






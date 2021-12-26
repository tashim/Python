"""
this example shows how to open a file for text write,read
and shows how to parse our data into text and back from text
"""
a,b = 0,0
FILENAME = "data.txt"

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
        f.write("{}\n{}\n".format(a,b))
        f.close()

    elif option == "L":
        f = open(FILENAME, "r")
        a = int(f.readline())
        b = int(f.readline())
        f.close()

    elif option == "Q":
        break

    else:
        print("\ninvalid option!\n")






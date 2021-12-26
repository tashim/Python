#this example shows the use of "with" keyword for automatically closing files
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
        with open(FILENAME, "w") as f:
            f.write("{}\n{}\n".format(a,b))

    elif option == "L":
        with open(FILENAME, "r") as f:
            a = int(f.readline())
            b = int(f.readline())

    elif option == "Q":
        break

    else:
        print("\ninvalid option!\n")






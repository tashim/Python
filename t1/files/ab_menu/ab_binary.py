"""
this example show how to open a file for binary write/read
and how to use int.to_bytes and int.from_bytes to convert the data to
and from binary
"""

a,b = 0,0
FILENAME = "data.bin"

SIZE = 4                #how many bytes we want to store for each number

ORDER = "little"        #in what order we wnat to store those files
                        #little=from the least significat byte (LSB) to the most significant byte (MSB)
                        #big = from the MSB to the LSB

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
        f = open(FILENAME, "wb") # the "b" in mode is important, otherwise it will open as text file
        f.write(a.to_bytes(SIZE,ORDER))
        f.write(b.to_bytes(SIZE,ORDER))
        f.close()

    elif option == "L":
        f = open(FILENAME, "rb") # the "b" in mode is important, otherwise it will open as text file
        a = int.from_bytes(f.read(SIZE), ORDER)
        b = int.from_bytes(f.read(SIZE), ORDER)
        f.close()

    elif option == "Q":
        break

    else:
        print("\ninvalid option!\n")






#this example shows some usage of try and except to handle errors
a, b = 0, 0

try:
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
            try:
                a = int(input("enter new value for A:"))
            except ValueError:
                print("that's not an integer")

        elif option == "B":
            try:
                a = int(input("enter new value for A:"))
            except ValueError:
                print("that's not an integer")

        elif option == "S":
            filename = input("enter file name to save:")

            with open(filename, "w") as f:
                f.write("{}\n{}\n".format(a,b))

        elif option == "L":
            try:
                filename = input("enter file name to load:")

                with open(filename, "r") as f:
                    a = int(f.readline())
                    b = int(f.readline())
            except FileNotFoundError as e:
                print("there is no such file")

        elif option == "Q":
            break

        else:
            print("\ninvalid option!\n")

except:
    print("something bad happend")
    raise

finally:
    print("a = {}, b = {}".format(a,b))



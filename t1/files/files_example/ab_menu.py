# f.seek(-4, 2) # go four bytes backwards before end of file
# f.seek(0) # go to start of file
# f.seek(5) # go five bytes forward from start of file
# f.seek(-3, 1) # go three bytes backwards from current position

a = 0
b = 0
changed = False


def save_ab():
    global f, changed
    f = open("ab.txt", "w")
    f.write(str(a) + "\n" + str(b) + "\n")
    f.close()
    changed = False


while True:
    print("A = ", a, "B = ", b)
    print()
    print("set (A)")
    print("set (B)")
    print("(S)ave")
    print("(L)oad")
    print("(Q)uit")
    print()

    inp = input("option:").lower()

    if inp == 'a':
        a = int(input("enter new number for A"))
        changed = True

    elif inp == 'b':
        b = int(input("enter new number for B"))
        changed = True

    # SAVE
    elif inp == 's':
        save_ab()

    # LOAD
    elif inp == 'l':
        f = open("ab.txt", "r")
        a = int(f.readline())
        b = int(f.readline())

        f.close()
        changed = False

    # QUIT
    elif inp == 'q':
        if changed:
            if input("save changes (y/n)?").lower() == 'y':
                save_ab()

        quit()
    else:
        input("bad input. Press ENTER to continue...")



















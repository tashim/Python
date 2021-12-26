
def isnum(a):
    if type(a) != type(1):
        if type(a) == type(" "):
            if not a.isdigit():
                print("a format not correct")
                return None
            else:
                a=int(a)
        else:
            print("a format not correct")
            return None
    return a


def dev(a=1,b=1):
    a = isnum(a)
    b = isnum(b)
    if a == None or b == None:
        return None
    if b==0:
        print(" dev bo 0")
        return None
    return a/b

def minus(a=1,b=1):
    a = isnum(a)
    b = isnum(b)
    if a == None or b == None:
        return None
    return a-b

def mul(a=1,b=1):
    a = isnum(a)
    b = isnum(b)
    if a == None or b == None:
        return None
    return a*b

def sum(a=1,b=1):
    a = isnum(a)
    b = isnum(b)
    if a == None or b == None:
        return None
    return a+b

p=print
p('eeer')
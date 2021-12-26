# import time
#
#
# for i in range(101):
#     print("\rfinished", i, "%", end='', flush=True)
#     time.sleep(0.1)
# print(" COMPLETED!")
#
# d = {"1":"t1","2":"t2","3":"t3","4":5}
# for n,key in enumerate(d):
# 	print(n,key,d[key])
#
# for x in d:#"AAAAAAAAA    AAAAAAAAA", "BBBBBB", "CC":
#     #print("\rreading", x, "                    ", end='', flush=True)
#     print("\rreading", x, "::",d[x],"           " ,end='', flush=True)
#     time.sleep(1)
#
# print()
def fun(a,b,w=None):
    a=5
    print("function",w)

def num(a,b):

    number = a/b
    return number

a = int(input("number a"))
b = int(input("number b"))

rez=num(a,b)
print(num(a,b))



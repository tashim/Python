#!/usr/bin/env python

# str = input('get sting')

def getmul(text):
    li = text.split('*')
    mul=1
    for l in li:
        try:
            mul *= int(l)
        except:
            mul *= getdev(l)
    return mul

def getdev(text):
    li = text.split('/')
    if len(li)<2:
        print('error dev')
        exit(2)
    dev = int(li[0])/int(li[1])
    for index in range(1,len(li)-1):
        print(index)
        try:
            dev = dev/int(li[index])
        except:
            print("error dev2")
            exit(3)
    return dev


str=' 1-2+3*5+4+5*8-9'
# str = '8/2*3'
li = str.split('+')
l2 = []
for l in li:
    ll = l.split('-')
    print(l)
    n=0
    for t in ll:
        if n==0:
            l2.append(t)
        else:
            l2.append('-'+t)
        n=1
print(l2)
sum=0
for n in l2:
    try:
        sum +=int(n)
    except:
        sum +=getmul(n)

print(sum)
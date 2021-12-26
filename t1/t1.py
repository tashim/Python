#!/usr/bin/env python
print('t1 start',__name__)
b='tecxj'
def sum(arg1='not',arg2=5):
    global b
    print(" arg=",arg1,arg2)
    print("end fun")
    return arg2,arg1
if __name__ == '__main__':
    sum()
    sum(10)
    sum(10,1)
    a,b=sum(arg2=90,arg1=33)
    print(a)
    print(b)
print('t1 end',__name__)
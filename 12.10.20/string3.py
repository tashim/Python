
a=[1,2,"jfjf"]
b = [5,a,{},'ff']
print(a[::1])
print(b[-1])
c = a
d = list(a)
e = a.copy()
a[1] = 'new'
print('a=',a)
print('c=',c)
print('d=',d)
print('e=',e)
t = (1,)+tuple(a)

print(type(t))
print(t)
print(list(t))

for i in (1,2,34,5):
    print(i)
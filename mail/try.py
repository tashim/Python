import re
text = "     nnn   ff     fff"
x = re.findall(r'\w+',text)
n = x[0]
# print(x[1:])
b=''
for a in x[1:]:b +='_'+ a
print("==",b[1:])
print(n)
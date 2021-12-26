#
# li=['-','1','-1','a','A']
#
# for a in li:
#     print(f"ths str <{a}>")
#     print('isdigit',a.isdigit())
#     print('isdecimal',a.isdecimal())
#     print('isnumeric',a.isnumeric())
#     print('isalnum',a.isalnum())
#     print('istitle',a.istitle())
#     print('isalpha',a.isalpha())
#     print('\n')

dic ={}

f =  open('text.txt','r+')
f.seek(11)
print(f.write('1.,mnbvcxz.,mnbvcx'))
#print(f.read(10))
f.seek(10)
f.write('23456789')
f.close()
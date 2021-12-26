import os

try:
    f=open('test.tx','r+')
    # except OSError as e:
    # except FileNotFoundError as e:
except  OSError as e:
    print('ERROR:',e)
    f = open('test.tx', 'w+')

print(f)
f.seek(0,os.SEEK_END)
print(f.tell())
f.seek(f.tell()-10)
while 1:
    text = f.read(1)
    if text == '':
        break
    print(text,f.tell())
f.close()
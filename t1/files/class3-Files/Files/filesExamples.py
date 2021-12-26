'''
Created on Nov 22, 2015

@author: eimad
'''
import os

path = os.getcwd()
print ("The current working directory is %s" % path)
if os.path.exists("textfile1.txt"):
    print("is file")
else:
    print("no such file")
try:

    f = open("textfile1.txt","r+")
#except OSError as e:
#except FileNotFoundError as e:
except IOError as e:
    print('file not exist',e)
    #f = open("textfile1.txt", "w+")
exit(0)
f.write("This Is An Example2")
f.seek(0)
print (f.read())

f1 = open("text2.txt","r+")
f.seek(0)
f1.seek(0,2)

f1.write(f.read()+"\n")
print (f)
f1.seek(0)
print (f1.read())

f.close
f1.close

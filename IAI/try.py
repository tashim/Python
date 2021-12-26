from subprocess import Popen, PIPE

proc = Popen("cmd 127.1.1.1", stdout=PIPE)
b=1
n=1
while b:
    try:
        b = proc.stdout.read(1)
        n+=1
        b = b.decode()
        print(b,end='')
    except:
        print(b,end='')
        n+=1

print(n)
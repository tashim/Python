
def rect(width,height,c):
    print(c * width)
    for i in range(0, height-2):
        print(c,end='')
        print(' '*(width-2),end='')
        print(c)
    print(c * width)

def inp_int(text=''):
    i = input(f"enter {text}:")
    if not i.isdecimal():
        print('error')
        return None
    if int(i) < 2:
        print('error')
        return None
    return int(i)

def quit():
    return None

def get_char():
    global c
    c=input('char>>')
    return c

def prin():
    global w,h,c
    rect(w, h, c)
    return 1

def inw():
    global w
    w = inp_int('width')
    return w

def inh():
    global h
    h = inp_int('height')
    return h


d = {
    "q" : ["for quit",quit],
    "w" : ["input width",inw],
    "h" : ["input height",inh],
    "c" : ["input char",get_char],
    "p" : ["print",prin]
}
w=2
h=2
c = '*'
while True:
    print('==========================')
    for j in d.keys():
        print(f'\t{j} - {d[j][0]}')
    print('==========================')
    print(f'width = {w} height = {h}')
    q = input('>>')
    if not q in d:
        print('input error')
        continue
    if not d[q][1]():
        break

    # elif q == 'q':
    #     break
    # elif q == 'w':
    #     i = newf('width')
    #     if not i : continue
    #     w = i
    # elif q == 'h':
    #     i = inp_int('height')
    #     if not i : continue
    #     h= i
    # elif q == 'c':
    #     c = input('char>>')
    # elif q == 'p':
    #     rect(w, h,c)
    # else:
    #     print('input error')
    #     continue


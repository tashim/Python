
def show_rect(width,heigth,sym='*'):
    for row in range(0,heigth):
        for col in range(0,width):
            print(sym,end='')
        print()

def show_triangle(width,heigth,sym='*'):
    step = width/heigth
    col = width
    for row in range(0,heigth):
        i=0
        col = int((width-(row*2+1))/2)
        for i in range(0,col):
            print('_',end='')
        for col in range(0,row*2+1):
            print(sym,end='')
        i=0
        col = int((width-(row*2+1))/2)
        for i in range(0,col):
            print('_',end='')
        print()

show_triangle(30,6,'%')
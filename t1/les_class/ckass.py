
class rect:
    "This is a person class"
    count = 0


    def __init__(self,x=2,y=2,ch='+'):
        self.x=x
        self.y=y
        self.ch=ch
        rect.count +=1
        self.id = str(rect.count)



    def show_data(self):
        print('x= ',self.x)
        print('y= ',self.y)


    def show(self):
        for y in range(0,self.y):
            for i in range(0,self.x):
                print(self.ch,end='')
            print()

    def __add__(self, other):
        self.x += other
        self.y += other

    def __str__(self):
        self.show()
        return "hello"+self.id

    def __del__(self):
        print("deleted")




r=rect(ch='*')
r+2
r2=rect(3,3)
r.ch='z'
print(r2)
print(r)
del (r)
del (r2)

class my:
    count=0
    def __init__(self,x=0,y=0):
        print('hello constractor')
        self.x=x
        self.y=y
        my.count +=1

    def copy(self):
        return my(self.x,self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def prn(self):
        print(f'x={self.x},y={self.y}')

    def prnt(self):
        print(f'x={self.get_x()},y={self.get_y()}')

    def add(self,n):
        if isinstance(n,int):
            self.x +=n
            self.y +=n
        elif isinstance(n,my):
            self.x +=n.x
            self.y +=n.y

    def fun(self,other):
        print('x1-x2 = ',self.x-other.x)
        print('y1-y2 = ',self.y-other.y)

    def __add__(self, other):
        new=my()
        new.x=self.x+other.x
        new.y=self.y+other.y
        return new

    def __str__(self):
        return f'<{self.x},{self.y}>'

    def __del__(self):
        print('destractor')
        my.count -=1


if __name__=="__main__":
    print(' count ',my.count)
    c=my(2,5)
    w=c.copy()
    print(c+w)

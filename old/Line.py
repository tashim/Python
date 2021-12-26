from math import sqrt

from Point import *

class Line:

    def __init__(self,x=0,y=0):
        if isinstance(x,Point):
            self.pstart=x
        else:
            self.pstart=Point()
        if isinstance(y,Point):
            self.peend=y
        else:
            self.peend=Point()

    def show(self):
        print(f'<{self.pstart} {self.peend}>')

    def __str__(self):
        return  f'<Line {self.pstart} {self.peend}>'

    def lenX(self):
        return abs( self.peend.getX()-self.pstart.getX() )

    def lenY(self):
        return abs( self.peend.getY()-self.pstart.getY() )

    def len(self):
        len =  sqrt(self.lenX()**2+self.lenY()**2)
        print(len)
        return len

if __name__ == '__main__':

    l=Line(Point(1,1),Point(10,10))
    # dd=len(l)
    print(l.len())
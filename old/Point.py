class Point:

    def __init__(self,x=0,y=0,):
        if isinstance(x, Point):
            self.__x = x.__x
            self.__y = x.__y
        elif type(x)==type(0) and type(y)==type(0):
            self.__x = x
            self.__y = y
        else:
            self.__x=0
            self.__y=0

    def __len__(self):
        return self.__x

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def set(self,x=None,y=None):
        if isinstance(x, Point):
            self.__x = x.__x
            self.__y = x.__y
        else:
            if x: self.__x = x
        if y: self.__y = y


    def prn(self):
        print('x=', self.__x, ' y=', self.__y)

    def __add__(self, other):
        if isinstance(other,Point):
            return Point(self.__x + other.__x, self.__y + other.__y)
        elif type(other)==type(1):
            return Point(self.__x + other, self.__y + other)
        else: return Point(self)

    def __sub__(self, other):
        if isinstance(other,Point):
            return Point(self.__x - other.__x, self.__y - other.__y)
        elif type(other)==type(1):
            return Point(self.__x - other, self.__y - other)
        else: return Point(self)

    def __str__(self):
        return f'({self.__x},{self.__y})'

    def __radd__(self, other):
        return self+other


if __name__ == '__main__':
    print("I is Point.py")

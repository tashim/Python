class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return "Rectangle(w={}, h={})".format(self.width, self.height)

    def __repr__(self):
        return str(self)


class Square(Rectangle):
    def __init__(self, length):
        # normally we would write here:
        #   Rectangle.__init__(self, length, length)
        # but the properties we add later makes this unnecessary
        self.length = length

    # the following properties override access of width and heght
    # into access to length instead
    @property
    def width(self):
        return self.length

    @width.setter
    def width(self, value):
        self.length = value

    @property
    def height(self):
        return self.length

    @height.setter
    def height(self, value):
        self.length = value

    def __str__(self):
        return "Square(length={})".format(self.length)


def max_area(*rectangles):
    mx = rectangles[0].area()

    for rect in rectangles[1:]:
        a = rect.area()
        if a > mx:
            mx = a

    return mx

# alternative solution using a generator expression and the max function
def max_area2(*rectangles):
    return max(x.area() for x in rectangles)


if __name__ == '__main__':
    r1 = Rectangle(10,20)
    print("r1:", r1)
    print("r1.area():", r1.area())
    print("r1.perimeter():", r1.perimeter())
    print()

    print("changing width to 15:")
    r1.width = 15
    print("r1:", r1)
    print()

    r2 = Square(15)
    print("r2:", r2.perimeter())
    print("r2.area():", r2.area())
    print()

    print("changing width to 30:")
    r2.height = 30
    print("r2:", r2)
    print("r2.area():", r2.area())
    print()

    print("testing max_area:")
    print(max_area(r1, r2, Square(5), Rectangle(35, 2)))
    print()

    print("testing max_area2:")
    print(max_area2(r1, r2, Square(5), Rectangle(35, 2)))
    print()


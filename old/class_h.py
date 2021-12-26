
l=[2,3,4,5]

class MyList(list):
    def __init__(self,arg=[]):
        list.__init__(self,arg)

    def show(self):
        for i in self:
            print(i)

l=MyList((2,3,4,5))
print(l)
l.show()

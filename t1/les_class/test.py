
def fun(*lst):
    print(type(lst))
    print(lst)
    base()

class base():
    count=0
    def __init__(self):
        print('self=',self)
        base.count += 1
        self.num = base.count
        self.show=10
        print('constractor base',self.num,base.count)

    def __del__(self):
        # base.count -= 1
        print('destractor',self.num,base.count)

    def __str__(self):
        return 'this is class BSAE'


class ben1(base):
    def __init__(self):
        print('constr ben')
        base.__init__(self)

    def __del__(self):
        print('destr ben')

    def __str__(self):
        return  'class BEN1'

    @property
    def show(self):
        print("show property ")
        return 'sfs'

    @show.setter
    def show(self,text):
        print("set value",text)
        return base.count



# b = base()

ben = ben1()
ben.show = 'prop =','fffff'
ben.show = 'prop 1'
ben.show = 'prop 2'

print('dddd',ben.show)
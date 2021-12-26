from Point import *


p=Point(2,5)
print(len(p))
p.__y=-3
p.__x=-3
p.prn()
p2=Point(2+p+7)
(p+p2).prn()
(p+4).prn()

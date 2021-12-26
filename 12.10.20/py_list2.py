a = [3, 56, 700]

a = a[:2] + [60] + a[2:]

b = a[:]

print(*a, sep='\n')

a[0] = 5

print(*b)

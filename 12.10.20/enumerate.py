a = [60, 45, 23, 100, 564, 8]

m = 0
m_i = -1

for (i, v) in enumerate(a):
	if v > m:
		m = v
		m_i = i

print(f'The max value in the list is: {m}, its index is {m_i}')

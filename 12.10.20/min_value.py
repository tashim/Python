a = [60, 45, 23, 100, 564, 8]

min_v = max_v = None

for x in a:
	if not min_v or x < min_v:
		min_v = x

	if not max_v or x > max_v:
		max_v = x

print(f'Max value: {max_v}, min value: {min_v}')

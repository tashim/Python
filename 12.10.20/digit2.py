while True:
	b = input("Please enter a number:\n\t")

	if not b.isdecimal():
		if b == 'q':
			print("bye!")
			quit()
			# break

		print(" ", "not a decimal".upper(), " ", sep='\n')
		continue

	b_int = int(b)

	if b_int > 10:
		print("input is greater than 10")
	elif b_int == 10:
		print("input is 10")
	else:
		print("input is less than 10")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  malben.py

def rect(place,size,defsim='*'):
	for row in range(size["height"]):
		for n in range(place):
			print(' ',end='')
		if row == 0 or row == size["height"]-1:
			sim0 = '-'
		else:
			sim0 = defsim
		for col in range(size["width"]):
			if col == 0 or col == size["width"]-1:
				sim = 'I'
			else:
				sim = sim0
			print(sim,end='')
		print()
	

if __name__ == '__main__':
	place=0
	size = {}
	size["width"]=4
	size["height"]=4
	sim = '.'
	while(True):
		print("""
	1 : get simbol
	2 : input place
	3 : input width
	4 : input height
	p : print
	q : quit
		input your choce:""",end='')
		choce = input()
		if choce in ('q','Q'): break
		elif choce in  ('p','P'):
			rect(place,size,sim)
		elif choce == '1':
			text = input('input simbol :').strip()
			if len(text) > 0:
				sim = text[0]
			else:
				sim = ' '
		elif choce == '2':
			try:
				place = int( input('input place :') )
			except ValueError:
				print("eroor : not number")
		elif choce == '3':
			try:
				size["width"] =int( input('input width :') )
			except ValueError:
				print("eroor : not number")
		elif choce == '4':
			try:
				size["height"] =int( input('input height :') )
			except ValueError:
				print("eroor : not number")
		else: print(" error choce" )

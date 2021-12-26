#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  malben.py
opt = {'place':1,'sym':'*','height':4,'width':4}

def place():
	try:
		opt['place'] = int( input('input place :') )
	except ValueError:
		print("eroor : not number")

def width():
	try:
		opt["width"] =int( input('input width :') )
	except ValueError:
		print("eroor : not number")
		

def height():
	try:
		opt["height"] =int( input('input height :') )
	except ValueError:
		print("eroor : not number")
		

def symbol():
	text = input('input symbol :').strip()
	if len(text) > 0:
		opt['sym'] = text[0]
	else:
		opt['sym'] = ' '

def quit():
	exit(0)

	
def rect():
	global opt
	print('=>')
	for row in range(opt["height"]):
		for n in range(opt['place']):
			print(' ',end='')
		if row == 0 or row == opt["height"]-1:
			sim0 = '-'
		else:
			sim0 = opt['sym']
		for col in range(opt["width"]):
			if col == 0 or col == opt["width"]-1:
				sim = 'I'
			else:
				sim = sim0
			print(sim,end='')
		print()
	print("=>")
	

if __name__ == '__main__':
	menu = {'q':["quit",quit],"1":["get symbol",symbol],
	"2":["input place",place],"3":["input width",width],"4":["input height",height],
	"p":["print",rect]}

	while(True):
		for key in menu:
			print("--",key," - ",menu[key][0])
		choce = input("your choce:")
		if not choce in menu:
			print(" error choce" )
			continue
			
		menu[choce][1]()

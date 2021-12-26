#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  malben.py
opt = {'place':1,'sym':'*','height':4,'width':4}



def rect():
	global opt
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
	

if __name__ == '__main__':
	menu = {'q':"quit","1":"get symbol","2":"input place","3":"input width","4":"input height","p":"print"}
	while(True):
		for key in menu:
			print("--",key," - ",menu[key])
		choce = input("your choce:")
		if not choce in menu:
			print(" error choce" )
			continue
			
		if choce in ('q','Q'): break
		
		elif choce in  ('p','P'):
			print()
			print("=>")
			rect()
			print("=>")
			print()
			
		elif choce == '1':
			text = input('input simbol :').strip()
			if len(text) > 0:
				opt['sym'] = text[0]
			else:
				opt['sym'] = ' '
				
		elif choce == '2':
			try:
				opt['place'] = int( input('input place :') )
			except ValueError:
				print("eroor : not number")
				
		elif choce == '3':
			try:
				opt["width"] =int( input('input width :') )
			except ValueError:
				print("eroor : not number")
				
		elif choce == '4':
			try:
				opt["height"] =int( input('input height :') )
			except ValueError:
				print("eroor : not number")
		#else: print(" error choce" )

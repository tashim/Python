'''
Created on Nov 22, 2015

@author: eimad
'''

def fib(n):
	a1=0
	a2=1
	a_sum=0

	n = int(n)
	i = 1

	if (n<=0):
		print ("this could not an element in the fibonachi series")
	else:
		while (i<=n):
			a_sum = a1 + a2
			a1 = a2
			a2 = a_sum
			print('i=',i,' f=',a2)
			i = i + 1
		#print(a_sum)
	return a_sum
    
def nn(n):
	if n == 0:
		return 0
	ret =  nn(n-1)            
	if ret == 0:
		return n
	return n*ret
        
        
if __name__ == '__main__':
	n =3
	print ("a[%d] = %d" % (n,nn(n)))
	print ("a[%d] = %d" % (n,fib(n)))

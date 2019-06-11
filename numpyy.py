import numpy as np
import sys
inputfile = sys.argv[1]
n = np.asarray([[0, 9, 9, 9, 3 , 4]])
print(n[0][1:5])
p = [[]]
p[0].append(1)
print(np.asarray(p))
m = np.asarray([[1,2],[3,4],[5,6]])
x = m[:,1]
print(np.sum(m,axis = 0))
c = int(0.9*5)
print(c)
s = 'stringgg7y'
print(s.rfind('g'))
if(inputfile.rfind('/')== -1):
	print(inputfile[0:inputfile.rfind('.')])
else:
	print(inputfile[1+inputfile.rfind('/'):inputfile.rfind('.')])


# #!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys


filepath = './observations.txt'

# Read data from the file
with open(filepath, 'r') as f:
    data = f.read()


data = data.split()
mode = sys.argv[1]
n_iter = sys.argv[2]

X = np.zeros(shape=(len(data),1))
# parameter vector (p, p1, p2)
theta = np.zeros(shape=(3,1))

if mode == 'uniform':
    theta[0] = 0.5
    theta[1] = 0.5
    theta[2] = 0.5
else:
    theta = np.random.rand(3,1)

print theta
N = len(data)
# No of heads, tails
H = 0
T = 0
print len(data)
for i in xrange(0,len(data)):
    if data[i]=='H':
        H += 1
        X[i] = 1
    else:
        T += 1
        X[i] = 0

print X.shape
# expected value of coin choice variable zi
expz = np.zeros((len(data),1))
print expz.shape

for i in range(int(n_iter)):
    x = np.power(theta[1], X)
    y = np.power((1-theta[1]), (1-X))
    num = theta[0] * (x * y)
    den = num + (1-theta[0])*np.power(theta[2], X)*np.power((1- theta[2]),(1-X))
    expz = num/den
    theta[0] = np.sum(expz)/N
    theta[1] = np.dot(X.T, expz)/float(np.sum(expz))
    x = np.sum(X) - np.dot( X.T, expz)
    y = N - np.sum(expz)
    theta[2] = x/float(y)
    print theta[0], theta[1], theta[2]

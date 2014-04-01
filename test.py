import os, sys
for i in range(100):
    print(str(i)+'1.txt')
    testing = open(str(i)+'1.txt','r')
    print(testing.readlines())

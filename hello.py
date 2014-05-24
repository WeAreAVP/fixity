#/usr/bin/env python

from time import sleep
from random import random
from threading import Thread, local

data = local()

def bar():
    print "I'm called from", data.v

def foo():
    bar()

class T(Thread):
    def run(self):
        sleep(random())
        data.v = self.getName()   # Thread-1 and Thread-2 accordingly
        sleep(1)
        foo()
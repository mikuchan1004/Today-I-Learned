# import fn.fn_15_1 
import fn.fn_15_1 as fn1

# a = fn.fn_15_1.add(1, 2)
a = fn1.add(1, 2)
print(a)

from fn.fn_15_1 import add as addd, sub
b = sub(3, 2)
print(b)

import random
print(random.random())

# from random import random
from random import random as rand
# print(random())
print(rand())

from fn.fn_15_1 import Hero
h = Hero()
h.attack()

import urllib.request 
response = urllib.request.urlopen('http://google.co.kr')
print(response.read().decode('utf-8'))


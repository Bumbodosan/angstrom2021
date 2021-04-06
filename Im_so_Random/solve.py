from pwn import remote
from itertools import combinations, chain
from factordb.factordb import FactorDB

'''
When we request a random number we get the result from two generators multiplied together. 
The insight is that these numbers are small (16 digits) so they are easy to factorize.
Using the factors we can generate all 8 digit numbers that multiply to the next random number (the 8 digit numbers are the current seeds)
and once we find those numbers we can predict the random generators. 
'''

def get_next(n):
    DIGITS = 8
    return int(str(n**2).rjust(DIGITS * 2, "0")[DIGITS // 2 : DIGITS + DIGITS // 2]) 

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

def get_seeds(rand, target):
    f = FactorDB(rand)
    f.connect()
    factors = f.get_factor_list()
    for p in powerset(range(len(factors))):
        n1 = 1
        for i in p:
            n1 *= factors[i]
        n2 = 1
        for i in range(len(factors)):
            if i not in p:
                n2 *= factors[i]
        if len(str(n1)) == len(str(n2)) == 8 and get_next(n1) * get_next(n2) == target:
            return n1, n2

def skip_question(r):
    r.recvuntil("?")


r = remote("crypto.2021.chall.actf.co", "21600")
skip_question(r)

r.sendline("r")
first_random = int(r.recvline().decode().strip())

skip_question(r)

r.sendline("r")
second_random = int(r.recvline().decode().strip())

n1, n2 = get_seeds(first_random, second_random)
n1, n2 = get_next(n1), get_next(n2)

skip_question(r)
r.sendline("g")
skip_question(r)
n1, n2 = get_next(n1), get_next(n2)
r.sendline(str(n1 * n2))
skip_question(r)
r.sendline(str(get_next(n1) * get_next(n2)))

print(r.recvall().decode().strip())

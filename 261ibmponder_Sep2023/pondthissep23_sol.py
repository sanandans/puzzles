'''
My IBM Ponder This September '23 challenge main, additional, and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/September2023.html
Sanandan Swaminathan, submitted August 31, 2023

The main and additional questions are small enough that the answers can be found
just by doing modular or even subtraction GCD (or using gmpy2 or sympy gcd functions),
and running through the recurrence. However, this wouldn't scale for the bonus *.
I looked at more terms for the given a1 = 11 example and one pattern emerged. Once
we reach a (an, n+1) pair that has gcd > 1 (and prime), and an is twice n+1, and we get
gcd = 1 with a(n+1) and n+2, their difference is an invariant until we reach the next
gcd > 1 (since both numbers keep increasing by 1 until then). If that difference is prime,
that difference itself seems to be the n where the next prime will occur. We can see this
mathematically too. Thus, when we hit gcd = 1, and difference prime, we can hop to next
location immediately. If gcd = 1 and difference is composite, we can stick to the slow
method of checking gcd for each step of 1 until we get gcd > 1. For the main and additional
questions, this improvement sufficed for both parts to complete instantaneously. For the
additional question, it starts with a1=1, and tries to find some d(n) > 1 that is non-prime.
But I cap it until an reaches a million, and try with the next higher a1. The cap is there
to avoid interminable search with a given a1. If an has become too large, it is quite unlikely
that we would find a non-prime d(n) later.
While the main and additional parts completed instantaneously, it took about an hour to find
the 100th occurrence of 5. Then it became progressively slower, as expected. So, the approach
obviously would be too slow for the bonus * question (200th occurrence of 5). We would need
to check if a(n) - (n+1) is prime for very large values; worse, if it was non-prime, we would
need to keep checking if gcd becomes more than 1 at each increment.
So I researched and found a nice paper on this subject:
https://cs.uwaterloo.ca/journals/JIS/VOL11/Rowland/rowland21.pdf
Once a(n) reached 3n (with a gcd > 1 between a(n-1) and n), then it's clear that we can find
the next prime p by finding the smallest prime factor of 2n - 1. Moreover, we can increment n by
(p-1)/2 to reach the next n. The only expensive part in this is to find the lowest prime factor
of very large 2n - 1. I check for factors 3 and 5 inline, and then check for factors in a small
sieve (primes below 10000). I could but don't check only upto the square root because the root
operation makes it slower for large numners. If a prime factor is not found in the sieve, I call
sympy's primefactors() function and take the lowest from the returned list.
Looking at primes found until 100th occurrence of 5, we see that the sequence has increasingly
large primes (large prime over twice the previous largest prime), and interspersed with much smaller
primes (though some intermediate primes get a bit large). So, this mixed procedure to find smallest
prime factor works well. With this procedure, the 200th occurrence of 5 for the bonus * was found
in about 90 secs. The runtime for sympy.primefactors() for very large n can be a bit unpredictable.
I guess it uses Pollard-Rho-Brent type of algo with probabilistic component.
This obviously works for the much smaller sized main question too.
'''

import sympy
import gmpy2
from datetime import datetime
#import math
#from sympy import factorint

#build small prime sieve
PRIME_STORE_LIM = 10000
prime_sieve = []
prime_sieve.append(2)
for i in range(3,PRIME_STORE_LIM,2):
    iroot = int(i**0.5) + 1
    not_prime = False
    for j in prime_sieve:
        if j >= iroot:
            break
        elif i%j == 0:
            not_prime = True
            break
    if not_prime == False:
        prime_sieve.append(i)
#remove prime 2 as it can't be factor of 2n-1, and treat 3 and 5 inline during processing
prime_sieve.remove(2)
prime_sieve.remove(3)
prime_sieve.remove(5)

'''
Try to get the smallest prime factor fast. First try with the small prime sieve.
Don't bother with only checking upto square root of the input number since finding
square root itself costs. For this specific problem we're better off going through
the small prime sieve. If small primes sieve don't give the answer, call sympy.primefactors()
and take the smallest from the returned list.
'''
def smallest_prime_factor(x):
    for prime in prime_sieve:
        if x%prime == 0:
            return prime
    return(sympy.primefactors(x)[0])

SEARCHTERM = 5
SEARCHLIM = 200 #10 for main, 200 for bonus *
searchcnt = 0
an = 531
n = 1
solfound = False
print(datetime.now(), "SEARCH START: a(1) =", an, "Starting n+1 =", n+1, "SEARCHTERM =", SEARCHTERM, \
      "Number of occurrences needed =", SEARCHLIM)
while True:
    #first get to a(n) = 3*n to switch to Rowland's method of skipping 1's
    n += 1
    gcdval = gmpy2.gcd(an,n)
    if gcdval == SEARCHTERM:
        searchcnt += 1
        if searchcnt == SEARCHLIM: #not going to happen so soon but keep it for completeness
            print(datetime.now(), "SEARCH END", n, an, gcdval)
            break
    an += gcdval

    '''
    Switch to Rowland's method of skipping 1's. The gcdval != 1 check below is not really
    going to be necessary for problems of this size. It's there for completeness. For example,
    in Rowland's sequence, a1 = 7. Then, a(3) = 9 = 3*3, which means a(n) = 3*n though the gcd
    of a2 = 8 and n = 3 is 1. We only want the a(n) = 3*n situation when gcd > 1. Once we reach
    such a point, the rest of the sequence will stay odd prime.
    '''
    if an == 3*n and gcdval != 1:
        print(datetime.now(), "a(n) reached 3n", an, n, searchcnt)
        while True:
            x = (2*n) -1
            if x%3 == 0:
                n += 1 # advance n by (3-1)/2
            elif x%5 == 0:
                n += 2 # advance n by (5-1)/2
                searchcnt += 1
                if searchcnt%10 == 0: #monitor progress for large searches
                    print(datetime.now(), n, searchcnt)
                if searchcnt == 10: #main question
                    print(datetime.now(), "MAIN ANSWER: Value of n is", n)
                if searchcnt == SEARCHLIM:
                    print(datetime.now(), "SEARCH END: Value of n is", n)
                    solfound = True
                    break
            else:
                n += (smallest_prime_factor(x) - 1)//2
        if solfound == True:
            break

#main's additional question
astart = 0
SEARCH_CAP = 1000000 #how far to go with an a1 before restarting with a new a1
solfound = False
while True:
    astart += 1
    an = astart
    nplusone = 2
    while an < SEARCH_CAP:
        gcdval = gmpy2.gcd(an, nplusone)
        if gcdval == 1:
            diff = an - nplusone
            if gmpy2.is_prime(diff) == True:
                nplusone = diff
                an = 2*nplusone
            else:
                nplusone += 1
                an += 1
        elif gmpy2.is_prime(gcdval) == False:
            print(datetime.now(), "Additional question's answer: k=", astart, \
                  "n =", nplusone, "Non-prime, > 1 gcd =", gcdval, \
                  "a(n) =", an, "a(n+1) =", an+gcdval)
            solfound = True
            break
        else:
            nplusone += 1
            an += gcdval
    if solfound == True:
        break


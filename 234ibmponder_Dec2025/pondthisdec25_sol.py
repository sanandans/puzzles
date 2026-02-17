'''
My IBM Ponder This December '25 challenge main and bonus * solutions
https://research.ibm.com/blog/ponder-this-december-2025
Old URL: https://research.ibm.com/haifa/ponderthis/challenges/December2025.html
Sanandan Swaminathan, submitted December 1, 2025

The largest prime sum that we need to deal with is at most 2n more than the
n'th odd prime. Using the very rough estimates from the prime number theorem -
the n'th prime is roughly n * ln(n), and number of primes less than a given
number x is roughly x/ln(x), we see that we are dealing with roughly 105-110
million primes in the case of the main puzzle, and roughly 1.1 billion primes
in the bonus puzzle. The memory footptint is not big for the main puzzle and
not too bad for the bonus puzzle. The primes would be in ascending order, so
all we need to do is count the number of primes in the list reachable from each
prime in the list. This is just a linear operation. If prime x is at index i,
and prime y at index j is the first prime > x + 2n (or j goes beyond the list),
then the count of prime sums with x as the base is j - i - 1. Also, for the next
prime z (larger than x) at index i+1, the search can continue from the current
search index j since primes from index i+2 through j-1 are already reachable
from z. Of course, this approach assumes that duplicate sums are allowed, as is
the case in the given example where f(5) = 16. This approach is faster than doing
a binary search to find the min index where a prime becomes unreachable (even though
the lower bound of the binary search would keep increasing as we find the desired
count for each prime). The program completes in about 15 seconds for the main puzzle,
and takes about 3 minutes for the bonus puzzle.
Answers:
f(10^8) = 972989871151789
f(10^9) = 87105187375692805
'''

import primesieve
from datetime import datetime

def count_prime_sums(N):
    max_even = N * 2 #max even number
    #generate and store the first N odd prime numbers in order
    primes_for_search = primesieve.n_primes(N + 1)[1:]
    #extend the list, in order, with primes between the max prime so far and that max prime + 2N
    primes_for_search.extend(primesieve.primes(primes_for_search[-1] + 1, primes_for_search[-1] + max_even))
    tot_count = 0
    j = 0
    primelist_len = len(primes_for_search)
    #linear search for reachable counts
    for i in range(N):
        reachable_max = primes_for_search[i] + max_even
        while j < primelist_len and primes_for_search[j] <= reachable_max:
            j += 1
        tot_count += j - i - 1
    return tot_count

for exp in (8, 9):
    print(datetime.now(), "For n = 10^"+str(exp))
    print("ANSWER: Number of prime sums: f(10^{}) = {}".format(exp, count_prime_sums(10**exp)))
print(datetime.now(), "done")

'''
My IBM Ponder This March '24 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/March2024.html
Sanandan Swaminathan, submitted March 3, 2024

The main puzzle, X1000, can be found by running a loop for about
5 minutes. Trying higher targets, we get to see some patterns:
Mainly, new record sequence lengths are set with a0 as multiple
of 3. This also means that we don't need to check the sum of a0
and multiple-of-3 triangular numbers since those sums will also be
composite (multiple of 3).
Further, for record a0's, we see that a0 mod5 has remainder of 0 or 4.
So, we can try a0's that are 0 or 9 mod(3*5).
Record a0's seem to have remainders 0, 4 or 6 mod 7.
So, we can try a0's that are 0, 39, 60, 69, 84, 90 mod (3*5*7).
Record a0's seem to have remainders 0, 1, 5, 8, 10 mod 11.
So, we can try a0's that are 0, 60, 144, 165, 195, 210, 294, 375, 384,
459, 489, 525, 594, 615, 690, 714, 720, 804, 819, 825, 879, 924, 945,
984, 1035, 1050, 1089, 1110, 1119, 1134 mod(3*5*7*11).
To avoid repeating a prime check, we have to store primes. Tried with
marking primes in a bitarray, but memory consumption was still too high
for X2024. Switched to using a dict to store found primes.

Program found the answer 115192665 as the smalles a0 for X1000 quickly,
in about 18 seconds. This a0 actually gives a sequence that has 1051 terms,
so 115192665 is the smallest a0 upto X1051.
Program ran for several hours to find smallest a0 for X2024 = 117778830159.
This a0 actually gives a sequence that has 2152 terms, so 117778830159 is
the smallest a0 upto X2152.
'''

import gmpy2
from datetime import datetime
#from sympy import primerange
#from bitarray import bitarray

N = 1000 # 1000 for main puzzle, 2024 for bonus * puzzle
print(datetime.now(), "Start: N =", N)
prime_sieve = {} #dict to store primes found
tri_nums_notdiv3 = [] #list to store triangular nums that are not 0mod3
tri_num = 0
for i in range(1, N): #we only need to go upto N-1
    tri_num += i
    if tri_num%3 != 0:
        tri_nums_notdiv3.append(tri_num)

#Only used for final check of answer.
#Check prime without using gmpy2.is_prime() since that might be
#probabilistic.
def iscomp(x):
    if x%2 == 0:
        return True
    i = 3
    while i < (x**0.5) + 1:
        if x%i == 0:
            return True
        i += 2
    return False

#Only used to check sequence length of final answer.
def actual_sequence_length(x0):
    seq_len = 0
    addend = 0
    while True: #until we get a prime in the sequence
        x0 += addend
        if iscomp(x0) == False:
            return seq_len
        else:
            seq_len += 1
        addend += 1

base_a0 = 0
max_len = 0 #longest sequence length
found = True
progress_marker = 1000000000 #counter for logging

while True:
    if base_a0 > progress_marker:
        print(datetime.now(), base_a0, max_len, N)
        #remove old primes
        for key in list(prime_sieve):
            if key < base_a0:
                del prime_sieve[key]
        progress_marker += 1000000000
    #based on patterns, check only certain a0 values
    base_a0 += 1155
    for rem in (0, 60, 144, 165, 195, 210, 294, 375, 384, 459, 489, 525, \
                594, 615, 690, 714, 720, 804, 819, 825, 879, 924, 945, \
                984, 1035, 1050, 1089, 1110, 1119, 1134):
        found = True
        a0 = base_a0 + rem
        #seq_len is used only to check if we've got a new record length
        #It does not show the actual sequence length since we skip
        #tringular nums that are guaranteed to result in composites
        seq_len = 1 #every a0 is 0mod3, hence composite
        for i in tri_nums_notdiv3: #add non 0mod3 triangular nums
            a = a0 + i
            if a in prime_sieve: #existing prime
                found = False
                break
            elif gmpy2.is_prime(a) == True: #new prime
                prime_sieve[a] = 1
                found = False
                break
            else:
                seq_len += 1
        if seq_len > max_len: #new record sequence
            print(datetime.now(), a0, seq_len)
            max_len = seq_len
        #if sequence has progressed through all necessary triangular
        #sums, we are done.
        if found == True:
            actual_len = actual_sequence_length(a0)
            if actual_len < N:
                print(datetime.now(), "Error:", a0, actual_len, N)
            else:
                print(datetime.now(), "Found answer:", a0, actual_len, N)
            break
    if found == True:
        break

print(datetime.now(), "End")

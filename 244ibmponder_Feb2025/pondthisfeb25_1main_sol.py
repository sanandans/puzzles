'''
My IBM Ponder This February '25 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/February2025.html
Sanandan Swaminathan, submitted February 2, 2025

Note: Separate files for main and bonus * puzzles.

Initially, for the main puzzle, each 5-digit prime is categorized into a bucket based on its digit sum. Partial matches of
each prime are also categorized (patterns that will be used during the search). For this purpose, I use an array of
dictionaries, where each array index corresponds to a digit sum. The dictionary keys are tuples containing the full primes
or portions of the primes. These tuples are patterns that serve the search process or to determine if the current path
should be aborted. The dictionary values are lists of tuples of the primes that match the given key (for a given digit sum).
Additionally, primes that qualify for the bottom row are stored in separate lists, categorized by digit sum. These are
primes that only contain digits 1, 3, 7, 9. For each digit sum, another array of lists is populated with primes that
qualify for the rightmost column, bucketed by digit sum and unit place digit 1, 3, 7 or 9. For each prime, the frequencies
of its digits are also stored.

Once the quick initial setup is done for all 5-digit primes, the search is started for each digit sum. The grid is filled
with primes in a specific order, trying to use the appropriate match pattern at each step. Also, as each prime is filled,
checks are done using the partial match patterns to ensure that the partial rows/columns/diagonals which are touched by the
current prime are all still potential primes. If any match fails, that prime is discarded, and the next qualifying one is
tried. I played around with the sequence of filling the grid. The bottom row followed by the rightmost column is a
reasonable starting point due to the small number of qualifying primes. This lets us narrow the top right to bottom left
diagonal based on the match of first and last digits. The top row and leftmost column are also slightly restricted since
they can't have a 0 digit. But this didn't seem to make a significant difference, and their match pattern would contain
only one digit at this stage. This is followed by filling top left to bottom right diagonal, then row 3 (0-indexed), column
3, row 2, column 2. The remaining cells are now determined (if the patterns match primes). When a grid is completed, the
distinct primes are evaluated for cost. If the cost is less than the current minimum, then the new minimum cost and grid
(tuple of 5 row primes) are saved. Similarly, if the cost is more than the current maximum, then the new maximum cost and
grid (tuple of 5 row primes) are saved.

The program completed immediately for the main puzzle, and printed the following solution (it's only required to find one
solution):

Minimum cost: 61
A square with minimum cost...
2 8 6 4 3 
8 9 0 5 1 
6 0 7 3 7 
4 5 3 2 9 
3 1 7 9 3 
Sum of digits in row/col/diagonal (value of A in above square): 23

Maximum cost: 488
A square with maximum cost...
1 7 3 3 3 
4 1 8 1 3 
3 3 3 1 7 
2 3 2 9 1 
7 3 1 3 3 
Sum of digits in row/col/diagonal (value of A in above square): 17

'''

import sympy
from datetime import datetime
import math
import copy

print(datetime.now())
N = 5
sum_arr_len = (9 * N) + 1
sum_array_lastrowcol = [None]*sum_arr_len
for i in range(sum_arr_len):
    sum_array_lastrowcol[i] = []
lastcol_arr = [[[] for _ in range(10)] for _ in range(sum_arr_len)]
dig_freq_dict = dict()
primecnt=0
partial_prime_matches = [None]*sum_arr_len
for i in range(sum_arr_len):
    partial_prime_matches[i] = dict()

for num in range(10**(N-1), 10**N):
    if sympy.isprime(num):
        primecnt+=1
        num1 = num
        templist = []
        i = 0
        lastrowcol = True
        tempsum = 0
        while i < N:
            dig = num1%10
            if dig in (0,2,4,5,6,8):
                lastrowcol = False
            tempsum += dig
            templist.insert(0, dig)
            num1 //= 10
            i += 1
        if lastrowcol == True:
            sum_array_lastrowcol[tempsum].append(tuple(templist))
            lastcol_arr[tempsum][templist[-1]].append(tuple(templist))
        
        dig_freq_arr = [0]*10
        for digit in templist:
            dig_freq_arr[digit] += 1
        dig_freq_dict[tuple(templist)] = copy.deepcopy(dig_freq_arr)
        
        #for cells 0, 4
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cell 4
        pattern = [-1]*N
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))
        
        #for cells 1, 4
        pattern = [-1]*N
        pattern[1] = templist[1]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 2, 4
        pattern = [-1]*N
        pattern[N-3] = templist[N-3]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))
        
        #for cells 3, 4
        pattern = [-1]*N
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 0, 3, 4
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))
        
        #for cells 1, 3, 4
        pattern = [-1]*N
        pattern[1] = templist[1]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))
        
        #for cells 2, 3, 4
        pattern = [-1]*N
        pattern[2] = templist[2]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 0, 1, 3, 4
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[1] = templist[1]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 0, 2, 3, 4
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[2] = templist[2]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))
        
        #for cells 1, 2, 3, 4
        pattern = [-1]*N
        pattern[1] = templist[1]
        pattern[N-3] = templist[N-3]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #to confirm a completed number belongs to this A bucket
        partial_prime_matches[tempsum][tuple(templist)] = [tuple(templist)]

min_cost = math.inf
min_nums = None
max_cost = 0
max_nums = None

for rowsum in range(sum_arr_len):
    for bottomnum in sum_array_lastrowcol[rowsum]:
        for lastcol in lastcol_arr[rowsum][bottomnum[-1]]:
            if (lastcol[0],-1,-1,-1,bottomnum[0]) not in partial_prime_matches[rowsum]:
                continue
            for diag_tr_bl in partial_prime_matches[rowsum][(lastcol[0],-1,-1,-1,bottomnum[0])]:
                if (-1,-1,-1,diag_tr_bl[3],bottomnum[1]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,diag_tr_bl[2],-1,bottomnum[2]) not in partial_prime_matches[rowsum] or \
                   (-1,diag_tr_bl[1],-1,-1,bottomnum[3]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,-1,diag_tr_bl[1],lastcol[1]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,diag_tr_bl[2],-1,lastcol[2]) not in partial_prime_matches[rowsum] or \
                   (-1,diag_tr_bl[3],-1,-1,lastcol[3]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,diag_tr_bl[2],-1,lastcol[4]) not in partial_prime_matches[rowsum]:
                    continue
                for diag_tl_br in partial_prime_matches[rowsum][(-1,-1,diag_tr_bl[2],-1,lastcol[4])]:
                    if (diag_tl_br[0],-1,-1,-1,lastcol[0]) not in partial_prime_matches[rowsum] or \
                       (diag_tl_br[0],-1,-1,-1,bottomnum[0]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tl_br[1],-1,diag_tr_bl[1],lastcol[1]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tl_br[1],-1,diag_tr_bl[3],bottomnum[1]) not in partial_prime_matches[rowsum] or \
                       (-1,-1,diag_tl_br[2],-1,lastcol[2]) not in partial_prime_matches[rowsum] or \
                       (-1,-1,diag_tl_br[2],-1,bottomnum[2]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tr_bl[3],-1,diag_tl_br[3],lastcol[3]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tr_bl[1],-1,diag_tl_br[3],bottomnum[3]) not in partial_prime_matches[rowsum]:
                        continue
                    for row3 in partial_prime_matches[rowsum][(-1,diag_tr_bl[3],-1,diag_tl_br[3],lastcol[3])]:
                        if (diag_tl_br[0],-1,-1,row3[0],bottomnum[0]) not in partial_prime_matches[rowsum] or \
                           (-1,-1,diag_tr_bl[2],row3[2],bottomnum[2]) not in partial_prime_matches[rowsum]:
                            continue
                        for col3 in partial_prime_matches[rowsum][(-1,diag_tr_bl[1],-1,row3[3],bottomnum[3])]:
                            if (diag_tl_br[0],-1,-1,col3[0],lastcol[0]) not in partial_prime_matches[rowsum] or \
                               (-1,-1,diag_tr_bl[2],col3[2],lastcol[2]) not in partial_prime_matches[rowsum]:
                                continue
                            for row2 in partial_prime_matches[rowsum][(-1,-1,diag_tr_bl[2],col3[2],lastcol[2])]:
                                if (diag_tl_br[0],-1,row2[0],row3[0],bottomnum[0]) not in partial_prime_matches[rowsum] or \
                                   (-1,diag_tl_br[1],row2[1],row3[1],bottomnum[1]) not in partial_prime_matches[rowsum]:
                                    continue
                                col0 = partial_prime_matches[rowsum][(diag_tl_br[0],-1,row2[0],row3[0],bottomnum[0])][0]
                                col1 = partial_prime_matches[rowsum][(-1,diag_tl_br[1],row2[1],row3[1],bottomnum[1])][0]
                                if (col0[0],col1[0],-1,col3[0],lastcol[0]) not in partial_prime_matches[rowsum] or \
                                   (col0[1],col1[1],-1,col3[1],lastcol[1]) not in partial_prime_matches[rowsum]:
                                    continue
                                row0 = partial_prime_matches[rowsum][(col0[0],col1[0],-1,col3[0],lastcol[0])][0]
                                row1 = partial_prime_matches[rowsum][(col0[1],col1[1],-1,col3[1],lastcol[1])][0]
                                if (row0[2],row1[2],row2[2],row3[2],bottomnum[2]) not in partial_prime_matches[rowsum]:
                                    continue
                                primes_set = set()
                                primes_set.add(row0)
                                primes_set.add(row1)
                                primes_set.add(row2)
                                primes_set.add(row3)
                                primes_set.add(bottomnum)
                                primes_set.add(col0)
                                primes_set.add(col1)
                                primes_set.add((row0[2],row1[2],row2[2],row3[2],bottomnum[2]))
                                primes_set.add(col3)
                                primes_set.add(lastcol)
                                primes_set.add((diag_tr_bl))
                                primes_set.add(diag_tl_br)
                                cost = 0
                                for dig in range(10):
                                    dig_cnt = 0
                                    for primenum in primes_set:
                                        dig_cnt += dig_freq_dict[primenum][dig]
                                    if dig_cnt > 1:
                                        cost += (dig_cnt*(dig_cnt-1))//2
                                if cost < min_cost:
                                    min_cost = cost
                                    min_nums = (row0,row1,row2,row3,bottomnum)
                                if cost > max_cost:
                                    max_cost = cost
                                    max_nums = (row0,row1,row2,row3,bottomnum)
                                                        
print(datetime.now(), "Answer for N =", N)
print("Minimum cost:", min_cost)
print("A square with minimum cost...")
for row in min_nums:
    for col in row:
        print(col, end = " ")
    print()
print("Sum of digits in row/col/diagonal (value of A in above square):", sum(min_nums[0]))
print()
print("Maximum cost:", max_cost)
print("A square with maximum cost...")
for row in max_nums:
    for col in row:
        print(col, end = " ")
    print()
print("Sum of digits in row/col/diagonal (value of A in above square):", sum(max_nums[0]))

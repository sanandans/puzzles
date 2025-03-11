'''
My IBM Ponder This February '25 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/February2025.html
Sanandan Swaminathan, submitted February 2, 2025

Note: Separate files for main and bonus * puzzles.

Initially, each 6-digit prime is categorized into a bucket based on its digit sum. Partial matches of
each prime are also categorized, patterns that will be used during the search). For this purpose, I use an
array of dictionaries, where each array index corresponds to a digit sum. The dictionary keys are tuples
containing the full primes or portions of the primes. These tuples are patterns that serve the search process
or to determine if the current path should be aborted. The dictionary values are lists of tuples of the primes
that match the given key (for a given digit sum). Additionally, primes that qualify for the bottom row are
stored in separate lists, categorized by digit sum. These are primes that only contain digits 1, 3, 7, 9. For
each digit sum, another array of lists is populated with primes that qualify for the rightmost column,
bucketed by digit sum and unit place digit 1, 3, 7 or 9. For each prime, the frequencies of its digits are
also stored.

Once the quick initial setup is done for the 68906 six-digit primes, the search is started for each digit sum.
The grid is filled with primes in a specific order, trying to use the appropriate match pattern at each step.
Also, as each prime is filled, checks are done using the partial match patterns to ensure that the partial
rows/columns/diagonals which are touched by the current prime are all still potential primes. If any match
fails, that prime is discarded, and the next qualifying one is tried. I played around with the sequence of
filling the grid. The bottom row followed by the rightmost column is a reasonable starting point due to the
small number of qualifying primes. This lets us narrow the top right to bottom left diagonal based on the
match of first and last digits. The top row and leftmost column are also slightly restricted since they
can't have a 0 digit. But this didn't seem to make a significant difference, and their match pattern would
contain only one digit at this stage. Filling a different row or column as the 4th step seemed better as the
match pattern would contain two filled digits. However, filling the top left to bottom right diagonal as the
4th step gave the advantage of checking all partial rows and columns early in the process despite having a
match pattern with only one digit filled. Subsequently, filling rows and columns alternately based on the best
match pattern available at each step seemed like a reasonable way to proceed. Of course, any row/column touched
by the prime being added is checked with appropriate match patterns at each step to ensure that those
rows/columns are all still potentially prime. The fill order I settled on is: 6th row (1-indexed), 6th column,
top right to bottom left diagonal, top left to bottom right column, 5th row, 5th column, 4th row, 4th column,
3rd row. Since there is only one missing digit at this stage in the first and second columns, those columns are
fixed (for the given digit sum), subject to the corresponding first and second rows still being potentially
prime. This also determines the missing top two digits of the third column, subject to the third column still
being prime. This completes the grid. When a grid is completed, the distinct primes are evaluated for cost.
If the cost is less than the current minimum, then the new minimum cost and grid (tuple of 6 row primes) are
saved. Similarly, if the cost is more than the current maximum, then the new maximum cost and grid (tuple of
6 row primes) are saved.

While a similar procedure completes the main puzzle (N = 5) immediately, and is fast for many digit sums for
N = 6, it's still quite slow for some digit sums for N = 6. Digit sums can only be even since the bottom row
(and rightmost column) has 6 odd digits. However, for some of those digit sums, a large number of primes have
those sums, like in the case of digit sums 22, 26, 28 and 32. So, I ran the program in parallel in batches of
digit sums, with some runs covering only one digit sum. While many batches completed relatively quickly, the
worst run was for digit sum 28 which took many hours. High electricty bill from my humble laptop expected!
And the answers were in digit sum 28.

I toyed a bit with the idea of predicting best-case lower and upper cost bounds for a partially filled grid, to
detect early if neither the current minimum nor the maximum would be improved when the grid is fully filled.
But I couldn't come up with a dependable, safe scheme for such a prediction. Perhaps the considerable usage of
hashing is a big overhead, and maybe multi-dimensional arrays without using dictionaries would have made some
difference to the performance (though probably not by much since a large number of multi-dimensional array jump
computations would occur instead of hashing). I also coded up a trie-based solution, but that didn't improve
the runtime for digit sums like 28. I cythonized the program, but still no significant difference.

Answer found:

Minimal cost = 158 (A = 28 for all rows, columns, and both diagonals)

2, 7, 8, 2, 2, 7,

7, 1, 5, 1, 5, 9,

8, 9, 4, 4, 0, 3

2, 1, 4, 9, 9, 3

2, 1, 4, 9, 9, 3

7, 9, 3, 3, 3, 3

Maximal cost = 1310 (A = 28 for all rows, columns, and both diagonals)

3, 1, 3, 7, 7, 7,

3, 7, 3, 3, 3, 9,

5, 3, 9, 5, 3, 3,

9, 7, 3, 3, 3, 3,

5, 7, 7, 3, 3, 3,

3, 3, 3, 7, 9, 3

'''

import sympy
from datetime import datetime
#from collections import defaultdict
import math
import copy

print(datetime.now())
N = 6
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
            #sum_array_lastrowcol[tempsum].add(tuple(templist))
            sum_array_lastrowcol[tempsum].append(tuple(templist))
            lastcol_arr[tempsum][templist[-1]].append(tuple(templist))

        dig_freq_arr = [0]*10
        for digit in templist:
            dig_freq_arr[digit] += 1
        dig_freq_dict[tuple(templist)] = copy.deepcopy(dig_freq_arr)
        
        #for top right to bottom left diagonal, and check after diag tl to br
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for top left to bottom right diagonal
        pattern = [-1]*N
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 1,5
        pattern = [-1]*N
        pattern[1] = templist[1]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 2,5
        pattern = [-1]*N
        pattern[2] = templist[2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 3,5
        pattern = [-1]*N
        pattern[3] = templist[3]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 4,5
        pattern = [-1]*N
        pattern[4] = templist[4]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 0,4,5
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[4] = templist[4]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 1,4,5
        pattern = [-1]*N
        pattern[1] = templist[1]
        pattern[4] = templist[4]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 2,3,5
        pattern = [-1]*N
        pattern[2] = templist[2]
        pattern[3] = templist[3]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 0,3,4,5
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[3] = templist[3]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 1,3,4,5
        pattern = [-1]*N
        pattern[1] = templist[1]
        pattern[3] = templist[3]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 2,3,4,5
        pattern = [-1]*N
        pattern[2] = templist[2]
        pattern[3] = templist[3]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 0,2,3,4,5
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[2] = templist[2]
        pattern[3] = templist[3]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 0,1,3,4,5
        pattern = [-1]*N
        pattern[0] = templist[0]
        pattern[1] = templist[1]
        pattern[3] = templist[3]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))

        #for cells 1,2,3,4,5
        pattern = [-1]*N
        pattern[1] = templist[1]
        pattern[2] = templist[2]
        pattern[3] = templist[3]
        pattern[N-2] = templist[N-2]
        pattern[N-1] = templist[N-1]
        if tuple(pattern) not in partial_prime_matches[tempsum]:
            partial_prime_matches[tempsum][tuple(pattern)] = []
        partial_prime_matches[tempsum][tuple(pattern)].append(tuple(templist))
        
        #to confirm a completed number belongs to this A bucket
        #partial_prime_matches[tempsum][tuple(templist)].add(tuple(templist))
        partial_prime_matches[tempsum][tuple(templist)] = [tuple(templist)]

min_cost = math.inf
min_nums = None
max_cost = 0
max_nums = None

for rowsum in range(14,15): #change to desired range of rowsums, answer found with rowsum 28 (runs long for 28!)
    print(datetime.now(), "Rowsum", rowsum, len(sum_array_lastrowcol[rowsum]),min_cost,min_nums,max_cost,max_nums)
    for bottomnum in sum_array_lastrowcol[rowsum]:
        #print(datetime.now(), bottomnum,min_cost,min_nums,max_cost,max_nums)
        for lastcol in lastcol_arr[rowsum][bottomnum[-1]]:
            if (lastcol[0],-1,-1,-1,-1,bottomnum[0]) not in partial_prime_matches[rowsum]:
                continue
            for diag_tr_bl in partial_prime_matches[rowsum][(lastcol[0],-1,-1,-1,-1,bottomnum[0])]:
                if (-1,-1,-1,-1,diag_tr_bl[1],lastcol[1]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,-1,diag_tr_bl[2],-1,lastcol[2]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,diag_tr_bl[3],-1,-1,lastcol[3]) not in partial_prime_matches[rowsum] or \
                   (-1,diag_tr_bl[4],-1,-1,-1,lastcol[4]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,-1,-1,diag_tr_bl[4],bottomnum[1]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,-1,diag_tr_bl[3],-1,bottomnum[2]) not in partial_prime_matches[rowsum] or \
                   (-1,-1,diag_tr_bl[2],-1,-1,bottomnum[3]) not in partial_prime_matches[rowsum] or \
                   (-1,diag_tr_bl[1],-1,-1,-1,bottomnum[4]) not in partial_prime_matches[rowsum]:
                    continue
                for diag_tl_br in partial_prime_matches[rowsum][(-1,-1,-1,-1,-1,bottomnum[5])]:
                    if (diag_tl_br[0],-1,-1,-1,-1,lastcol[0]) not in partial_prime_matches[rowsum] or \
                       (diag_tl_br[0],-1,-1,-1,-1,bottomnum[0]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tl_br[1],-1,-1,diag_tr_bl[1],lastcol[1]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tl_br[1],-1,-1,diag_tr_bl[4],bottomnum[1]) not in partial_prime_matches[rowsum] or \
                       (-1,-1,diag_tl_br[2],diag_tr_bl[2],-1,lastcol[2]) not in partial_prime_matches[rowsum] or \
                       (-1,-1,diag_tl_br[2],diag_tr_bl[3],-1,bottomnum[2]) not in partial_prime_matches[rowsum] or \
                       (-1,-1,diag_tr_bl[3],diag_tl_br[3],-1,lastcol[3]) not in partial_prime_matches[rowsum] or \
                       (-1,-1,diag_tr_bl[2],diag_tl_br[3],-1,bottomnum[3]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tr_bl[4],-1,-1,diag_tl_br[4],lastcol[4]) not in partial_prime_matches[rowsum] or \
                       (-1,diag_tr_bl[1],-1,-1,diag_tl_br[4],bottomnum[4]) not in partial_prime_matches[rowsum]:
                        continue
                    for row4 in partial_prime_matches[rowsum][(-1,diag_tr_bl[4],-1,-1,diag_tl_br[4],lastcol[4])]:
                            if (-1,-1,diag_tl_br[2],diag_tr_bl[3],row4[2],bottomnum[2]) not in partial_prime_matches[rowsum] or \
                               (-1,-1,diag_tr_bl[2],diag_tl_br[3],row4[3],bottomnum[3]) not in partial_prime_matches[rowsum] or \
                               (diag_tl_br[0],-1,-1,-1,row4[0],bottomnum[0]) not in partial_prime_matches[rowsum]:
                                continue
                            for col4 in partial_prime_matches[rowsum][(-1,diag_tr_bl[1],-1,-1,row4[4],bottomnum[4])]:
                                if (-1,-1,diag_tl_br[2],diag_tr_bl[2],col4[2],lastcol[2]) not in partial_prime_matches[rowsum] or \
                                   (-1,-1,diag_tr_bl[3],diag_tl_br[3],col4[3],lastcol[3]) not in partial_prime_matches[rowsum] or \
                                   (diag_tl_br[0],-1,-1,-1,col4[0],lastcol[0]) not in partial_prime_matches[rowsum]:
                                    continue
                                for row3 in partial_prime_matches[rowsum][(-1,-1,diag_tr_bl[3],diag_tl_br[3],col4[3],lastcol[3])]:
                                    if (diag_tl_br[0],-1,-1,row3[0],row4[0],bottomnum[0]) not in partial_prime_matches[rowsum] or \
                                       (-1,diag_tl_br[1],-1,row3[1],row4[1],bottomnum[1]) not in partial_prime_matches[rowsum]:
                                        continue
                                    for col3 in partial_prime_matches[rowsum][(-1,-1,diag_tr_bl[2],row3[3],row4[3],bottomnum[3])]:
                                        if (diag_tl_br[0],-1,-1,col3[0],col4[0],lastcol[0]) not in partial_prime_matches[rowsum] or \
                                           (-1,diag_tl_br[1],-1,col3[1],col4[1],lastcol[1]) not in partial_prime_matches[rowsum]:
                                            continue
                                        for row2 in partial_prime_matches[rowsum][(-1,-1,diag_tl_br[2],col3[2],col4[2],lastcol[2])]:
                                            if (diag_tl_br[0],-1,row2[0],row3[0],row4[0],bottomnum[0]) not in partial_prime_matches[rowsum] or \
                                               (-1,diag_tl_br[1],row2[1],row3[1],row4[1],bottomnum[1]) not in partial_prime_matches[rowsum]:
                                                continue
                                            col1 = partial_prime_matches[rowsum][(-1,diag_tl_br[1],row2[1],row3[1],row4[1],bottomnum[1])][0]
                                            col0 = partial_prime_matches[rowsum][(diag_tl_br[0],-1,row2[0],row3[0],row4[0],bottomnum[0])][0]
                                            if (col0[0],col1[0],-1,col3[0],col4[0],lastcol[0]) not in partial_prime_matches[rowsum] or \
                                               (col0[1],col1[1],-1,col3[1],col4[1],lastcol[1]) not in partial_prime_matches[rowsum]:
                                                continue
                                            row1 = partial_prime_matches[rowsum][(col0[1],col1[1],-1,col3[1],col4[1],lastcol[1])][0]
                                            row0 = partial_prime_matches[rowsum][(col0[0],col1[0],-1,col3[0],col4[0],lastcol[0])][0]
                                            if (row0[2],row1[2],row2[2],row3[2],row4[2],bottomnum[2]) not in partial_prime_matches[rowsum]:
                                                continue
                                            primes_set = set()
                                            primes_set.add(row0)
                                            primes_set.add(row1)
                                            primes_set.add(row2)
                                            primes_set.add(row3)
                                            primes_set.add(row4)
                                            primes_set.add(bottomnum)
                                            primes_set.add(col0)
                                            primes_set.add(col1)
                                            primes_set.add((row0[2],row1[2],row2[2],row3[2],row4[2],bottomnum[2]))
                                            primes_set.add(col3)
                                            primes_set.add(col4)
                                            primes_set.add(lastcol)
                                            primes_set.add(diag_tr_bl)
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
                                                min_nums = (row0,row1,row2,row3,row4,bottomnum)
                                            if cost > max_cost:
                                                max_cost = cost
                                                max_nums = (row0,row1,row2,row3,row4,bottomnum)
                                                        
print(datetime.now(), min_cost, min_nums, max_cost, max_nums)

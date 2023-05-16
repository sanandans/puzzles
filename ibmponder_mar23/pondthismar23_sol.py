'''
IBM Ponder This challenge and bonus *, Mar 23
https://research.ibm.com/haifa/ponderthis/challenges/March2023.html
Sanandan Swaminathan, submitted March 6, 2023

Main puzzle (largest number which is a 5-exception chained prime, where the chain starts with a single digit, the leftmost):
3733799911799539139382193991

I wrote a python program for the main puzzle. It does an iterative depth-first search for the answer, maintaining a list of only the nodes in the current path of the search (from the start node). Since prime numbers greater than 3 are of the form 1mod6 or 5mod6, I maintain a static list of digits that could potentially result in a prime when the digit is appended to the right of the number at that step. A primality check is done in the case of such candidates. Other digits are also tried as long as the number of non-prime exceptions has not exceeded the threshold. This continues until a number is reached where appending any digit would cause the number of exceptions to exceed the threshold.

Bonus "*" puzzle (largest number which is a 5-exception reverse chained prime, where the chain starts with a single digit, the rightmost):
996381323136248319687995918918997653319693967


For the bonus "*" question, I set some fixed lookups (lists, array) at the start of the program. Prime numbers greater than 3 have the form 1mod6 or 5mod6. If we add a digit to the left of a number, the new number's remainder mod6 will be 4 times the digit being added plus the previous number's remainder, mod6. From this, we can build a fixed list of digits that will lead to prime candidates (for each possible previous remainder). The remaining digits go into a list of non-prime digits (for each possible previous remainder mod6). With the fixed lists in place, I do a recursive depth-first search to find the largest 5-exception reverse chained prime, starting with the single rightmost digit 1, 3, 7 or 9. In the case of 1 or 3, that is the first exception. At each step, we know the digits that can be added that can lead to a prime potentially. Primality check is done for such candidates. If it turns out to be a non-prime, the exception count increases (as long as the exception max of 5 has not been reached). We also know the list of digits that can be added to make a non-prime (as long as the exception max of 5 has not been reached). The remainder mod6 for each new number formed is directly looked up from the fixed array. The only calculation to be done at every step is to form the new number, apart from the primality test for prime candidates.
'''

import math
from datetime import datetime
import gmpy2
#import sympy
#import scipy
#import numpy

largest_p=0
EXCEPTION_MAX=5
pot_primes = [[1,7],[],[3,9],[],[1,3,7,9],[]]
non_primes = [[0,2,3,4,5,6,8,9],[0,1,2,3,4,5,6,7,8,9],[0,1,2,4,5,6,7,8],[0,1,2,3,4,5,6,7,8,9],[0,2,4,5,6,8],[0,1,2,3,4,5,6,7,8,9]]

def recurs_find_largest(snum, non_prime_cnt, mod6_rem):
    largestp = snum
    temp_num = snum*10
    temp_rem = (mod6_rem*10)%6
    for i in pot_primes[temp_rem]:
        new_num = temp_num+i
        new_mod6_rem = (temp_rem+i)%6
        if gmpy2.is_prime(new_num) == False:
            np_cnt = non_prime_cnt+1
            if np_cnt <= EXCEPTION_MAX:
                p = recurs_find_largest(new_num, np_cnt, new_mod6_rem)
                if p > largestp:
                    largestp = p
        else:
            p = recurs_find_largest(new_num, non_prime_cnt, new_mod6_rem)
            if p > largestp:
                largestp = p

    if non_prime_cnt < EXCEPTION_MAX:
        for i in non_primes[temp_rem]:
            new_num = temp_num+i
            new_mod6_rem = (temp_rem+i)%6
            p = recurs_find_largest(new_num, non_prime_cnt+1, new_mod6_rem)
            if p > largestp:
                largestp = p
    return largestp

for start_num in range(1,10):
    print(largest_p,start_num,datetime.now())
    if start_num in (2,3,5,7):
        npcnt=0
    else:
        npcnt=1
    if npcnt > EXCEPTION_MAX:
        continue
    pnum = recurs_find_largest(start_num, npcnt, start_num%6)
    if pnum > largest_p:
        largest_p = pnum
     
print(largest_p, datetime.now())

''' iterative code
import math
from datetime import datetime
import gmpy2

children_matrix = [ [0,1,0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0,1], [0,0,0,0,0,0,0,0,0,0], [0,1,0,1,0,0,0,1,0,1], [0,0,0,0,0,0,0,0,0,0] ]

nodeList = []

class Node:
    def __init__(self, num, np_cnt, children_arr, next_child_pos, mod6_rem):
        self.num = num
        self.np_cnt = np_cnt
        self.children_arr = children_arr
        self.next_child_pos = next_child_pos
        self.mod6_rem = mod6_rem

largest_p = 0
EXCEPTION_MAX=5

def DFS_find_largestp():
    global largest_p
    for i in range(1,3):
        print(largest_p,i,datetime.now())
        if i in (2,3,5,7):
            temp_np_cnt = 0
        else:
            temp_np_cnt = 1
        if temp_np_cnt > EXCEPTION_MAX:
            continue
        temp_mod6_rem = i%6
        temp_rem = (i*10)%6
        nodeList.append(Node(i,temp_np_cnt,children_matrix[temp_rem],0,temp_mod6_rem))
        while len(nodeList) > 0:
            curr_node = nodeList[-1]
            if curr_node.next_child_pos > 9:
                if curr_node.num > largest_p:
                    largest_p = curr_node.num
                nodeList.pop(-1)
            else:
                for j in range(curr_node.next_child_pos,10):
                    curr_node.next_child_pos += 1
                    if (curr_node.children_arr[j] == 1):
                        temp_child_num = ((curr_node.num)*10)+j
                        temp_mod6 = ((curr_node.mod6_rem*10) + j)%6
                        temp_rem = (temp_mod6*10)%6
                        if gmpy2.is_prime(temp_child_num) == True:
                            nodeList.append(Node(temp_child_num,curr_node.np_cnt,children_matrix[temp_rem],0,temp_mod6))
                        elif curr_node.np_cnt < EXCEPTION_MAX:
                            nodeList.append(Node(temp_child_num,curr_node.np_cnt+1,children_matrix[temp_rem],0,temp_mod6))
                        break
                    elif curr_node.np_cnt < EXCEPTION_MAX:
                        temp_child_num = ((curr_node.num)*10)+j
                        temp_mod6 = ((curr_node.mod6_rem*10) + j)%6
                        temp_rem = (temp_mod6*10)%6
                        nodeList.append(Node(temp_child_num,curr_node.np_cnt+1,children_matrix[temp_rem],0,temp_mod6))
                        break

DFS_find_largestp()
     
print(largest_p)
'''

import math
from datetime import datetime
import gmpy2
#import sympy
#import scipy
#import numpy

largest_p=0
EXCEPTION_MAX=5

mod6_arr = [[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0]]
for i in range(1,10):
    for prev_mode in range(0,6):
        mod6_arr[i][prev_mode] = ((4*i) + prev_mode)%6

pot_primes = []
non_primes = []
for prev_mode in range(0,6):
    pot_primes_temp = []
    non_primes_temp = []
    for i in range(1,10):
        if mod6_arr[i][prev_mode] == 1 or mod6_arr[i][prev_mode] == 5:
            pot_primes_temp.append(i)
        else:
            non_primes_temp.append(i)
    pot_primes.append(pot_primes_temp)
    non_primes.append(non_primes_temp)

def recurs_find_largest(prev_num, non_prime_cnt, prev_mod6_rem, next_exp10):
    largestp = prev_num
    temp_pow = pow(10,next_exp10)

    for i in pot_primes[prev_mod6_rem]:
        temp_child_num = (temp_pow*i) + prev_num
        if gmpy2.is_prime(temp_child_num) == True:
            p = recurs_find_largest(temp_child_num, non_prime_cnt, mod6_arr[i][prev_mod6_rem], next_exp10 + 1)
            if p > largestp:
                largestp=p
        elif non_prime_cnt < EXCEPTION_MAX:
            p = recurs_find_largest(temp_child_num, non_prime_cnt+1, mod6_arr[i][prev_mod6_rem], next_exp10 + 1)
            if p > largestp:
                largestp=p

    if non_prime_cnt < EXCEPTION_MAX:
        for i in non_primes[prev_mod6_rem]:
            temp_child_num = (temp_pow*i) + prev_num
            p = recurs_find_largest(temp_child_num, non_prime_cnt+1, mod6_arr[i][prev_mod6_rem], next_exp10 + 1)
            if p > largestp:
                largestp=p
   
    return largestp

for start_num in (1,3,7,9):
    print(largest_p,EXCEPTION_MAX,start_num,datetime.now())
    if start_num in (3,7):
        npcnt=0
    else:
        npcnt=1
    if npcnt > EXCEPTION_MAX:
        continue
    pnum = recurs_find_largest(start_num, npcnt, start_num%6, 1)
    if pnum > largest_p:
        largest_p = pnum

print(largest_p)
print(datetime.now())

import math
import gmpy2
from datetime import datetime

#main checker
N = 3733799911799539139382193991
np_cnt = 0
tempnum = N
while tempnum > 0:
    print(tempnum, datetime.now())
    if gmpy2.is_prime(tempnum) == False:
        print("not prime ", tempnum)
        np_cnt += 1
    tempnum //= 10
for dig in range(1,10):
    if gmpy2.is_prime((N*10)+dig) == True:
        print("found larger num")
print("main exception count", np_cnt, datetime.now())

#bonus checker
N = 996381323136248319687995918918997653319693967
np_cnt = 0
tempnum = 0
pow10 = 1
while tempnum<N:
    tempnum = N%pow(10, pow10)
    print(tempnum, datetime.now())
    if gmpy2.is_prime(tempnum) == False:
        print("not prime ", tempnum)
        np_cnt += 1
    pow10 += 1
for dig in range(1,10):
    if gmpy2.is_prime((dig*pow10)+N) == True:
        print("found larger num")
print("bonus exception count", np_cnt, datetime.now())


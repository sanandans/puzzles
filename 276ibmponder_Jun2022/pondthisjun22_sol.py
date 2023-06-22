'''
IBM Ponder This challenge main and bonus *, June 22
https://research.ibm.com/haifa/ponderthis/challenges/June2022.html
Sanandan Swaminathan, submitted June 6, 2022

My answer for the main question of the June 2022 IBM Ponder This challenge (sequence of number of odd fixed polyominoes for n = 1 
through n = 18) is:

0, 1, 3, 11, 35, 108, 380, 1348, 5014, 18223, 67634, 252849, 950346, 3602437, 13697333, 52293534, 200399576, 770410271

For bonus *...
0, 1, 3, 11, 35, 108, 380, 1348, 5014, 18223, 67634, 252849, 950346, 3602437, 13697333, 52293534, 200399576, 770410271, 
2970369338, 11482572252

As a side note, the sequence I got for number of fixed polyominoes (total of odd and even) from n = 1 through n = 20 is:
1, 2, 6, 19, 63, 216, 760, 2725, 9910, 36446, 135268, 505861, 1903890, 7204874, 27394666, 104592937, 400795844, 1540820542, 
5940738676, 22964779660

My program basically works like the Redelmeier recursive, depth-first search for enumerating polyominoes and avoiding duplicates. Apart 
from having counters for fixed and odd, fixed polyominoes, I also have a counter to keep track of the total number of inversions needed 
to take a polyomino from one sort order to the other. When a cell gets added to the current polyomino, I compute the number of inversions 
this cell would need with all the other existing cells to go from one sort order to the other. This number gets added to the total 
inversions counter for this polyomino. If the total inversion count for the polyomino so far has odd parity, then this polyomino with the 
new cell added is another odd polyomino of that size.

While it's not surprising that the number of odd fixed polyominoes hovers around the 50% mark, it was nice to see several sizes where the 
split is exactly 50-50 between odd and even fixed polyominoes, including n = 18 !

'''

import copy
import time

def neighbors(polyomino):
    found = {}
    for key in polyomino:
        for delta_x, delta_y in [(1,0), (-1,0), (0,1), (0,-1)]:
            if key[1] + delta_y < 0 or (key[1] + delta_y == 0 and key[0] + delta_x < 0):
                continue
            new_square = (key[0] + delta_x, key[1] + delta_y)
            if new_square not in found and new_square not in polyomino:
                found[new_square]=None
    return found

def ns_neighbors(square, polyomino):
    found = {}
    for delta_x, delta_y in [(1,0), (-1,0), (0,1), (0,-1)]:
        if square[1] + delta_y < 0 or (square[1] + delta_y == 0 and square[0] + delta_x < 0):
                continue
        new_square = (square[0] + delta_x, square[1] + delta_y)
        if new_square not in polyomino:
            found[new_square]=None
    return found

def oddperms(polyomino, square):
    oddpermct = 0
    for key in polyomino:
        if square[0] < key[0] or (square[0] == key[0] and square[1] < key[1]):
            to_left_order1 = True
        else:
            to_left_order1 = False

        if square[1] < key[1] or (square[1] == key[1] and square[0] > key[0]):
            to_left_order2 = True
        else:
            to_left_order2 = False

        if (to_left_order1 == True and to_left_order2 == False) or (to_left_order1 == False and to_left_order2 == True):
            oddpermct += 1
    return oddpermct

def redelmeier(n):
    counts = [0] * (n+1)
    odd_counts = [0] * (n+1)
    counts[0] = 1
    polyomino = {}
    untried_set = [(0,0)]
    redelmeier_recursion(n, counts, polyomino, untried_set, odd_counts, 0)
    return counts, odd_counts

def redelmeier_recursion(n, counts, polyomino, untried_set, odd_counts, oddsum):
   
    while len(untried_set) > 0:
        new_square = untried_set.pop()
        new_untried_set = copy.copy(untried_set)
        new_square_neighbors = ns_neighbors(new_square, polyomino)
        polyomino_neighbors = neighbors(polyomino)
        for s in new_square_neighbors:
            if s not in polyomino_neighbors and s not in polyomino:
                new_untried_set.append(s)
        new_polyomino = copy.copy(polyomino)
        newoddsum = oddsum + oddperms(new_polyomino, new_square)
        new_polyomino[new_square]=None
        counts[len(new_polyomino)] += 1
        tempctr=counts[n]
        if tempctr > 0 and tempctr%100000000 == 0:
            local_time = time.ctime(time.time())
            print(local_time, tempctr)
        if (newoddsum%2 == 1):
            odd_counts[len(new_polyomino)] += 1
       
        if len(new_polyomino) < n:
            redelmeier_recursion(n, counts, new_polyomino, new_untried_set, odd_counts, newoddsum)

local_time = time.ctime(time.time())
print(local_time)
m=20
print(m)            
(ct,oddct)=redelmeier(m)
print(m,ct,oddct)
local_time = time.ctime(time.time())
print(local_time)


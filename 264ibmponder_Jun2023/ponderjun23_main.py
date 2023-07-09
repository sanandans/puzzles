'''
IBM Ponder This challenge main and bonus June '23
https://research.ibm.com/haifa/ponderthis/challenges/June2023.html
Sanandan Swaminathan, submitted June 2, 2023

This is my solution for the main puzzle (k=30, n=100). Separate program
tweaked from this one used for the bonus puzzle and its different conditions.

Program completes in about 6 seconds. First, it pre-populates a fixed k x k x k x n array with
cheese present/absent flag at the different times. It also pre-populates a fixed k x k x k array
containing an adjacency list for each of the cells. Then it does a recursive DFS search to determine
max cheese that can be collected. It uses a k x k x k x n x 2 array for memoization.
For each cell, there are two types of values that can be memoized - the max cheese possible starting
from this cell in the remaining time if cheese had not been collected in this cell before, and when
cheese had been collected in this cell before. The memoization is done at each time unit when this
cell is reached. Once the overall max cheese amount is determined, the program does a recursive
path print using the memoization array which was populated during the search for the max number.
It can print one or all solution paths (there can be many paths with the same max cheese amount).
I just printed the first solution string. I also have a verifier that takes a solution string and
plays out the steps to verify that it gives the max amount of cheese. I ran the program for k=5, n=20
also, and verified that one of the solutions matched the example given.
Below is my program for the main puzzle (conditions quite a bit different from bonus puzzle).
'''

import numpy as np
from datetime import datetime

print(datetime.now())

k=30
n=100
xrange = n//2

#given linear congruential generator to determine temporal cheese in cells at different times
def f(x):
    a = 1103515245
    c = 12345
    m = 2**31
    res = ((a*x) + c)%m
    return res

cheese_present = np.zeros((k+1,k+1,k+1), dtype=object) #object will be 1d array containing 0/1
adj_matrix = np.zeros((k+1,k+1,k+1), dtype=object) #object will be list of neighbor cells
#one-time populate these global arrays which will only be read
for a in range(1,k+1):
    for b in range(1,k+1):
        for c in range(1,k+1):
            #make array of times when cheese is present in this cell
            cheese_t = np.zeros((n+1), dtype=int)
            abc_product = a*b*c
            for x in range(xrange):
                cheese_t[(f(abc_product + x))%n] = 1
            cheese_present[a][b][c] = cheese_t

            #build adjacency list for this cell
            adjlist = []
            #adjlist.append((a,b,c,1)) #we can use current cell
            if a < k:
                adjlist.append((a+1,b,c,2))
            if b < k:
                adjlist.append((a,b+1,c,3))
            if c < k:
                adjlist.append((a,b,c+1,4))
            adj_matrix[a][b][c] = adjlist

print(datetime.now())

#recursive function that determines max amount of temporal cheese that can be collected
def recur_max_cheese(curr_cell, curr_t, matrix_max_rem_cheese, has_been_consumed = False):

    (a,b,c,d) = curr_cell

    #if there is a memoized value for this cell, time and consumed state (before this call), return it
    consumed_state = 0
    if has_been_consumed == True:
        consumed_state = 1
    temp_max_rem_cheese = matrix_max_rem_cheese[a][b][c][curr_t][consumed_state]
    if temp_max_rem_cheese > 0:
        return temp_max_rem_cheese
    
    #if cheese uncollected previously from this cell and cheese is present right now
    rem_cheese_cnt = 0
    if (has_been_consumed == False) and (cheese_present[a][b][c][curr_t] == 1):
        rem_cheese_cnt += 1
        has_been_consumed = True

    #if no more collection is possible
    if (curr_t == n) or (((a,b,c) == (k,k,k)) and (has_been_consumed == True)):
        matrix_max_rem_cheese[a][b][c][curr_t] = rem_cheese_cnt
        return rem_cheese_cnt

    #find max remaining cheese after this cell after time t
    best_rem_cheese_cnt = recur_max_cheese(curr_cell, curr_t + 1, matrix_max_rem_cheese, has_been_consumed)
    for next_cell in adj_matrix[a][b][c]:
        cnt = recur_max_cheese(next_cell, curr_t + 1, matrix_max_rem_cheese, False)
        if cnt > best_rem_cheese_cnt:
            best_rem_cheese_cnt = cnt
    best_rem_cheese_cnt += rem_cheese_cnt
    
    matrix_max_rem_cheese[a][b][c][curr_t][consumed_state] = best_rem_cheese_cnt #memoization
    return best_rem_cheese_cnt

#verify any solution string found
def sol_verifier(pathstring, max_cheese_cnt):
    consumed_arr = np.zeros((k+1,k+1,k+1), dtype=int)
    cheese_cnt = 0
    #start from cell (1,1,1) at t = 1
    curr_cell = (1,1,1)
    curr_t = 1
    for i in pathstring:
        (a,b,c) = curr_cell
        if consumed_arr[a][b][c] == 0 and (cheese_present[a][b][c][curr_t] == 1):
            cheese_cnt += 1
            consumed_arr[a][b][c] = 1
        match i:
            case '1':
                curr_cell = (a,b,c)
            case '2':
                curr_cell = (a+1,b,c)
            case '3':
                curr_cell = (a,b+1,c)
            case '4':
                curr_cell = (a,b,c+1)
            case default:
                curr_cell = (1,1,1)
        curr_t += 1
    return (cheese_cnt == max_cheese_cnt)

#print one or all paths that the mouse can take to collect max temporal cheese
def recurs_print_paths(curr_cell, curr_t, matrix_max_rem_cheese, pathstr, rem_cheese_cnt, max_cheese_cnt, \
                       has_been_consumed = False, mode = "onepath"):
    (a,b,c,d) = curr_cell
    consumed_state = 0
    if has_been_consumed == True:
        consumed_state = 1
    
    if matrix_max_rem_cheese[a][b][c][curr_t][consumed_state] == 0:
        if sol_verifier(pathstr, max_cheese_cnt) == False:
            print("ERROR in: ", pathstr)
            return "done"
        new_str = (((pathstr.replace('1','W')).replace('2','R')).replace('3','U')).replace('4','F')
        for i in range((n - len(new_str)) - 1):
            new_str += 'W'
        '''
        #verify given example for k=5, n=20 (use "onepath" argument to see it easier
        if new_str == "FFRFWFWRRRUUUWWWUWW":
            print("HOORAY")
            print(new_str)
        '''
        print(new_str, pathstr)
        if (mode == "onepath"):
            return "done"
        else:
            return "continue"
        
    if (has_been_consumed == False) and (cheese_present[a][b][c][curr_t] == 1):
        has_been_consumed = True
        consumed_state = 1
        rem_cheese_cnt -= 1

    temp_max_rem_cheese = matrix_max_rem_cheese[a][b][c][curr_t+1][consumed_state]
    if temp_max_rem_cheese == rem_cheese_cnt:
        if recurs_print_paths(curr_cell, curr_t+1, matrix_max_rem_cheese, pathstr+'1', temp_max_rem_cheese, \
                           max_cheese_cnt, has_been_consumed, mode) == "done":
            return "done"

    for next_cell in adj_matrix[a][b][c]:
        (w,x,y,z) = next_cell
        temp_max_rem_cheese = matrix_max_rem_cheese[w][x][y][curr_t+1][0]
        if temp_max_rem_cheese == rem_cheese_cnt:
            if recurs_print_paths(next_cell, curr_t+1, matrix_max_rem_cheese, pathstr+str(z), temp_max_rem_cheese, \
                               max_cheese_cnt, False, mode) == "done":
                return "done"
    return "continue"

if __name__ == "__main__":
    start_cell = (1,1,1,0)
    matrix_max_rem_cheese = np.zeros((k+1,k+1,k+1), dtype=object) #object will be 2d array
    for a in range(1,k+1):
        for b in range(1,k+1):
            for c in range(1,k+1):
                #2d array holding best counts with cheese consumed or not in a cell
                max_cheese_t = np.zeros((n+1,2), dtype=int)
                matrix_max_rem_cheese[a][b][c] = max_cheese_t
    max_cheese_cnt = recur_max_cheese(start_cell, 1, matrix_max_rem_cheese, False)
    print("max cheese collected: ", max_cheese_cnt)
    printstatus = recurs_print_paths(start_cell, 1, matrix_max_rem_cheese, "", max_cheese_cnt, max_cheese_cnt, \
                       False, "onepath") #send last argument as "onepath" to print just one possible solution
    print(datetime.now())
    #print(sol_verifier("111112212212112221234341222323213322224432332333344224232334344333344434342442423343444444422343341", max_cheese_cnt))
    '''
    max cheese collected:  87
    WWWWWRRWRRWRWWRRRWRUFUFWRRRURURWUURRRRFFURUURUUUUFFRRFRURUUFUFFUUUUFFFUFUFRFFRFRUUFUFFFFFFFRRUFUUFW
    111112212212112221234341222323213322224432332333344224232334344333344434342442423343444444422343341
    '''
    

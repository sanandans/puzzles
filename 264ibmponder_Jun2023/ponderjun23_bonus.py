'''
IBM Ponder This challenge main and bonus June '23
https://research.ibm.com/haifa/ponderthis/challenges/June2023.html
Sanandan Swaminathan, submitted June 2, 2023
Refer to another file for main puzzle's solution
In the bonus "*' puzzle, all directions are allowed, and cheese can be
collectred multiple times from a cell
Much larger search space: k=50, n=200, so bonus program takes around 56 seconds
compared to 6 seconds for the main puzzle.
Below is my program for the bonus puzzle (conditions quite a bit different from main puzzle).
'''
import numpy as np
from datetime import datetime

print(datetime.now())

k=50
n=200
xrange = n//2

#given linear congruential generator to determine temporal cheese in cells at different times
def f(x):
    a = 1103515245
    c = 12345
    m = 2**31
    res = ((a*x) + c)%m
    return res

#x=0,y=0,z=0 are redundant cells, but too few in the grand scheme to bother zero-indexing the cells in the problem
cheese_present = np.zeros((k+1,k+1,k+1,n+1), dtype=int) #containing 0/1 if cheese present/absent in cell at time t
adj_matrix = np.zeros((k+1,k+1,k+1), dtype=object) #object will be list of neighbor cells
#one-time populate these global arrays which will only be read
for a in range(1,k+1):
    for b in range(1,k+1):
        for c in range(1,k+1):
            abc_product = a*b*c
            for x in range(xrange):
                cheese_present[a][b][c][(f(abc_product + x))%n] = 1

            #build adjacency list for this cell
            adjlist = []
            #the fourth value in a neighbor cell denotes what direction must have been taken to reach the neighbor
            adjlist.append((a,b,c,1)) #wait W
            if a < k:
                adjlist.append((a+1,b,c,2)) #right R
            if b < k:
                adjlist.append((a,b+1,c,3)) #up U
            if c < k:
                adjlist.append((a,b,c+1,4)) #forward F
            if a > 1:
                adjlist.append((a-1,b,c,5)) #left L
            if b > 1:
                adjlist.append((a,b-1,c,6)) #down D
            if c > 1:
                adjlist.append((a,b,c-1,7)) #backwards B  
            adj_matrix[a][b][c] = adjlist

print(datetime.now())

#recursive function that determines max amount of temporal cheese that can be collected
def recur_max_cheese(curr_cell, curr_t, matrix_max_rem_cheese):

    (a,b,c,d) = curr_cell

    #if there is a memoized value for this cell and time (before this call), return it
    temp_max_rem_cheese = matrix_max_rem_cheese[a][b][c][curr_t]
    if temp_max_rem_cheese > -1: #if entry for this cell has been updated with best remaining cheese count before
        return temp_max_rem_cheese
    
    #if cheese is present right now
    rem_cheese_cnt = 0
    if cheese_present[a][b][c][curr_t] == 1:
        rem_cheese_cnt += 1

    #if no more collection is possible
    if curr_t == n:
        #cheese can't appear at t=n, so this will really be zero
        #in fact, we could have broken out at t=n-1 after collecting cheese if available at that time
        matrix_max_rem_cheese[a][b][c][curr_t] = rem_cheese_cnt
        return rem_cheese_cnt

    #find max remaining cheese after this cell after time t
    best_rem_cheese_cnt = 0
    for next_cell in adj_matrix[a][b][c]:
        cnt = recur_max_cheese(next_cell, curr_t + 1, matrix_max_rem_cheese)
        if cnt > best_rem_cheese_cnt:
            best_rem_cheese_cnt = cnt
    best_rem_cheese_cnt += rem_cheese_cnt #add any cheese that may have been gained in this step (above)
    matrix_max_rem_cheese[a][b][c][curr_t] = best_rem_cheese_cnt #memoization
    return best_rem_cheese_cnt

#verify any solution string found
def sol_verifier(pathstring, max_cheese_cnt):
    cheese_cnt = 0
    #start from cell (1,1,1) at t = 1
    curr_cell = (1,1,1)
    curr_t = 1
    for i in pathstring:
        (a,b,c) = curr_cell
        if cheese_present[a][b][c][curr_t] == 1:
            cheese_cnt += 1
        match i:
            case '1':
                curr_cell = (a,b,c)
            case '2':
                curr_cell = (a+1,b,c)
            case '3':
                curr_cell = (a,b+1,c)
            case '4':
                curr_cell = (a,b,c+1)
            case '5':
                curr_cell = (a-1,b,c)
            case '6':
                curr_cell = (a,b-1,c)
            case '7':
                curr_cell = (a,b,c-1)
            case default:
                curr_cell = (1,1,1)
        curr_t += 1
    return (cheese_cnt == max_cheese_cnt)

#print one or all paths that the mouse can take to collect max temporal cheese
def recurs_print_paths(curr_cell, curr_t, matrix_max_rem_cheese, pathstr, rem_cheese_cnt, max_cheese_cnt, \
                       mode = "onepath"):
    (a,b,c,d) = curr_cell
    
    #if leaf of this best path has been reached
    if matrix_max_rem_cheese[a][b][c][curr_t] == 0:
        if len(pathstr) != (n-1):
            print("ERROR: path not of length n-1 as expected: ", pathstr)
            return "done"
        if sol_verifier(pathstr, max_cheese_cnt) == False:
            print("ERROR: path not giving max cheese as expected: ", pathstr)
            return "done"
        new_str = ((((((pathstr.replace('1','W')).replace('2','R')).replace('3','U')).replace('4','F')).replace('5','L')).replace('6','D')).replace('7','B')
        print(new_str, pathstr)
        if (mode == "onepath"):
            return "done"
        else:
            return "continue"
        
    if cheese_present[a][b][c][curr_t] == 1:
        rem_cheese_cnt -= 1

    for next_cell in adj_matrix[a][b][c]:
        (w,x,y,z) = next_cell #z denotes what direction is taken to reach the neighbor
        temp_max_rem_cheese = matrix_max_rem_cheese[w][x][y][curr_t+1]
        if temp_max_rem_cheese == rem_cheese_cnt: #link to any next cell in the chain that achieves max cheese
            if recurs_print_paths(next_cell, curr_t+1, matrix_max_rem_cheese, pathstr+str(z), rem_cheese_cnt, \
                               max_cheese_cnt, mode) == "done":
                return "done"
    return "continue"

if __name__ == "__main__":
    start_cell = (1,1,1,0) #the fourth value of 0 for direction does not matter here; we just start from cell (1,1,1)
    #for memoizarion: max cheese possible from this cell starting at time t
    matrix_max_rem_cheese = np.full((k+1,k+1,k+1,n+1), -1, dtype=int)
    max_cheese_cnt = recur_max_cheese(start_cell, 1, matrix_max_rem_cheese)
    print("max cheese collected: ", max_cheese_cnt)
    printstatus = recurs_print_paths(start_cell, 1, matrix_max_rem_cheese, "", max_cheese_cnt, max_cheese_cnt, \
                       "onepath") #send last argument as "onepath" to print just one possible solution
    print(printstatus)
    print(datetime.now())
    print(sol_verifier("1222222222223222233422333332473374241464145477414131467314774774774147747741454145414135731314121412121454131254131255212552574552125721255212552552574125527741255277412145725745721214777454572147741", max_cheese_cnt))
    '''
    max cheese collected:  184
    WRRRRRRRRRRRURRRRUUFRRUUUUURFBUUBFRFWFDFWFLFBBFWFWUWFDBUWFBBFBBFBBFWFBBFBBFWFLFWFLFWFWULBUWUWFWRWFWRWRWFLFWUWRLFWUWRLLRWRLLRLBFLLRWRLBRWRLLRWRLLRLLRLBFWRLLRBBFWRLLRBBFWRWFLBRLBFLBRWRWFBBBFLFLBRWFBBFW
    1222222222223222233422333332473374241464145477414131467314774774774147747741454145414135731314121412121454131254131255212552574552125721255212552552574125527741255277412145725745721214777454572147741
    '''
    

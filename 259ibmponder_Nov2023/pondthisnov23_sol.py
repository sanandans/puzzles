'''
My IBM Ponder This November '23 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/November2023.html
Sanandan Swaminathan, submitted October 31, 2023

As mentioned in the puzzle, there are only two "sorted" states for the 15 puzzle. All states can be reduced to
exactly one of the two sorted states - half to one, half to the other. We can go from a magic square (there
are so few 4x4s relative to 15 puzzle states) to the appropriate sorted state. The answer for the given problem
will be the reversed steps.
The decision on which sorted state to aim for can be based on an invariant. One such invariant is: the parity
of the sum of (1) the parity of total number of inversions of the 1-15 tiles, and (2) the parity of the
difference between the bottom row number and the row number of the 0 tile. This parity of the sum remains constant
from the start state to whatever state we go to. We can see why this is an invariant. Any horizontal move doesn't change
either of the sum's components. In a vertical move, the parity of the row number difference of the 0 tile necessarily
flips, and the parity of inversion total of 1-15 tiles also flips. Thus, the parity of the sum doesn't change;
if a 15-puzzle starts with the invariant as 0, it remains 0. If it starts as 1, it remains 1. We can determine
this invariant value for the two solved states. Depending on the invariant value of a given magic square, we
can aim for the solved state having the same invariant value.

Since the limit on number of steps allowed is generously high for the main puzzle, I just took the first magic square
generated and solved it by hand on a spreadsheet. This initial attempt was quick and I took 98 steps. Of course, this
is not feasible when we want to explore potentially many magic squares for the bonus * puzzle which has a
steps limit of 50. I first tried standard BFS but, unsurprisingly,  it ran into memory issues. DFS would
avoid the memory issues, but execution time could be enormous, especially due to cycles. If we try DFS with
tracking of visited states, we could run into memory issues. IDDFS (iterative deepening DFS) could be a bit
better, but it's still a blind, uniformed search. A* informed heuristic search could be appropriate but could
run into memory issues. Eventually I decided to go with recursively doing IDA* search (Iterative Deepening A*)
which uses heuristic like A* but has very low memory footprint due to usage of DFS style traversal. However,
this can run into cycles (i.e. repeating tile moves circularly), so I use an LRU cache style dictionary to
maintain the last 50 game states. I encode the game state as a base 16 number, and use this as the key for the
LRU cache. This encoding helps in quickly calculating the next game state based on the move; I use bitwise
operations to go from one game state value to another.

For the IDA* search heuristic, I use the standard combo of path length from start to current node plus the
Manhattan distance total of the 1-15 tiles from their respective goal cells. This is, of course, an "admissible"
lower bound (we are looking for the minimum path). If all 1-15 tiles were unhindered, each would need to at least
traverse the Manhattan distance from its current location to its goal cell. Of course, this heuristic will usually
be quite an underestimate, but this puzzle did not need tighter heuristics like tiles conflicting on their desired
row/column. As we move from a node to a child state, the Manhattan distance can be quickly adjusted just based on the tile pair
being swapped and direction of swap. Memory footprint of the IDA* search is small. There is the recursion function stack (limited
to 50 depth for bonus problem). Copies of game grid are avoided as we can swap/unswap two tiles before/after every move.
LRU cache dictionary to avoid cycles is limited to 50 entries for bonus problem. There's an empty list passed around to
store the sequence of steps when a solution is found, though we could avoid this as well by having each node just print
the step it took while returning, when solution is found. The program found the first solution for the bonus problem in
about 12 minutes after trying a couple of thousand magic squares. Potential improvement could be to first generate all
the magic squares, and store them in a min heap based on their total Manhattan distance. Magic squares having lower
Manhattan distance are more likely to have a solution with fewer steps needed. The number of magic squares can also be
reduced based on rotations/reflections. The heuristic for the IDA* search can be improved by adding aspects like linear
conflicts of tile pairs blocking each other on their desired row/column, or a pattern database with precomputed solution
steps for some patterns.
'''

from datetime import datetime
from itertools import permutations
import sys
from collections import OrderedDict
from collections.abc import MutableMapping
#from queue import Queue
#from collections import deque
#import copy

steps_lim = 50 # 50 steps max allowed for bonus * puzzle, 150 for main puzzle
N = 4 #for 4x4 puzzle
MAGIC_SUM = 30 #4x44 magic square row/column/diagonal sum for numbers 0-15
tot_magic_squares = 0 #just to track progress as we try magic squares
solved_arr_odd = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0] #solved state with 15 inversions with 0 tile
#where the tiles 0-15 for the above solved state are located (for example. 0 tile is at bottom right of solved grid)
pos_odd_perm = [[3,3],[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0], \
                [2,1],[2,2],[2,3],[3,0],[3,1],[3,2]]
    
solved_arr_even = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,14,0] #solved state with 15 inversions with 0 tile and 15/14 tiles
#where the tiles 0-15 for the above solved state are located (for example. 0 tile is at bottom right of solved grid)
pos_even_perm = [[3,3],[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0], \
                [2,1],[2,2],[2,3],[3,0],[3,2],[3,1]]

#to calculate initial total Manhattan distance for a given game board, to be used as a heuristic in IDA* search
def tot_manhattan_dist(arr, compareToOddPerm):
    pos_target_perm = pos_even_perm
    if compareToOddPerm == True:
        pos_target_perm = pos_odd_perm
    md = 0
    for row in range(len(arr)):
        for col in range(len(arr)):
            md += abs(row - pos_target_perm[arr[row][col]][0]) + abs(col - pos_target_perm[arr[row][col]][1])
    return md

#generate all info needed for the IDA* search when a magic square is generated
def getPermInfo(grid):
    grid_2d = [[0]*N for _ in range(N)]
    zero_pos_row = 0
    zero_pos_col = 0
    val = 0
    mult = 1
    zero_rightbit_pos = 0
    for i in range((N*N)-1,-1,-1):
        row = i//N
        col = i%N
        grid_2d[row][col] = grid[i]
        if grid[i] == 0:
            zero_pos_row = row
            zero_pos_col = col
            zero_rightbit_pos = ((N*N) - 1 - i) * N
        val += mult*grid[i]
        mult *= N*N

    inversions = 0
    for i in range((N*N)-1):
        if grid[i] == 0:
            continue
        for j in range(i+1, N*N):
            if grid[j] == 0:
                continue
            if grid[i] > grid[j]:
                inversions += 1          
    invariant = (((N-1 - zero_pos_row)%2) + (inversions%2))%2
    grid_manhattan_odd_perm = tot_manhattan_dist(grid_2d, True)
    grid_manhattan_even_perm = tot_manhattan_dist(grid_2d, False)
    return grid_2d, zero_pos_row, zero_pos_col, grid_manhattan_odd_perm, grid_manhattan_even_perm, \
           val, zero_rightbit_pos, invariant

#to calculate "value" of the grid as a base 16 number; grid value is used as key in LRU cache dictionary
def calc_grid_val(v, zero_p, direction):
    offset = zero_p
    if direction == 0: #up
        offset += 16
    elif direction == 1: #down
        offset -= 16
    elif direction == 2: #left
        offset += 4
    elif direction == 3: #right
        offset -= 4
    x = (v>>(offset)) & 15
    y = ((x<<(offset)) | (x<<zero_p)) ^ v
    return y, offset
       
#cache to store recent game states to avoid cycles during IDA* search
#taken from https://stackoverflow.com/questions/2437617/how-to-limit-the-size-of-a-dictionary
class dictLRUCache(MutableMapping):
    def __init__(self, maxlen, items=None):
        self._maxlen = maxlen
        self.d = OrderedDict()
        if items:
            for k, v in items:
                self[k] = v

    @property
    def maxlen(self):
        return self._maxlen

    def __getitem__(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)
        return self.d[key]

    def __setitem__(self, key, value):
        if key in self.d:
            self.d.move_to_end(key)
        elif len(self.d) == self.maxlen:
            self.d.popitem(last=False)
        self.d[key] = value

    def __delitem__(self, key):
        del self.d[key]

    def __iter__(self):
        return self.d.__iter__()

    def __len__(self):
        return len(self.d)

#recursive IDA* search for an answer
def iterative_deepening_Astar_DFS(grid, zero_pos_row, zero_pos_col, manhattan, pos_target_perm, \
                                  parent_dist_from_root, threshold, val, zero_pos, lrucache, step_seq):
    if manhattan == 0:
        return 0, True
    gval = parent_dist_from_root + 1 #path length from start state to this state
    fval = gval + manhattan #heuristic used
    if fval > threshold: #threshold for this iteration of IDA* exceeded, so go back to request threshold increase
        return fval, False

    min_child_cost = sys.maxsize #this variable will store the minimum value above threshold that got halted
    #try moving the 0 tile up
    if zero_pos_row > 0:
        child_md = manhattan + 1 # 0 moving away from its target cell
        num_moved = grid[zero_pos_row-1][zero_pos_col]
        new_val, new_zero_pos = calc_grid_val(val, zero_pos, 0)
        if lrucache.__getitem__(new_val) == -1: #check if exact state has been encountered before (to avoid cycles)
            lrucache.__setitem__(new_val, 1) #memoize this state
            if zero_pos_row <= pos_target_perm[num_moved][0]:
                child_md -= 1
            else:
                child_md += 1
            grid[zero_pos_row][zero_pos_col] = num_moved
            grid[zero_pos_row-1][zero_pos_col] = 0
            pruned_min, status = iterative_deepening_Astar_DFS(grid, zero_pos_row-1, zero_pos_col, child_md, \
                                                               pos_target_perm, gval, threshold, new_val, \
                                                               new_zero_pos, lrucache, step_seq)
            if status == True: # match found somewhere downstream
                step_seq.append(num_moved)
                return 0, True
            #reset grid by reverse swapping the two tiles (avoids array copies at every child/step)
            grid[zero_pos_row-1][zero_pos_col] = num_moved
            grid[zero_pos_row][zero_pos_col] = 0
            if pruned_min < min_child_cost:
                min_child_cost = pruned_min

    #try moving the 0 tile down
    if zero_pos_row < N-1:
        child_md = manhattan - 1 # 0 moving towards its target cell
        num_moved = grid[zero_pos_row+1][zero_pos_col]
        new_val, new_zero_pos = calc_grid_val(val, zero_pos, 1)
        if lrucache.__getitem__(new_val) == -1:
            lrucache.__setitem__(new_val, 1)
            if zero_pos_row >= pos_target_perm[num_moved][0]:
                child_md -= 1
            else:
                child_md += 1
            grid[zero_pos_row][zero_pos_col] = num_moved
            grid[zero_pos_row+1][zero_pos_col] = 0
            pruned_min, status = iterative_deepening_Astar_DFS(grid, zero_pos_row+1, zero_pos_col, child_md, \
                                                               pos_target_perm, gval, threshold, new_val, \
                                                               new_zero_pos, lrucache, step_seq)
            if status == True:
                step_seq.append(num_moved)
                return 0, True
            grid[zero_pos_row+1][zero_pos_col] = num_moved
            grid[zero_pos_row][zero_pos_col] = 0
            if pruned_min < min_child_cost:
                min_child_cost = pruned_min     

    #try moving the 0 tile left
    if zero_pos_col > 0:
        child_md = manhattan + 1 # 0 moving away from its target cell
        num_moved = grid[zero_pos_row][zero_pos_col-1]
        new_val, new_zero_pos = calc_grid_val(val, zero_pos, 2)
        if lrucache.__getitem__(new_val) == -1:
            lrucache.__setitem__(new_val, 1)
            if zero_pos_col <= pos_target_perm[num_moved][1]:
                child_md -= 1
            else:
                child_md += 1
            grid[zero_pos_row][zero_pos_col] = num_moved
            grid[zero_pos_row][zero_pos_col-1] = 0
            pruned_min, status = iterative_deepening_Astar_DFS(grid, zero_pos_row, zero_pos_col-1, child_md, \
                                                               pos_target_perm, gval, threshold, new_val, \
                                                               new_zero_pos, lrucache, step_seq)
            if status == True:
                step_seq.append(num_moved)
                return 0, True
            grid[zero_pos_row][zero_pos_col-1] = num_moved
            grid[zero_pos_row][zero_pos_col] = 0
            if pruned_min < min_child_cost:
                min_child_cost = pruned_min

    #try moving the 0 tile right
    if zero_pos_col < N-1:
        child_md = manhattan - 1 # 0 moving towards its target cell
        num_moved = grid[zero_pos_row][zero_pos_col+1]
        new_val, new_zero_pos = calc_grid_val(val, zero_pos, 3)
        if lrucache.__getitem__(new_val) == -1:
            lrucache.__setitem__(new_val, 1)
            if zero_pos_col >= pos_target_perm[num_moved][1]:
                child_md -= 1
            else:
                child_md += 1
            grid[zero_pos_row][zero_pos_col] = num_moved
            grid[zero_pos_row][zero_pos_col+1] = 0
            pruned_min, status = iterative_deepening_Astar_DFS(grid, zero_pos_row, zero_pos_col+1, child_md, \
                                                               pos_target_perm, gval, threshold, new_val, \
                                                               new_zero_pos, lrucache, step_seq)
            if status == True:
                step_seq.append(num_moved)
                return 0, True
            grid[zero_pos_row][zero_pos_col+1] = num_moved
            grid[zero_pos_row][zero_pos_col] = 0
            if pruned_min < min_child_cost:
                min_child_cost = pruned_min

    return min_child_cost, False

#sentinal dummy node that adjusts heuristic threshold and repeatedly launches DFS from root
def IDAstar_search_driver(start_grid, zero_pos_row, zero_pos_col, manhattan_initial, compareToOddPerm, gridval, \
                          zero_pos, step_sequence):
    if manhattan_initial == 0:
        print("Input grid matches goal, no moves needed")
        return True

    pos_target_perm = pos_even_perm
    if compareToOddPerm:
        pos_target_perm = pos_odd_perm

    threshold = manhattan_initial
    while True:
        if threshold > steps_lim:
            return False
        lru_cache = dictLRUCache(steps_lim)
        threshold, status = iterative_deepening_Astar_DFS(start_grid, zero_pos_row, zero_pos_col, manhattan_initial, \
                                                          pos_target_perm, -1, threshold, gridval, zero_pos, \
                                                          lru_cache, step_sequence)
        if status == True:
            return True

    return False

#recursive method to generate magic sqaures.
#for each magic square generated, launch an IDA* search to go to desired goal state.
def find_magic_15sq(rem_nums, rowcol, grid):
    global tot_magic_squares
    if rowcol == N-1:
        grid[(N*N)-1] = rem_nums.pop()
        if sum(grid[(N-1)*N:N*N]) == MAGIC_SUM and \
               sum(grid[N-1 + (i*N)] for i in range(N)) == MAGIC_SUM and \
               sum(grid[i+(i*N)] for i in range(N)) == MAGIC_SUM and \
               sum(grid[N-1-i+(i*N)] for i in range(N)) == MAGIC_SUM:

            #magic square generated; can do IDA* search
            grid_2d, zero_pos_row, zero_pos_col, grid_manhattan_odd_perm, grid_manhattan_even_perm, val, \
                     zero_pos, invariant = getPermInfo(grid)
            tot_magic_squares += 1
            if tot_magic_squares%1000 == 0:
                print(tot_magic_squares, datetime.now())
            sequence = []
            #call IDA* for relavant goal state based on invariant value of the magic square grid
            if invariant == 0:
                if IDAstar_search_driver(grid_2d, zero_pos_row, zero_pos_col, grid_manhattan_odd_perm, True, val, zero_pos, sequence) == True:
                    return True, sequence, grid, solved_arr_odd
            else:
                if IDAstar_search_driver(grid_2d, zero_pos_row, zero_pos_col, grid_manhattan_even_perm, False, val, zero_pos, sequence) == True:
                    return True, sequence, grid, solved_arr_even
        return False, [], [], []

    tempsum = sum(grid[rowcol*N:(rowcol*N) + rowcol])
    for perm in permutations(rem_nums, N-rowcol):
        if sum(perm) + tempsum == MAGIC_SUM:
            for i in range(N-rowcol):
                grid[(rowcol*N) + rowcol + i] = perm[i]
            rem = rem_nums - set(perm)
            tempsum1 = sum(grid[rowcol+(i*N)] for i in range(rowcol+1))
            for perm1 in permutations(rem, N-rowcol-1):
                if sum(perm1) + tempsum1 == MAGIC_SUM:
                    for i in range(N-rowcol-1):
                        grid[(rowcol+1+i)*N + rowcol] = perm1[i]
                    status, seq, retgrid, solvedarr = find_magic_15sq(rem - set(perm1), rowcol+1, grid)
                    if status == True:
                        return status, seq, retgrid, solvedarr
    return False, [], [], []

#verify the solution
def solution_checker(start_grid, goal_arr, seq):
    zero_row = N-1
    zero_col = N-1
    for i in range(len(seq)):
        found = False
        if zero_row > 0 and start_grid[zero_row-1][zero_col] == seq[i]:
            start_grid[zero_row-1][zero_col] = 0
            start_grid[zero_row][zero_col] = seq[i]
            zero_row -= 1
            found = True
        elif zero_row < 3 and start_grid[zero_row+1][zero_col] == seq[i]:
            start_grid[zero_row+1][zero_col] = 0
            start_grid[zero_row][zero_col] = seq[i]
            zero_row += 1
            found = True
        elif zero_col > 0 and start_grid[zero_row][zero_col-1] == seq[i]:
            start_grid[zero_row][zero_col-1] = 0
            start_grid[zero_row][zero_col] = seq[i]
            zero_col -= 1
            found = True
        elif zero_col < 3 and start_grid[zero_row][zero_col+1] == seq[i]:
            start_grid[zero_row][zero_col+1] = 0
            start_grid[zero_row][zero_col] = seq[i]
            zero_col += 1
            found = True
        if found == False:
            print("error", i, seq[i])
            return False
    for i in range(N*N):
        if goal_arr[i] != start_grid[i//N][i%N]:
            print("error", goal_arr[i], start_grid[i//N][i%N])
            return False
    print("check successful")
    return True

print(datetime.now())
sq_grid = [0]*(N*N)
status, seq, end_arr, start_arr = find_magic_15sq(set(range(0,N*N)), 0, sq_grid)
if status == False:
    print("no solution found")
else:
    start_grid = [[0]*N for _ in range(N)]
    for i in range(N*N):
        start_grid[i//N][i%N] = start_arr[i]
    if solution_checker(start_grid, end_arr, seq) == True:
        print("solution found")
        print("Sequence of steps", seq)
        print("Number of steps", len(seq))
        print("Initial grid (sorted or almost sorted)", start_arr)
        print("final grid (magic square)", end_arr)
print(datetime.now())


'''
My IBM Ponder This April '25 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/April2025.html
Sanandan Swaminathan, submitted March 31, 2025

My approach for the main puzzle was as follows. 19 is the largest object size in the grid. The program first
uses dynamic programming, with typical memoization to avoid repeating states and some checks to backtrack early.
The objective of this first stage is to get to GP of at least 19 x 19 = 361 in upto 100 steps since, once we get to
GP 361, i.e. size 19, we can sweep through all 400 cells of the 20x20 grid blindly in another 400 steps for
a total of upto 500 steps.

The program reached the required GP of 361 instantaneoulsy in 99 steps. Then, all 400 cells in the grid could
be visited in exactly 400 steps, starting from the cell we landed in when GP 361 was reached, regardless of
where that cell is located in the grid. We can sweep through these 400 cells blindly without any checks. The
program simply adds the relevant directions to simulate the moves through all 400 cells.
The program completed instantaneously and printed the full path of 499 steps given below:

RRDRRUDLLULLDURRDRRURRDULLDURRRRDULRRRDLDRRDRRDRUURDDDRRDRDLDRDDDRDLDLDLULURULLDDDRDDDDLDLUUUUULUUURRRRRRRUUUUUU
UUUUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDLUUUUUUU
UUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDLUUUUUUUUUULDDDDDDDDDDDDDDDDDDDR
UUUUUUUURDDDDDDDDRUUUUUUUURDDDDDDDDRUUUUUUUURDDDDDDDDRUUUUUUUURDDDDDDDDRUUUUUUUURDDDDDDDDRUUUUUUUURDDDDDDDDRUUUU
UUURDDDDDDDRUUUUUUURDDDDDDDRUUUUUUURDDDDDDDRUUUUUUU

Note that GP 361 could be reached in well less than 100 steps too, and the whole grid could be emptied in fewer
than 500 steps, but the objective was met instantaneouly with 500 steps, so I moved on to the bonus puzzle. Finding
the fewest number of steps to empty the whole board in the main puzzle would need more compute time since there is
not a very solid look-ahead heuristic here apart from basic ones like checking if the remaining steps are
insufficient even if every future cell had value 19, or greedily going to the neighbors in order of largest to
smallest value offered (or largest value looking ahead into next k cells), etc. Also, we wouldn't have the luxury
of simply sweeping through 400 cells blindly in the end if we are looking for the absolute minimum.

The bonus puzzle is a different beast with a much larger grid (30x30). While we are not asked to sweep through the
whole grid, GP of 900 (size 30) has to be reached in <= 150 steps. I decided to switch to doing this by hand. I put
the 30x30 grid into a spreadsheet, and highlighted high-value cells (I considered cells with values 16, 17, 18, 19
as high-value cells). This showed some promising clusters in the top-right and bottom-left quadrants. There are some
clusters in the bottom-right quadrant too, but it might have taken too many steps to get there. I first focused on
getting out of the starting top-left quadrant as quickly as possible, with the objective being to get to GP 361 (size
19) in a reasonably low number of steps. Then the plan was to attack one of the other dense quadrants, and I decided
on the top-right quadrant as the one where the path should finish. I crossed GP of 361 at the 86th step, almost at
the vertical border between the top-left and top-right quadrants. Then I just followed the high-value cells in the
top-right region to get to GP 911 (size 30) in a further 39 steps (total steps 125). I ran my manual solution path
through a verification function to ensure correctness. My full path of 125 steps for the bonus puzzle is given below:

RRRRDDDDLDLLDRRDRDDRURLUUUDRRURUDRDRDLDURRUULURULULRUURDDRURDDDRDRDDLULLUURRURRRRDDLULDDRDDRUURDRUUURDDDDDRDDDRRUR
URRRURULUUR

In hindsight, the main puzzle could also have been done by hand by looking for a path of <= 100 steps to get to GP
361, and then simply listing the sweep through all 400 cells in exactly 400 more steps.
'''

import math
from datetime import datetime
from copy import deepcopy

BONUS = False #set to False for main, True for bonus
N = 20 #grid dimensions for main
STEP_LIMIT = 500 #at most 500 steps allowed for main
if BONUS:
    N = 30 #grid dimensions for bonus
    STEP_LIMIT = 150 #at most 150 steps allowed for bonus
grid = None
if not BONUS:
    grid = [[0,0,1,5,1,0,0,0,0,0,1,19,0,7,4,2,7,12,7,1],
    [2,6,0,0,1,8,0,8,1,2,1,0,8,9,1,7,10,13,10,6],
    [4,11,6,7,5,5,14,1,12,1,0,2,0,2,2,5,1,10,0,14],
    [15,12,2,5,18,6,19,16,18,11,14,3,1,2,3,3,8,2,1,9],
    [5,6,8,18,4,17,7,16,14,13,4,13,8,1,2,2,7,5,11,12],
    [6,7,13,16,1,14,7,17,18,9,14,6,16,10,0,3,2,0,6,5],
    [11,5,11,3,14,19,19,4,17,16,3,12,17,17,1,2,12,6,7,11],
    [18,6,6,3,19,13,7,9,5,13,4,4,2,13,2,0,0,5,4,6],
    [17,19,7,2,4,3,4,1,16,9,13,17,17,15,6,9,1,5,2,0],
    [8,8,17,18,10,12,10,0,0,13,13,10,8,0,0,7,18,10,6,3],
    [13,3,19,3,5,9,17,16,12,2,19,9,1,17,3,0,10,11,4,19],
    [14,5,11,13,15,6,5,10,6,1,7,3,4,15,10,10,13,4,9,7],
    [2,12,5,7,7,16,3,2,18,14,11,18,12,15,4,2,12,15,10,6],
    [12,5,2,15,8,9,18,9,5,1,17,17,1,0,8,9,5,6,8,13],
    [9,13,5,3,9,8,18,15,10,6,12,18,11,15,2,12,6,8,12,15],
    [14,4,2,0,13,2,18,12,16,2,4,13,0,3,16,15,15,16,7,7],
    [6,12,1,14,4,12,8,14,10,0,15,16,13,4,5,12,5,2,16,12],
    [5,5,3,0,8,0,5,16,11,4,17,13,18,17,0,9,8,16,13,6],
    [15,13,13,5,6,7,9,15,12,18,2,12,19,4,9,5,6,8,9,3],
    [12,10,11,2,5,8,11,7,16,12,0,14,10,5,9,0,15,4,11,3]]
else:
    grid = [[0,1,0,0,0,5,16,8,15,4,5,5,17,17,7,11,18,4,16,15,9,17,1,3,19,6,4,16,3,7],
            [6,3,13,11,1,5,10,18,8,18,8,8,3,10,18,4,2,8,3,1,11,12,11,15,12,8,14,5,4,9],
            [9,0,15,4,1,11,1,11,17,8,4,6,4,12,16,19,9,8,4,2,18,12,1,4,4,10,10,4,9,2],
            [10,10,2,9,1,19,19,16,19,18,2,4,17,6,8,1,14,9,13,4,1,4,10,2,11,2,7,8,10,15],
            [11,6,14,1,0,8,4,9,3,16,6,6,14,9,5,19,13,5,5,0,17,18,8,17,6,4,5,17,5,15],
            [0,1,0,0,7,1,8,0,4,3,3,5,10,16,2,9,18,17,17,6,14,15,13,12,1,8,15,1,9,1],
            [0,1,1,0,19,4,1,0,13,4,4,6,3,11,11,1,19,17,12,7,16,17,0,18,0,14,17,18,17,18],
            [16,14,5,1,3,0,18,12,15,7,2,0,2,2,8,13,3,9,13,13,18,3,1,12,18,19,1,6,16,0],
            [7,13,15,9,0,1,4,15,8,3,19,12,4,0,2,1,11,19,6,3,0,14,5,15,7,4,3,15,10,15],
            [19,16,11,8,3,2,10,13,10,14,11,12,10,18,6,2,7,9,11,10,4,14,10,6,11,4,12,5,17,10],
            [9,0,10,19,19,11,14,19,17,3,4,8,11,4,3,6,8,12,4,8,4,3,16,10,4,10,12,10,19,0],
            [18,17,1,17,19,5,3,10,10,19,17,6,6,14,3,2,8,5,1,2,8,10,7,4,18,10,5,3,9,6],
            [10,16,0,17,11,10,14,1,11,1,2,14,16,4,8,2,10,2,8,8,18,12,18,13,18,1,17,18,8,2],
            [2,11,8,11,12,15,0,5,8,3,4,6,6,7,6,15,7,7,13,18,13,12,14,9,15,0,15,8,1,7],
            [2,6,17,14,5,14,0,8,1,11,13,13,19,13,5,1,8,9,18,5,1,16,14,11,9,2,12,18,10,19],
            [15,2,15,17,8,5,11,18,16,10,7,1,17,18,19,9,4,13,12,6,3,2,4,5,0,13,13,17,19,12],
            [17,4,4,17,8,14,6,12,18,14,13,7,17,5,19,18,9,11,11,10,6,17,19,6,13,19,7,0,14,5],
            [8,9,10,2,19,3,7,10,9,14,16,3,6,4,1,15,13,8,5,0,14,8,6,0,1,3,14,1,13,10],
            [12,3,10,18,5,19,17,16,5,12,14,19,6,13,15,3,1,15,15,4,10,9,12,2,19,3,10,13,12,2],
            [19,18,17,19,2,18,16,5,6,4,12,10,0,1,5,12,10,18,3,0,3,12,14,2,16,13,9,15,10,15],
            [17,5,19,16,14,6,2,15,9,14,19,15,7,15,16,6,12,1,8,12,2,14,12,18,4,4,4,12,12,17],
            [6,12,7,17,0,11,17,11,5,12,13,6,4,13,15,16,9,16,15,3,13,11,3,17,14,9,5,5,5,12],
            [3,0,4,15,16,4,17,2,2,16,0,1,7,4,3,0,4,2,9,13,13,4,15,10,16,0,1,5,1,2],
            [6,1,9,6,9,9,8,18,2,5,2,9,19,0,12,7,0,17,4,3,19,10,12,14,10,8,6,6,10,19],
            [6,11,13,2,17,11,3,1,18,13,12,0,11,7,2,12,9,3,13,8,2,1,17,19,11,19,5,0,2,15],
            [13,19,12,17,9,18,13,9,1,12,6,9,15,13,9,3,4,4,0,15,15,4,16,9,16,13,1,13,4,6],
            [17,5,11,3,3,15,9,16,8,1,15,14,9,12,13,8,17,1,16,7,15,17,18,8,11,16,19,14,7,8],
            [6,10,18,16,4,10,2,14,6,2,1,1,18,0,6,17,6,15,17,0,5,13,11,4,8,10,8,1,10,13],
            [13,0,3,2,9,14,3,5,14,11,4,13,0,8,5,14,14,8,19,7,14,10,16,14,8,19,19,2,6,19],
            [5,3,4,5,10,19,2,5,8,10,9,6,11,4,4,12,10,15,17,15,8,9,5,19,14,16,12,16,16,5]]

verification_grid = deepcopy(grid) #to check correctness of answer in the end

print(datetime.now(), "Start, N =", N, "Step limit =", STEP_LIMIT, " BONUS =", BONUS)
pointsum = 1 #max GP possible (starting with GP 1)
populated = 0 #number of non-empty cells in the grid
maxnum = 0 #highest value available in the grid in a cell
for row in range(N):
    for col in range(N):
        if grid[row][col] > 0:
            populated += 1
            pointsum += grid[row][col]
            if grid[row][col] > maxnum:
                maxnum = grid[row][col]
maxnum *= maxnum #to convert max GP possible into max size possible
x = math.ceil(math.sqrt(pointsum))
gp_size_map = [0]*((x*x)+1) #map of GP to size
curr = 1
prevsize = 1
for i in range(2,x+1):
    sqnum = i*i
    while curr < sqnum:
        gp_size_map[curr] = prevsize
        curr += 1
    prevsize = i

#DP function for main puzzle to determine path to GP 361 in <= 100 steps
def recurs_process(grid, curr_row, curr_col, curr_gp, rem_cells, rem_steps, pathlist, curr_state, visited, direction):
    if rem_steps < rem_cells-1 or rem_steps < 300:
        return (False, None, None, None)
    curr_cell_val = grid[curr_row][curr_col]
    curr_gp += curr_cell_val
    if curr_gp >= maxnum:
        grid[curr_row][curr_col] = 0
        pathlist.append(direction)
        return (True, curr_row, curr_col, curr_gp)

    #memoize to avoid repeating state for same board state, cell and entry direction
    new_state = curr_state | (1<<((curr_row*N)+curr_col))
    state_tuple = (new_state, curr_row, curr_col, direction)
    if state_tuple in visited:
        return (False, None, None, None)
    else:
        visited.add(state_tuple)

    if curr_cell_val > 0:
        grid[curr_row][curr_col] = 0
        rem_cells -= 1
        
    if curr_row - 1 >= 0 and grid[curr_row-1][curr_col] <= gp_size_map[curr_gp]:
        ret = recurs_process(grid, curr_row-1, curr_col, curr_gp, rem_cells, rem_steps-1, pathlist, new_state, visited, 'U')
        if ret[0]:
            pathlist.append(direction)
            return ret
    if curr_row + 1 < N and grid[curr_row+1][curr_col] <= gp_size_map[curr_gp]:
        ret = recurs_process(grid, curr_row+1, curr_col, curr_gp, rem_cells, rem_steps-1, pathlist, new_state, visited, 'D')
        if ret[0]:
            pathlist.append(direction)
            return ret
    if curr_col - 1 >= 0 and grid[curr_row][curr_col-1] <= gp_size_map[curr_gp]:
        ret = recurs_process(grid, curr_row, curr_col-1, curr_gp, rem_cells, rem_steps-1, pathlist, new_state, visited, 'L')
        if ret[0]:
            pathlist.append(direction)
            return ret
    if curr_col + 1 < N and grid[curr_row][curr_col+1] <= gp_size_map[curr_gp]:
        ret = recurs_process(grid, curr_row, curr_col+1, curr_gp, rem_cells, rem_steps-1, pathlist, new_state, visited, 'R')
        if ret[0]:
            pathlist.append(direction)
            return ret

    #backtracking, so undo cell changes (if changed) and state
    if curr_cell_val > 0:
        grid[curr_row][curr_col] = curr_cell_val
    visited.remove(state_tuple)
    return (False, None, None, None)

#verify the correctness of the full path found, and print it
def verify_print_sol(fullpath):
    numsteps = len(fullpath)
    if numsteps > STEP_LIMIT:
        print("Path length limit exceeded, limit =", STEP_LIMIT, "Path length =", numsteps)
        return False
    curr_row = 0
    curr_col = 0
    curr_gp = 1
    pathstr = ""
    for direction in fullpath:
        if direction == 'U':
            curr_row -= 1
        elif direction == 'D':
            curr_row += 1
        elif direction == 'L':
            curr_col -= 1
        elif direction == 'R':
            curr_col += 1

        if verification_grid[curr_row][curr_col] > gp_size_map[curr_gp]:
            print("GP ERROR:", gp_size_map[curr_gp], curr_row, curr_col, verification_grid[curr_row][curr_col])
            return False
        else:
            curr_gp += verification_grid[curr_row][curr_col]
            verification_grid[curr_row][curr_col] = 0
        pathstr += direction

    if not BONUS:
        for row in verification_grid:
            for cell_val in row:
                if cell_val != 0:
                    print("ERROR: Non-zero cell val")
                    return False
        print("Verified by playing the steps, no cell size violations, grid becomes empty within step limit")
    else:
        curr_size = math.floor(math.sqrt(curr_gp))
        if curr_size < 30:
            print("Goal size not achieved, size needed:", 30, "Size achieved:", curr_size)
            return False
        else:
            print("Size reached:", curr_size)
            print("Verified by playing the steps, no cell size violations, desired size achieved within step limit")

    print("Total number of steps:", numsteps, "GP reached:", curr_gp)
    print("Path string:")
    print(pathstr)
    return True

'''
For main puzzle, function to sweep through all 20x20 cells in exactly 20x20 steps after path
to GP of 361 has been found in <= 100 steps, starting from the cell we landed in when GP of 361
was reached, regardless of where that cell is located in the grid.
In this function, N is assumed to be even (as is the case in the main puzzle where N = 20).
'''
def finish_process(ret_tuple, pathlist):
    fullpath = []
    #path so far to reach GP 361
    for i in range(len(pathlist)-2, -1, -1):
        fullpath.append(pathlist[i])

    #Special handling if GP 361 was reached in a cell in the top row.
    #Sweep order is different if that cell is in an even or odd column.
    if ret_tuple[1] == 0:
        if ret_tuple[2]%2 == 0:
            for i in range(N-1 - ret[2]):
                fullpath.append('R')
            fullpath.append('D')
            for col in range(N-1 - ret[2]):
                direction = 'U'
                if col%2 == 1:
                    direction = 'D'
                for row in range(N-2):
                    fullpath.append(direction)
                fullpath.append('L')
            for col in range(ret[2], -1, -1):
                direction = 'U'
                if col%2 == 1:
                    direction = 'D'
                for row in range(N-1):
                    fullpath.append(direction)
                fullpath.append('L')
            fullpath.pop(-1)
        else:
            for i in range(ret[2]):
                fullpath.append('L')
            fullpath.append('D')
            for col in range(ret[2]):
                direction = 'D'
                if col%2 == 1:
                    direction = 'U'
                for row in range(N-2):
                    fullpath.append(direction)
                fullpath.append('R')
            for col in range(ret[2], N):
                direction = 'U'
                if col%2 == 1:
                    direction = 'D'
                for row in range(N-1):
                    fullpath.append(direction)
                fullpath.append('R')
            fullpath.pop(-1)
        if verify_print_sol(fullpath):
            return True
        else:
            return False

    #For GP 361 being reached in a cell in any row other than top row.
    #Sweep order is different if that cell is in an even or odd column.
    if ret_tuple[2]%2 == 0:
        for i in range(N-1-ret[2]):
            fullpath.append('R')
        fullpath.append('U')
        for col in range(N-1,-1,-1):
            direction = 'D'
            if col%2 == 1:
                direction = 'U'
            for row in range(ret[1]-1):
                fullpath.append(direction)
            fullpath.append('L')
        fullpath[-1] = 'D'

        for col in range(ret[2]+1):
            direction = 'D'
            if col%2 == 1:
                direction = 'U'
            for row in range(N-1 - ret[1]):
                fullpath.append(direction)
            fullpath.append('R')

        for col in range(ret[2]+1,N):
            direction = 'D'
            if col%2 == 1:
                direction = 'U'
            for row in range(N-2 - ret[1]):
                fullpath.append(direction)
            fullpath.append('R')
        fullpath.pop(-1)
    else:
        for i in range(ret[2]):
            fullpath.append('L')
        fullpath.append('U')
        for col in range(N):
            direction = 'U'
            if col%2 == 1:
                direction = 'D'
            for row in range(ret[1]-1):
                fullpath.append(direction)
            fullpath.append('R')
        fullpath[-1] = 'D'

        for col in range(N-1, ret[2]-1, -1):
            direction = 'U'
            if col%2 == 1:
                direction = 'D'
            for row in range(N-1 - ret[1]):
                fullpath.append(direction)
            fullpath.append('L')

        for col in range(ret[2]-1,-1,-1):
            direction = 'U'
            if col%2 == 1:
                direction = 'D'
            for row in range(N-2 - ret[1]):
                fullpath.append(direction)
            fullpath.append('L')
        fullpath.pop(-1)

    if verify_print_sol(fullpath):
        return True
    else:
        return False
    
path = []
if not BONUS:
    visited_set = set()
    ret = recurs_process(grid, 0, 0, 1, populated, 400, path, 0, visited_set, ' ')
    if ret[0]:
        print("Successful pivot cell row, column, GP:", ret[1], ret[2], ret[3])
        print("Number of steps so far from starting state:", len(path)-1)
        if finish_process(ret, path):
            print(datetime.now(), "Solution found, verified and printed, BONUS =", BONUS)
else:
    #Verify and print the bonus path found by hand
    pathstr = "RRRRDDDDLDLLDRRDRDDRURLUUUDRRURUDRDRDLDURRUULURULULRUURDDRURDDDRDRDDLULLUURRURRRRDDLULDDRDDRUURDRUUURDDDDDRDDDRRURURRRURULUUR"
    if verify_print_sol(pathstr):
        print(datetime.now(), "Manual solution verified and printed, BONUS =", BONUS)

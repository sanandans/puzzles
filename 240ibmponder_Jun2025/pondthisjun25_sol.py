'''
My IBM Ponder This June '25 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/June2025.html
Sanandan Swaminathan, submitted May 30, 2025

I first solved the main puzzle with pen and paper, and also wrote a function just to play out the
strategy and print the answer string. While my manual strategy for the main puzzle would work for
arbitrarily large grids (N >= 5) and even rectangular ones, it doesn't quite port for starting cells like
the one in the bonus puzzle. The search space for the bonus puzzle is reasonably small, so I wrote a
DFS routine to solve the bonus puzzle. For the main puzzle, the aha moment (which came in a movie theater!)
was realizing that we could simply set up bumper guards of red cells as we move through the grid. The outside
of the grid already serves as a bumper guard. Imagine a long strip of paper with rows of 3 cells - blue, blue,
red. Unfurl it along the left edge of the grid, turn it 90 degrees to the right at the bottom left corner,
roll it along the bottom edge, turn it 90 degrees to the north at the bottom right corner, and so on. This
would create a spiral going towards the center of the grid. We can play the game along this spiral path. The
"blue, blue, red" in every row of the strip we roll means start from a blue (the top left corner cell in
the beginning), go right to turn that white cell into blue and the subsequent cell in that direction to red,
then swing back southwest to make that white cell blue, then swing right again, and so on. There are some
manoeuvres to make when we need to turn the strip 90 degrees. The moves would always be safe because we would
be creating guardrails of red cells as we go (or use existing guardrails including the virtual ones we have all
around the grid). This gives us a solution in linear time. This would work for any large grid, even rectanular
grids, with width and height at least 5, when starting at a corner. For smaller grids, we could simply solve by
hand (some small grids are not solvable, for example a 1 x 4). If we wanted to solve a 5 x 5 or 6 x 6 grid, we
would turn 180 degrees when we reach the bottom. For a 7 x 7, we would do the same, except also creatng red cells
on both flanks as we move up. For an 8 x 8 or 9 x 9, we would turn 180 degrees again when we reach the top. This
strategy of taking a long strip and rolling and turning it should work for all rectangular grids >= 5 x 5.

For the bonus puzzle with start cell at (4,4), we can quickly see that a patterned path (like for the main
puzzle) won't work. But the grid size (10 x 10) is small enough for us to just do a depth-first search for
an answer. The grid is treated as a 12 x 12 grid, with red cells bordering the actual 10 x 10 grid all around.
A visited set is maintained to avoid processing a visited state again. State of the grid is treated as a
144-digit ternary number since there are 3 colors involved. When a white cell (digit 0) changes to blue
(or red), the digit at that position changes to 1 for blue (or 2 for red). Each different state of the grid
is a different ternary number. Also, the white cells remaining at any point of the game should be in a single
connected component; if there are white cells in unconnected somponents, the game cannot be completed. So, it
is checked if a move would break this condition; if yes, we can backtrack. Since the recursion stack will
never be too deep (there are only 99 white cells at the start of the bonus game), I went with recursive DFS
(iterative DFS would also be fine).

The answers generated were:
Main puzzle answer: ADADADADADADADADADADADADADADADADADADBEHBGBGBGBGBGBGBGBGBGBGBGBGBGBGBGBGBHCFHEHEHEHEHEHEHE
HEHEHEHEHEHEHEHEHEHFADFCFCFCFCFCFCFCFCFCFCFCFCFCFDGBDADADADADADADADADADADADADADBEHBGBGBGBGBGBGBGBGBGBGBHCFHEH
EHEHEHEHEHEHEHEHEHFADFCFCFCFCFCFCFCFDGBDADADADADADADADBEHBGBGBGBGBHCFHEHEHEHEHFADFCFDGBDADBEH

Bonus puzzle answer: ABABADBCFCEFDEFAFDCFDGHFAFAFAFAFAFGBGACAHABHABEBEBCFCEGFCFEBEDCACAB
'''

from datetime import datetime

#linear time function to play out the spiral path for the main puzzle
#while function is specifically written for main puzzle, it can be tweaked to generalize for
#any rectangular grid >= 5 x 5. Rather than 90 degree turns, we could take 180 degree turns, and
#create red cells on both flanks or only one flank depending on the need.
def mainPuzzle(currgrid, dirs):
    res_str = ""
    rem_whites = (N*N)-1
    #turn steps w.r.t previous regular step, sequence to be done clockwise when turning
    turn_steps = (6, 3, 3, 2, 5, 3)
    #when not turning, regular steps are just a pair that repeat an appropriate number of times
    last_dir1 = 0
    last_dir2 = 3
    #walls which bound the path (and keep changing): right, top, left, bottom
    walls = [N+1, 0, 0, N+1]
    #direction of the overall spiralling path (changes at turns): right=0, up=1, left=2, down=3
    path_dir = 3
    curr_cell = [start_cell[0], start_cell[1]]
    while True:
        #repeat regular steps until we hit a turn
        repeat_cnt = 0
        if path_dir == 0:
            repeat_cnt = walls[0] - walls[2] - 3
        elif path_dir == 1:
            repeat_cnt = walls[3] - walls[1] - 3
        elif path_dir == 2:
            repeat_cnt = walls[0] - walls[2] - 3
        elif path_dir == 3:
            repeat_cnt = walls[3] - walls[1] - 3
        for repeat in range(repeat_cnt):
            for dir in (last_dir1, last_dir2):
                curr_cell[0] += dirs[dir][0]
                curr_cell[1] += dirs[dir][1]
                if currgrid[curr_cell[0]][curr_cell[1]] != 0:
                    return "ERROR"
                currgrid[curr_cell[0]][curr_cell[1]] = 1
                whites_removed = 1
                if currgrid[curr_cell[0] + dirs[dir][0]][curr_cell[1] + dirs[dir][1]] == 1:
                    return "ERROR"
                elif currgrid[curr_cell[0] + dirs[dir][0]][curr_cell[1] + dirs[dir][1]] == 0:
                    currgrid[curr_cell[0] + dirs[dir][0]][curr_cell[1] + dirs[dir][1]] = 2
                    whites_removed += 1
                res_str += dirs[dir][2]
                rem_whites -= whites_removed
                if rem_whites == 0:
                    return res_str
        #do the turn manoeuvres
        for d in turn_steps:
            last_dir1 = last_dir2
            last_dir2 = (last_dir2 + d)%8
            res_str += dirs[last_dir2][2]
            curr_cell[0] += dirs[last_dir2][0]
            curr_cell[1] += dirs[last_dir2][1]
            if currgrid[curr_cell[0]][curr_cell[1]] != 0:
                    return "ERROR"
            currgrid[curr_cell[0]][curr_cell[1]] = 1
            whites_removed = 1
            if currgrid[curr_cell[0] + dirs[last_dir2][0]][curr_cell[1] + dirs[last_dir2][1]] == 1:
                return "ERROR"
            elif currgrid[curr_cell[0] + dirs[last_dir2][0]][curr_cell[1] + dirs[last_dir2][1]] == 0:
                currgrid[curr_cell[0] + dirs[last_dir2][0]][curr_cell[1] + dirs[last_dir2][1]] = 2
                whites_removed += 1
            rem_whites -= whites_removed
            if rem_whites == 0:
                return res_str
        #turn is done, so change the overall path direction counter clockwise, and update the walls
        path_dir = (path_dir+1)%4
        if path_dir == 0:
            walls[2] = curr_cell[1] - 1
        elif path_dir == 1:
            walls[3] = curr_cell[0] + 1
        elif path_dir == 2:
            walls[0] = curr_cell[1] + 1
        elif path_dir == 3:
            walls[1] = curr_cell[0] - 1

#function used for bonus puzzle to check if remaining white cells are in a single connected component
def numConnNodes(grid, curr_cell, dirs):
    vis = set()
    q = [(curr_cell),]
    vis.add(curr_cell)
    while len(q) > 0:
        curr = q.pop(0)
        #vis.add(curr_cell)
        for dir in dirs:
            temp_row = curr[0] + dir[0]
            temp_col = curr[1] + dir[1]
            if grid[temp_row][temp_col] != 0 or (temp_row, temp_col) in vis:
                continue
            q.append((temp_row, temp_col))
            vis.add((temp_row, temp_col))
    return len(vis)

#recursive DFS used for bonus puzzle
def recursDFS(currgrid, curr_cell, gridval, steps_str, rem_whites, vis, pos_lookup, dirs):
    if rem_whites == 0:
        return (True, steps_str) 
    for i in range(len(dirs)):
        temp_row = curr_cell[0] + dirs[i][0]
        temp_col = curr_cell[1] + dirs[i][1]
        if currgrid[temp_row][temp_col] != 0:
            continue
        temp_next_row = temp_row + dirs[i][0]
        temp_next_col = temp_col + dirs[i][1]
        if currgrid[temp_next_row][temp_next_col] == 1:
            continue
        temp_gridval = gridval + (3**pos_lookup[(temp_row, temp_col)])
        if currgrid[temp_next_row][temp_next_col] == 0:
            temp_gridval += (3**pos_lookup[(temp_next_row, temp_next_col)]) * 2
        if temp_gridval in vis:
            continue
        if numConnNodes(currgrid, (temp_row, temp_col), dirs) != rem_whites:
            continue
        vis.add(temp_gridval)
        currgrid[temp_row][temp_col] = 1
        if currgrid[temp_next_row][temp_next_col] == 0:
            currgrid[temp_next_row][temp_next_col] = 2
            ret = recursDFS(currgrid, (temp_row, temp_col), temp_gridval, steps_str+dirs[i][2], rem_whites-2, vis, pos_lookup, dirs)
            if ret[0]:
                return ret
            currgrid[temp_next_row][temp_next_col] = 0
        else:
            ret = recursDFS(currgrid, (temp_row, temp_col), temp_gridval, steps_str+dirs[i][2], rem_whites-1, vis, pos_lookup, dirs)
            if ret[0]:
                return ret
        currgrid[temp_row][temp_col] = 0
    return (False, "")

#function to verify main and bonus answers found
def verifySol(currgrid, dirs, ans):
    letter_dict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
    curr_row = start_cell[0]
    curr_col = start_cell[1]
    for c in ans:
        int_c = letter_dict[c]
        if currgrid[curr_row + dirs[int_c][0]][curr_col + dirs[int_c][1]] != 0:
            print("ERROR: Cell not white", curr_row, curr_col)
            return False
        currgrid[curr_row + dirs[int_c][0]][curr_col + dirs[int_c][1]] = 1
        if currgrid[curr_row + (dirs[int_c][0]*2)][curr_col + (dirs[int_c][1]*2)] == 1:
            print("ERROR: Next-next cell blue", curr_row, curr_col)
            return False
        currgrid[curr_row + (dirs[int_c][0]*2)][curr_col + (dirs[int_c][1]*2)] = 2
        curr_row += dirs[int_c][0]
        curr_col += dirs[int_c][1]
    for row in range(N+2):
        for col in range(N+2):
            if currgrid[row][col] == 0:
                print("ERROR: Grid still has white eventually", row, col)
                return False
    return True

#function to initialize grid with 1 (blue) in the start cell, and red cells all
#around the playing area of the grid
def initGrid(grid):
    grid[start_cell[0]][start_cell[1]] = 1
    for col in range(N+2):
        grid[0][col] = 2
    for col in range(N+2):
        grid[N+1][col] = 2
    for row in range(1, N+1):
        grid[row][0] = 2
    for row in range(1, N+1):
        grid[row][N+1] = 2
  
print(datetime.now(), "Start main puzzle")
#the given 8 directions with their net movement along row and column
dirs = ((0,1, 'A'), (1,1, 'B'), (1,0, 'C'), (1,-1, 'D'), (0,-1, 'E'), (-1,-1, 'F'), (-1,0, 'G'), (-1,1, 'H'))
N = 20 #main puzzle
start_cell = (1, 1) #border of red cells is put all around the grid, hence start cell shifted from (0,0)
# in the grid, 0 = white (empty), 1 = blue (visited), 2 = red (forbidden) 
grid = [[0 for _ in range(N+2)] for _ in range(N+2)]
initGrid(grid)
ans_str = mainPuzzle(grid, dirs)
print(datetime.now(), "Main puzzle answer:", ans_str)
grid = [[0 for _ in range(N+2)] for _ in range(N+2)] #grid for verify function
initGrid(grid)
if verifySol(grid, dirs, ans_str):
    print("Main puzzle answer verified\n")

print(datetime.now(), "Start bonus puzzle")
N = 10 #bonus puzzle
start_cell = (5, 5) #border of red cells is put all around the grid, hence start cell shifted from (4,4)
grid = [[0 for _ in range(N+2)] for _ in range(N+2)]
initGrid(grid)
pos_lookup = dict() #map of cell location to digit position in 144-digit state ternary number
gridval = 0 #ternary number denoting the state of the grid
tempcnt = 0
for row in range(N+2):
    for col in range(N+2):
        pos_lookup[(row, col)] = tempcnt
        gridval += grid[row][col] * (3**tempcnt)
        tempcnt += 1
vis = set() #grid states already visited during DFS
vis.add(gridval)
ret = recursDFS(grid, start_cell, gridval, "", (N*N)-1, vis, pos_lookup, dirs)
print(datetime.now(), "Bonus puzzle answer:", ret[1])
grid = [[0 for _ in range(N+2)] for _ in range(N+2)] #grid for verify function
initGrid(grid)
if verifySol(grid, dirs, ret[1]):
    print("Bonus puzzle answer verified")
print(datetime.now(), "end")

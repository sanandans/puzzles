'''
IBM Ponder This challenge main and bonus July '23
https://research.ibm.com/haifa/ponderthis/challenges/July2023.html
Sanandan Swaminathan, submitted July 4, 2023

Reminded me of the Rush Hour puzzles where vehicles have to be moved around in a traffic jam.
I did the main puzzle with pen and paper, and got an answer (with cost exactly 100):
8D4D9D5D6D7L7L3D3D2R2R1R1R7U7U6U6U5U3L3L1D1D1R3R3U9U9R5D5D5R6L6D6D
But, using pen and paper for the bonus * puzzle, the lowest cost I could get to fairly
quickly was 168 when the requirement is 150.
So, I resorted to writing the program below (of course, it works for the main puzzle as well).
Here, there are 6 types of shapes, and 9 shapes in total (three of the shape types repeat).
Shape numbers are 1 through 9. I denote shape types as 1 through 6, and 7 to denote a blank
cell, 8 to denote a border cell. Border cells help avoid having to check if we are out of bounds.
For each of the 9 shapes, I have a reference cell, and all movements are w.r.t. the reference cell.
The general approach is to recursively (depth-first) try moves, bail out when cost limit is
crossed. I maintain a map of seen grid states versus the cost of getting there. If we arrive at a
previously seen state incurring a lower cost, we update cost, and we can pursue the paths
further (otherwise, the paths have already been explored).
I also have a solution verifier function (which is a bit of an overkill as we could check by hand).
Main puzzle runtime was about 28 seconds, and just short of 3 minutes for the bonus *.
Speed could potentially be increased by also tracking min possible cost from a grid state
to the goal. As we bail out on crossing the cost limit, this would be an "at least" cost.
This can be updated if we get a lesser "at least" cost for a grid state.
On reaching a grid state, we could add the distance to this state and the "at least" cost
remaining to reach the goal to see if there's any point in proceeding down this road.

Answer found for main by the program (cost 100):
8D4D9D5D6D7L7L3D2R3D2R1R1R7U7U5U5U6U3L6L3L1D1D1R3R3U9U9R6D5D6D5D6R

Answer found for bonus * by the program (cost 150):
8D4D7D9D7L6R5R1D1D2L3L4L4D3R2R3R2R1U1U7L5L6L4L3D2R4U4U4L2L3U8U9R9R7D9R7R5D1D5R1D1D4L2L3L8U4D5R5R5R6D6R6R

By trying cost limit 99 for the main, and 149 for the bonus, we can also see that the
respective goal states cannot be reached within cost limit.
So, 100 and 150 are the lowest costs to reach the respective goal states.
Of course, there can clearly be multiple sequences of cost 100 and 150 that reach the goals.
In the case of 100, we can see differences (though minor) between my pen and paper solution
and the program's answer. For the 150 case, we can tweak the final movements of the 5 and 6
to get a distinct sequence, as an example.
The program bails out on finding the first solution.
'''

from datetime import datetime

#starting position in the grid of the reference cell of each of the 9 shapes 1-9 (ignore shape num 0)
shape_positions = [[0,0],[1,1],[1,2],[1,4],[1,5],[3,1],[3,2],[3,3],[3,5],[4,1]]
#starting config of the grid, 1-6 denote the distinct shape types, 7 empty cell, 8 border cell
grid_state = [[8,8,8,8,8,8,8],[8,1,2,2,3,1,8],[8,1,2,3,3,1,8], \
              [8,4,4,5,5,6,8],[8,5,5,6,6,6,8],[8,7,7,7,7,7,8],[8,8,8,8,8,8,8]]

#goal grid for the main puzzle
#GOAL_STR = str([[8,8,8,8,8,8,8],[8,5,5,7,2,2,8],[8,7,7,3,2,1,8],[8,7,3,3,1,1,8],[8,4,5,5,1,6,8],[8,7,4,6,6,6,8],[8,8,8,8,8,8,8]])
#goal grid for the bonus * puzzle
GOAL_STR = str([[8,8,8,8,8,8,8],[8,7,2,2,3,7,8],[8,1,2,3,3,6,8],[8,1,7,6,6,6,8],[8,1,7,7,4,4,8],[8,1,5,5,5,5,8],[8,8,8,8,8,8,8]])

COST_LIMIT = 150 #100 for main, 150 for bonus *
seen_config = dict()
seen_config[str(grid_state)] = 0 #stringified grid as key, lowest cost so far to this state as value

#for tiles 1 and 4 (both of type 1)
def move_type1_shape(cost, shape_num):
    shape_pos_row = shape_positions[shape_num][0]
    shape_pos_col = shape_positions[shape_num][1]
    newcost = cost+3

    #try up
    if grid_state[shape_pos_row-1][shape_pos_col] == 7:
        shape_positions[shape_num][0] = shape_pos_row-1
        grid_state[shape_pos_row-1][shape_pos_col] = 1
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'U' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row-1][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 1

    #try down
    if grid_state[shape_pos_row+2][shape_pos_col] == 7:
        shape_positions[shape_num][0] = shape_pos_row+1
        grid_state[shape_pos_row+2][shape_pos_col] = 1
        grid_state[shape_pos_row][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'D' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row+2][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col] = 1

    #try left
    if grid_state[shape_pos_row][shape_pos_col-1] == 7 and grid_state[shape_pos_row+1][shape_pos_col-1] == 7:
        shape_positions[shape_num][1] = shape_pos_col-1
        grid_state[shape_pos_row][shape_pos_col-1] = 1
        grid_state[shape_pos_row+1][shape_pos_col-1] = 1
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'L' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row+1][shape_pos_col-1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 1
        grid_state[shape_pos_row+1][shape_pos_col] = 1
        
    #try right
    if grid_state[shape_pos_row][shape_pos_col+1] == 7 and grid_state[shape_pos_row+1][shape_pos_col+1] == 7:
        shape_positions[shape_num][1] = shape_pos_col+1
        grid_state[shape_pos_row][shape_pos_col+1] = 1
        grid_state[shape_pos_row+1][shape_pos_col+1] = 1
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'R' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        grid_state[shape_pos_row+1][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 1
        grid_state[shape_pos_row+1][shape_pos_col] = 1

    return (False, "", cost)

#for tile 2 (of type 2)
def move_type2_shape(cost, shape_num):
    shape_pos_row = shape_positions[shape_num][0]
    shape_pos_col = shape_positions[shape_num][1]
    newcost = cost+2
    
    #try up
    if grid_state[shape_pos_row-1][shape_pos_col] == 7 and grid_state[shape_pos_row-1][shape_pos_col+1] == 7:
        shape_positions[shape_num][0] = shape_pos_row-1
        grid_state[shape_pos_row-1][shape_pos_col] = 2
        grid_state[shape_pos_row-1][shape_pos_col+1] = 2
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'U' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row-1][shape_pos_col] = 7
        grid_state[shape_pos_row-1][shape_pos_col+1] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 2
        grid_state[shape_pos_row][shape_pos_col+1] = 2

    #try down
    if grid_state[shape_pos_row+2][shape_pos_col] == 7 and grid_state[shape_pos_row+1][shape_pos_col+1] == 7:
        shape_positions[shape_num][0] = shape_pos_row+1
        grid_state[shape_pos_row+2][shape_pos_col] = 2
        grid_state[shape_pos_row+1][shape_pos_col+1] = 2
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'D' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row+2][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 2
        grid_state[shape_pos_row][shape_pos_col+1] = 2

    #try left
    if grid_state[shape_pos_row][shape_pos_col-1] == 7 and grid_state[shape_pos_row+1][shape_pos_col-1] == 7:
        shape_positions[shape_num][1] = shape_pos_col-1
        grid_state[shape_pos_row][shape_pos_col-1] = 2
        grid_state[shape_pos_row+1][shape_pos_col-1] = 2
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'L' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row+1][shape_pos_col-1] = 7
        grid_state[shape_pos_row][shape_pos_col+1] = 2
        grid_state[shape_pos_row+1][shape_pos_col] = 2
        
    #try right
    if grid_state[shape_pos_row][shape_pos_col+2] == 7 and grid_state[shape_pos_row+1][shape_pos_col+1] == 7:
        shape_positions[shape_num][1] = shape_pos_col+1
        grid_state[shape_pos_row][shape_pos_col+2] = 2
        grid_state[shape_pos_row+1][shape_pos_col+1] = 2
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'R' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col+2] = 7
        grid_state[shape_pos_row+1][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 2
        grid_state[shape_pos_row+1][shape_pos_col] = 2

    return (False, "", cost)

#for tile 3 (of type 3)
def move_type3_shape(cost, shape_num):
    shape_pos_row = shape_positions[shape_num][0]
    shape_pos_col = shape_positions[shape_num][1]
    newcost = cost+2

    #try up
    if grid_state[shape_pos_row-1][shape_pos_col] == 7 and grid_state[shape_pos_row][shape_pos_col-1] == 7:
        shape_positions[shape_num][0] = shape_pos_row-1
        grid_state[shape_pos_row-1][shape_pos_col] = 3
        grid_state[shape_pos_row][shape_pos_col-1] = 3
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col-1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'U' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row-1][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 3
        grid_state[shape_pos_row+1][shape_pos_col-1] = 3

    #try down
    if grid_state[shape_pos_row+2][shape_pos_col] == 7 and grid_state[shape_pos_row+2][shape_pos_col-1] == 7:
        shape_positions[shape_num][0] = shape_pos_row+1
        grid_state[shape_pos_row+2][shape_pos_col] = 3
        grid_state[shape_pos_row+2][shape_pos_col-1] = 3
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col-1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'D' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row+2][shape_pos_col] = 7
        grid_state[shape_pos_row+2][shape_pos_col-1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 3
        grid_state[shape_pos_row+1][shape_pos_col-1] = 3

    #try left
    if grid_state[shape_pos_row][shape_pos_col-1] == 7 and grid_state[shape_pos_row+1][shape_pos_col-2] == 7:
        shape_positions[shape_num][1] = shape_pos_col-1
        grid_state[shape_pos_row][shape_pos_col-1] = 3
        grid_state[shape_pos_row+1][shape_pos_col-2] = 3
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'L' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row+1][shape_pos_col-2] = 7
        grid_state[shape_pos_row][shape_pos_col] = 3
        grid_state[shape_pos_row+1][shape_pos_col] = 3
        
    #try right
    if grid_state[shape_pos_row][shape_pos_col+1] == 7 and grid_state[shape_pos_row+1][shape_pos_col+1] == 7:
        shape_positions[shape_num][1] = shape_pos_col+1
        grid_state[shape_pos_row][shape_pos_col+1] = 3
        grid_state[shape_pos_row+1][shape_pos_col+1] = 3
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col-1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'R' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        grid_state[shape_pos_row+1][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 3
        grid_state[shape_pos_row+1][shape_pos_col-1] = 3

    return (False, "", cost)

#for tiles 5 and 6 (both of type 4)
def move_type4_shape(cost, shape_num):
    shape_pos_row = shape_positions[shape_num][0]
    shape_pos_col = shape_positions[shape_num][1]
    newcost = cost+4

    #try up
    if grid_state[shape_pos_row-1][shape_pos_col] == 7:
        shape_positions[shape_num][0] = shape_pos_row-1
        grid_state[shape_pos_row-1][shape_pos_col] = 4
        grid_state[shape_pos_row][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'U' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row-1][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col] = 4

    #try down
    if grid_state[shape_pos_row+1][shape_pos_col] == 7:
        shape_positions[shape_num][0] = shape_pos_row+1
        grid_state[shape_pos_row+1][shape_pos_col] = 4
        grid_state[shape_pos_row][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'D' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col] = 4

    #try left
    if grid_state[shape_pos_row][shape_pos_col-1] == 7:
        shape_positions[shape_num][1] = shape_pos_col-1
        grid_state[shape_pos_row][shape_pos_col-1] = 4
        grid_state[shape_pos_row][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'L' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 4
        
    #try right
    if grid_state[shape_pos_row][shape_pos_col+1] == 7:
        shape_positions[shape_num][1] = shape_pos_col+1
        grid_state[shape_pos_row][shape_pos_col+1] = 4
        grid_state[shape_pos_row][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'R' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 4

    return (False, "", cost)

#for tiles 7 and 9 (both of type 5)
def move_type5_shape(cost, shape_num):
    shape_pos_row = shape_positions[shape_num][0]
    shape_pos_col = shape_positions[shape_num][1]
    newcost = cost+3

    #try up
    if grid_state[shape_pos_row-1][shape_pos_col] == 7 and grid_state[shape_pos_row-1][shape_pos_col+1] == 7:
        shape_positions[shape_num][0] = shape_pos_row-1
        grid_state[shape_pos_row-1][shape_pos_col] = 5
        grid_state[shape_pos_row-1][shape_pos_col+1] = 5
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'U' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row-1][shape_pos_col] = 7
        grid_state[shape_pos_row-1][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 5
        grid_state[shape_pos_row][shape_pos_col+1] = 5

    #try down
    if grid_state[shape_pos_row+1][shape_pos_col] == 7 and grid_state[shape_pos_row+1][shape_pos_col+1] == 7:
        shape_positions[shape_num][0] = shape_pos_row+1
        grid_state[shape_pos_row+1][shape_pos_col] = 5
        grid_state[shape_pos_row+1][shape_pos_col+1] = 5
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'D' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 5
        grid_state[shape_pos_row][shape_pos_col+1] = 5

    #try left
    if grid_state[shape_pos_row][shape_pos_col-1] == 7:
        shape_positions[shape_num][1] = shape_pos_col-1
        grid_state[shape_pos_row][shape_pos_col-1] = 5
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'L' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row][shape_pos_col+1] = 5
        
    #try right
    if grid_state[shape_pos_row][shape_pos_col+2] == 7:
        shape_positions[shape_num][1] = shape_pos_col+1
        grid_state[shape_pos_row][shape_pos_col+2] = 5
        grid_state[shape_pos_row][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'R' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col+2] = 7
        grid_state[shape_pos_row][shape_pos_col] = 5

    return (False, "", cost)

#for tile 8 (of type 6)
def move_type6_shape(cost, shape_num):
    shape_pos_row = shape_positions[shape_num][0]
    shape_pos_col = shape_positions[shape_num][1]
    newcost = cost+1

    #try up
    if grid_state[shape_pos_row-1][shape_pos_col] == 7 and grid_state[shape_pos_row][shape_pos_col-2] == 7 \
       and grid_state[shape_pos_row][shape_pos_col-1] == 7:
        shape_positions[shape_num][0] = shape_pos_row-1
        grid_state[shape_pos_row-1][shape_pos_col] = 6
        grid_state[shape_pos_row][shape_pos_col-2] = 6
        grid_state[shape_pos_row][shape_pos_col-1] = 6
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col-2] = 7
        grid_state[shape_pos_row+1][shape_pos_col-1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'U' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row-1][shape_pos_col] = 7
        grid_state[shape_pos_row][shape_pos_col-2] = 7
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 6
        grid_state[shape_pos_row+1][shape_pos_col-2] = 6
        grid_state[shape_pos_row+1][shape_pos_col-1] = 6

    #try down
    if grid_state[shape_pos_row+2][shape_pos_col] == 7 and grid_state[shape_pos_row+2][shape_pos_col-2] == 7 \
       and grid_state[shape_pos_row+2][shape_pos_col-1] == 7:
        shape_positions[shape_num][0] = shape_pos_row+1
        grid_state[shape_pos_row+2][shape_pos_col] = 6
        grid_state[shape_pos_row+2][shape_pos_col-2] = 6
        grid_state[shape_pos_row+2][shape_pos_col-1] = 6
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col-2] = 7
        grid_state[shape_pos_row+1][shape_pos_col-1] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'D' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][0] = shape_pos_row
        grid_state[shape_pos_row+2][shape_pos_col] = 7
        grid_state[shape_pos_row+2][shape_pos_col-2] = 7
        grid_state[shape_pos_row+2][shape_pos_col-1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 6
        grid_state[shape_pos_row+1][shape_pos_col-2] = 6
        grid_state[shape_pos_row+1][shape_pos_col-1] = 6

    #try left
    if grid_state[shape_pos_row][shape_pos_col-1] == 7 and grid_state[shape_pos_row+1][shape_pos_col-3] == 7:
        shape_positions[shape_num][1] = shape_pos_col-1
        grid_state[shape_pos_row][shape_pos_col-1] = 6
        grid_state[shape_pos_row+1][shape_pos_col-3] = 6
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'L' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col-1] = 7
        grid_state[shape_pos_row+1][shape_pos_col-3] = 7
        grid_state[shape_pos_row][shape_pos_col] = 6
        grid_state[shape_pos_row+1][shape_pos_col] = 6
        
    #try right
    if grid_state[shape_pos_row][shape_pos_col+1] == 7 and grid_state[shape_pos_row+1][shape_pos_col+1] == 7:
        shape_positions[shape_num][1] = shape_pos_col+1
        grid_state[shape_pos_row][shape_pos_col+1] = 6
        grid_state[shape_pos_row+1][shape_pos_col+1] = 6
        grid_state[shape_pos_row][shape_pos_col] = 7
        grid_state[shape_pos_row+1][shape_pos_col-2] = 7
        tempstr = str(grid_state)
        if (tempstr in seen_config.keys() and seen_config[tempstr] > newcost) \
           or tempstr not in seen_config.keys():
            seen_config[tempstr] = newcost
            result_tuple = recurs_find_sol(newcost)
            if result_tuple[0] == True:
                return (True, result_tuple[1] + 'R' + str(shape_num), result_tuple[2])
        shape_positions[shape_num][1] = shape_pos_col
        grid_state[shape_pos_row][shape_pos_col+1] = 7
        grid_state[shape_pos_row+1][shape_pos_col+1] = 7
        grid_state[shape_pos_row][shape_pos_col] = 6
        grid_state[shape_pos_row+1][shape_pos_col-2] = 6

    return (False, "", cost)

def recurs_find_sol(cost):

    if cost > COST_LIMIT:
        return (False, "", cost)
    
    if str(grid_state) == GOAL_STR:
        return (True, "", cost)

    #try moving each shape.
    #Some sort of signaling by empty cells to "eligible" shapes could be better,
    #but the simple approach below could be fast enough.
    result_tuple = move_type6_shape(cost, 8)
    if result_tuple[0] == True:
        return result_tuple
    result_tuple = move_type2_shape(cost, 2)
    if result_tuple[0] == True:
        return result_tuple  
    result_tuple = move_type3_shape(cost, 3)
    if result_tuple[0] == True:
        return result_tuple 
    result_tuple = move_type1_shape(cost, 1)
    if result_tuple[0] == True:
        return result_tuple 
    result_tuple = move_type1_shape(cost, 4)
    if result_tuple[0] == True:
        return result_tuple
    result_tuple = move_type5_shape(cost, 7)
    if result_tuple[0] == True:
        return result_tuple 
    result_tuple = move_type5_shape(cost, 9)
    if result_tuple[0] == True:
        return result_tuple
    result_tuple = move_type4_shape(cost, 5)
    if result_tuple[0] == True:
        return result_tuple
    result_tuple = move_type4_shape(cost, 6)
    if result_tuple[0] == True:
        return result_tuple
    
    return (False, "", cost)

def verify_sol(arr, shape_positions, solstr):
    cost = 0

    for i in range(0,len(solstr),2):
        shapenum = int(solstr[i])
        direction = solstr[i+1]
        shape_pos_row = shape_positions[shapenum][0]
        shape_pos_col = shape_positions[shapenum][1]
    
        if direction == 'U':
            if shapenum == 1 or shapenum == 4:
                if arr[shape_pos_row-1][shape_pos_col] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row-1][shape_pos_col] = 1
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    shape_positions[shapenum][0] = shape_pos_row-1
                    cost += 3
            elif shapenum == 2:
                if arr[shape_pos_row-1][shape_pos_col] != 7 or arr[shape_pos_row-1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row-1][shape_pos_col] = 2
                    arr[shape_pos_row-1][shape_pos_col+1] = 2
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    arr[shape_pos_row][shape_pos_col+1] = 7
                    shape_positions[shapenum][0] = shape_pos_row-1
                    cost += 2
            elif shapenum == 3:
                if arr[shape_pos_row-1][shape_pos_col] != 7 or arr[shape_pos_row][shape_pos_col-1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row-1][shape_pos_col] = 3
                    arr[shape_pos_row][shape_pos_col-1] = 3
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col-1] = 7
                    shape_positions[shapenum][0] = shape_pos_row-1
                    cost += 2
            elif shapenum == 5 or shapenum == 6:
                if arr[shape_pos_row-1][shape_pos_col] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row-1][shape_pos_col] = 4
                    arr[shape_pos_row][shape_pos_col] = 7
                    shape_positions[shapenum][0] = shape_pos_row-1
                    cost += 4
            elif shapenum == 7 or shapenum == 9:
                if arr[shape_pos_row-1][shape_pos_col] != 7 or arr[shape_pos_row-1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row-1][shape_pos_col] = 5
                    arr[shape_pos_row-1][shape_pos_col+1] = 5
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row][shape_pos_col+1] = 7
                    shape_positions[shapenum][0] = shape_pos_row-1
                    cost += 3
            elif shapenum == 8:
                if arr[shape_pos_row-1][shape_pos_col] != 7 or arr[shape_pos_row][shape_pos_col-1] != 7 or arr[shape_pos_row][shape_pos_col-2] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row-1][shape_pos_col] = 6
                    arr[shape_pos_row][shape_pos_col-1] = 6
                    arr[shape_pos_row][shape_pos_col-2] = 6
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col-1] = 7
                    arr[shape_pos_row+1][shape_pos_col-2] = 7
                    shape_positions[shapenum][0] = shape_pos_row-1
                    cost += 1
               
        elif direction == 'D':
            if shapenum == 1 or shapenum == 4:
                if arr[shape_pos_row+2][shape_pos_col] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row+2][shape_pos_col] = 1
                    arr[shape_pos_row][shape_pos_col] = 7
                    shape_positions[shapenum][0] = shape_pos_row+1
                    cost += 3
            elif shapenum == 2:
                if arr[shape_pos_row+2][shape_pos_col] != 7 or arr[shape_pos_row+1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row+2][shape_pos_col] = 2
                    arr[shape_pos_row+1][shape_pos_col+1] = 2
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row][shape_pos_col+1] = 7
                    shape_positions[shapenum][0] = shape_pos_row+1
                    cost += 2
            elif shapenum == 3:
                if arr[shape_pos_row+2][shape_pos_col] != 7 or arr[shape_pos_row+2][shape_pos_col-1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row+2][shape_pos_col] = 3
                    arr[shape_pos_row+2][shape_pos_col-1] = 3
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col-1] = 7
                    shape_positions[shapenum][0] = shape_pos_row+1
                    cost += 2
            elif shapenum == 5 or shapenum == 6:
                if arr[shape_pos_row+1][shape_pos_col] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row+1][shape_pos_col] = 4
                    arr[shape_pos_row][shape_pos_col] = 7
                    shape_positions[shapenum][0] = shape_pos_row+1
                    cost += 4
            elif shapenum == 7 or shapenum == 9:
                if arr[shape_pos_row+1][shape_pos_col] != 7 or arr[shape_pos_row+1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row+1][shape_pos_col] = 5
                    arr[shape_pos_row+1][shape_pos_col+1] = 5
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row][shape_pos_col+1] = 7
                    shape_positions[shapenum][0] = shape_pos_row+1
                    cost += 3
            elif shapenum == 8:
                if arr[shape_pos_row+2][shape_pos_col] != 7 or arr[shape_pos_row+2][shape_pos_col-1] != 7 or arr[shape_pos_row+2][shape_pos_col-2] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row+2][shape_pos_col] = 6
                    arr[shape_pos_row+2][shape_pos_col-1] = 6
                    arr[shape_pos_row+2][shape_pos_col-2] = 6
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col-1] = 7
                    arr[shape_pos_row+1][shape_pos_col-2] = 7
                    shape_positions[shapenum][0] = shape_pos_row+1
                    cost += 1

        elif direction == 'L':
            if shapenum == 1 or shapenum == 4:
                if arr[shape_pos_row][shape_pos_col-1] != 7 or arr[shape_pos_row+1][shape_pos_col-1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col-1] = 1
                    arr[shape_pos_row+1][shape_pos_col-1] = 1
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col-1
                    cost += 3
            elif shapenum == 2:
                if arr[shape_pos_row][shape_pos_col-1] != 7 or arr[shape_pos_row+1][shape_pos_col-1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col-1] = 2
                    arr[shape_pos_row+1][shape_pos_col-1] = 2
                    arr[shape_pos_row][shape_pos_col+1] = 7
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col-1
                    cost += 2
            elif shapenum == 3:
                if arr[shape_pos_row][shape_pos_col-1] != 7 or arr[shape_pos_row+1][shape_pos_col-2] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col-1] = 3
                    arr[shape_pos_row+1][shape_pos_col-2] = 3
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col-1
                    cost += 2
            elif shapenum == 5 or shapenum == 6:
                if arr[shape_pos_row][shape_pos_col-1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col-1] = 4
                    arr[shape_pos_row][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col-1
                    cost += 4
            elif shapenum == 7 or shapenum == 9:
                if arr[shape_pos_row][shape_pos_col-1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col-1] = 5
                    arr[shape_pos_row][shape_pos_col+1] = 7
                    shape_positions[shapenum][1] = shape_pos_col-1
                    cost += 3
            elif shapenum == 8:
                if arr[shape_pos_row][shape_pos_col-1] != 7 or arr[shape_pos_row+1][shape_pos_col-3] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col-1] = 6
                    arr[shape_pos_row+1][shape_pos_col-3] = 6
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col-1
                    cost += 1

        elif direction == 'R':
            if shapenum == 1 or shapenum == 4:
                if arr[shape_pos_row][shape_pos_col+1] != 7 or arr[shape_pos_row+1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col+1] = 1
                    arr[shape_pos_row+1][shape_pos_col+1] = 1
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col+1
                    cost += 3
            elif shapenum == 2:
                if arr[shape_pos_row][shape_pos_col+2] != 7 or arr[shape_pos_row+1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col+2] = 2
                    arr[shape_pos_row+1][shape_pos_col+1] = 2
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col+1
                    cost += 2
            elif shapenum == 3:
                if arr[shape_pos_row][shape_pos_col+1] != 7 or arr[shape_pos_row+1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col+1] = 3
                    arr[shape_pos_row+1][shape_pos_col+1] = 3
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col-1] = 7
                    shape_positions[shapenum][1] = shape_pos_col+1
                    cost += 2
            elif shapenum == 5 or shapenum == 6:
                if arr[shape_pos_row][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col+1] = 4
                    arr[shape_pos_row][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col+1
                    cost += 4
            elif shapenum == 7 or shapenum == 9:
                if arr[shape_pos_row][shape_pos_col+2] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col+2] = 5
                    arr[shape_pos_row][shape_pos_col] = 7
                    shape_positions[shapenum][1] = shape_pos_col+1
                    cost += 3
            elif shapenum == 8:
                if arr[shape_pos_row][shape_pos_col+1] != 7 or arr[shape_pos_row+1][shape_pos_col+1] != 7:
                    print("ERROR at sol str index:",i)
                    break
                else:
                    arr[shape_pos_row][shape_pos_col+1] = 6
                    arr[shape_pos_row+1][shape_pos_col+1] = 6
                    arr[shape_pos_row][shape_pos_col] = 7
                    arr[shape_pos_row+1][shape_pos_col-2] = 7
                    shape_positions[shapenum][1] = shape_pos_col+1
                    cost += 1

    if str(arr) != GOAL_STR:
        print("Final grid not matching end goal", arr)
    else:
        print("Final grid correct", arr)
        print("Solution string:", solstr)
        print("Total cost:", cost)

print("starting", datetime.now())
result_tuple = recurs_find_sol(0)
print(result_tuple)
solstr = result_tuple[1][::-1]
print("answer: ", solstr)
print("done", datetime.now())
start_shape_positions = [[0,0],[1,1],[1,2],[1,4],[1,5],[3,1],[3,2],[3,3],[3,5],[4,1]]
start_grid_state = [[8,8,8,8,8,8,8],[8,1,2,2,3,1,8],[8,1,2,3,3,1,8], \
              [8,4,4,5,5,6,8],[8,5,5,6,6,6,8],[8,7,7,7,7,7,8],[8,8,8,8,8,8,8]]
verify_sol(start_grid_state, start_shape_positions, solstr)
print("verified", datetime.now())

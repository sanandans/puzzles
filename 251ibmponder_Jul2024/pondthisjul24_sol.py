'''
My IBM Ponder This July '24 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/July2024.html
Sanandan Swaminathan, submitted July 7, 2024

Initially, I solved the main puzzle using a variant of the below program and pen-and-paper since
it wasn't clear to me whether the theoretical minimum could be achieved. Once the theoretical minimum
was achieved for the main, I tweaked the program below to directly aim for the theoretical minimum
for the bonus * puzzle. The final program is given below. It finds solutions instantaneously for both
the main and bonus * puzzles.

All 4x4 tiles that have half the squares black, and also don't contain more than two consecutive
same-color cells in any row or column, are considered initially (and then pruned). Qualifying tiles are
bucketed into equivalence classes based on rotations and/or reflections. Any tile in an equivalence class
can be transformed into any other tile in the same class using rotations and/or reflections. Tiles in
different classes cannot be transformed into each other with rotations and/or reflections. All tiles in
an equivalence class will obviously have the same number of same-color adjacent pairs (horizontal and
vertical pairs). This is the "score" of the class. Tiles are placed left to right, top to bottom in the
large grid. For every tile, tiles that are "compatible" on its right and bottom are determined. Compatible
tiles must not violate the "no more than two consecutive same-color cells" at the edge where the tiles meet.
Ideally, compatible tiles should cause no new same-color pairs at the edge.

For the main puzzle, it turns out that there is 1 equivalence class with score 0, two classes with score 3,
six with score 4, and six with score 5. If we use a tile from each of these 15 classes, we will have
a minimum score of 60 even before we start placing tiles. We must add a 16th tile which will have a score
of at least 6. Thus, the theoretical minimum is 66, and this can be achieved if we manage to place the 16
tiles such that no new same-color pairs get created at the edges where two tiles meet. Initially, I wasn't
sure if the theoretical minimum could be achieved, so I had the program place a tile from each of the 15
cheapest classes. The recursion aimed to find a minimum. Along the way, it reported an arrangement of the
15 tiles that gave a score of 65 (not too far from the theoretical min of 60 with 15 tiles). This was low
enough to try to optimize on paper. I terminated the program, and manually added a 16th tile (having score 6),
and then moved four tiles (with some rotations and/or reflections). The theoretical min of 66 with 16 tiles
was achieved fairly quickly. Then I decided to directly shoot for the theoretical min for the bonus
puzzle (184). So, I changed my definition of "compatible" tiles to be ones that strictly don't cause any new
same-color pair at the edge where two tiles meet. This made the search enormously faster. The program found
a solution instantaneously for the bonus puzzle. I retroactively ran it for the main puzzle too (though I
already had found an answer for the main puzzle using a combo of program search and pen-and-paper).
The tweaked program found a solution for the main puzzle also instantaneously. Due to the number of constraints,
I wrote some code to independently verify that none of the constraints were violated by the solution found.

Answers are given below. To run the program for the main puzzle, set BONUS variable to False; for bonus puzzle,
set it to True.

Minimal total same-color adjacent pairs (horizontal and vertical): 66 for main puzzle, 184 for bonus puzzle.

One arrangement that works for main puzzle:
0010100101010101
0101010010101010
1010101101010101
1011010100110101
0100101011001010
1011010101010100
0101001010101011
1010110101010110
0101001010101001
0110110101010110
1001011010010101
0110100101101010
1001011010010101
0110100101101010
1001001010010101
1010110101101010

One arrangement that works for bonus puzzle:
00101001001100110101
00110010110100101001
11010101011011010010
01101011001010101101
10010100110101010010
00101011001010101011
11001101010010101101
11010010101101010100
00101101010010101011
01010010101100101001
10110101011011010100
01101001010100110011
10010110101011001100
00110101010100110010
01001011011011001101
11010100100100110101
00101011011011001010
11010100100101010100
11010100101010101011
00101011010100110011
'''

from datetime import datetime
import heapq
from collections import OrderedDict

BONUS = True #set to False to run for main puzzle, True to run for bonus puzzle

CELLS_PER_ROW = 4 #number of cells in each row or column of square tile
TILE_CELLS = CELLS_PER_ROW**2 #number of cells in a tile

#TILES_PER_ROW_COL below is set as follows: 4 for main (4x4 tiles, each tile 4x4, grid has 16x16 cells), and
#5 for bonus * (5x5 tiles, each tile still 4x4, grid has 20x20 cells)
TILES_PER_ROW_COL = 4
if BONUS == True:
    TILES_PER_ROW_COL = 5

#function used only in final bonus solution verification to ensure equiv classes used have exactly 4 members
def check_num_equiv(tile_str):
    equiv_set = set()
    oldstr = ''
    for rotate in range(CELLS_PER_ROW):
        if rotate == 0:
            equiv_set.add(tile_str)
            oldstr = tile_str[:]
        else:
            newstr = ''
            for i in range(CELLS_PER_ROW*3, TILE_CELLS):
                for j in range(0, 13, CELLS_PER_ROW):
                    newstr += oldstr[i-j]
            equiv_set.add(newstr)
            oldstr = newstr[:]

        #vertical reflection
        newstr = ''
        for i in range(CELLS_PER_ROW - 1, TILE_CELLS, CELLS_PER_ROW):
            for j in range(CELLS_PER_ROW):
                newstr += oldstr[i-j]
        equiv_set.add(newstr)
        #horizontal reflection
        newstr = ''
        for i in range(CELLS_PER_ROW*3, -1, (-1)*CELLS_PER_ROW):
            for j in range(CELLS_PER_ROW):
                newstr += oldstr[i+j]
        equiv_set.add(newstr)
        #reflection over top-left to bottom-right diagonal
        newstr = ''
        for i in range(CELLS_PER_ROW):
            for j in range(0, 13, CELLS_PER_ROW):
                newstr += oldstr[i+j]
        equiv_set.add(newstr)
        #reflection over top-right to bottom-left diagonal
        newstr = ''
        for i in range(3, -1, -1):
            for j in range(CELLS_PER_ROW*3, -1, (-1)*CELLS_PER_ROW):
                newstr += oldstr[i+j]
        equiv_set.add(newstr)

    if len(equiv_set) != 4: #equiv classes used in bonus puzzle must have exactly 4 members
        print(tile_str,equiv_set)
        return False
    else:
        return True

#function to check if reflected tile has already been encountered
def check_reflection(tile, equiv):
    #vertical reflection
    newstr = ''
    for i in range(CELLS_PER_ROW - 1, TILE_CELLS, CELLS_PER_ROW):
        for j in range(CELLS_PER_ROW):
            newstr += tile[i-j]
    if newstr in equiv:
        return newstr
    #horizontal reflection
    newstr = ''
    for i in range(CELLS_PER_ROW*3, -1, (-1)*CELLS_PER_ROW):
        for j in range(CELLS_PER_ROW):
            newstr += tile[i+j]
    if newstr in equiv:
        return newstr
    #reflection over top-left to bottom-right diagonal
    newstr = ''
    for i in range(CELLS_PER_ROW):
        for j in range(0, 13, CELLS_PER_ROW):
            newstr += tile[i+j]
    if newstr in equiv:
        return newstr
    #reflection over top-right to bottom-left diagonal
    newstr = ''
    for i in range(3, -1, -1):
        for j in range(CELLS_PER_ROW*3, -1, (-1)*CELLS_PER_ROW):
            newstr += tile[i+j]
    if newstr in equiv:
        return newstr
    return ''

#recursive function to fill tiles in grid, left to right, top to bottom
def recurs_placetiles(new_pos, tiling, basetiles_set, comp_rights, comp_bottoms, \
                      basetiles, dense_tile_cnt, dense_score, dense_limit):
    if new_pos == TILES_PER_ROW_COL**2: #grid completed, solution found
        return True

    dense_cnt = 0
    #if tile being placed in column 0 (0'th tile pre-filled before initial call to this function)
    if new_pos%TILES_PER_ROW_COL == 0:
        for tile in comp_bottoms[tiling[new_pos-TILES_PER_ROW_COL]]:
            if basetiles[tile][0] in basetiles_set: #equiv class already in grid
                continue
            #allow highest-score tiles only upto the necessary number
            if basetiles[tile][1] == dense_score:
                if dense_tile_cnt == dense_limit:
                    continue
                else:
                    dense_cnt = dense_tile_cnt + 1
            else:
                dense_cnt = dense_tile_cnt
            #update grid tiling
            tiling.append(tile)
            #add equiv class to tracker to prevent reuse
            basetiles_set.add(basetiles[tile][0])
            ret = recurs_placetiles(new_pos+1, tiling, basetiles_set, comp_rights, comp_bottoms, \
                                    basetiles, dense_cnt, dense_score, dense_limit)
            if ret == True:
                return True
            #this tile didn't work, reset, try another one
            basetiles_set.remove(basetiles[tile][0])
            tiling.pop()
    #if tile being placed in row 0 (0'th tile pre-filled before initial call to this function)
    elif new_pos < TILES_PER_ROW_COL:
        for tile in comp_rights[tiling[new_pos-1]]:
            if basetiles[tile][0] in basetiles_set:
                continue
            if basetiles[tile][1] == dense_score:
                if dense_tile_cnt == dense_limit:
                    continue
                else:
                    dense_cnt = dense_tile_cnt + 1
            else:
                dense_cnt = dense_tile_cnt
            tiling.append(tile)
            basetiles_set.add(basetiles[tile][0])
            ret = recurs_placetiles(new_pos+1, tiling, basetiles_set, comp_rights, comp_bottoms, \
                                    basetiles, dense_cnt, dense_score, dense_limit)
            if ret == True:
                return True
            basetiles_set.remove(basetiles[tile][0])
            tiling.pop()
    #if tile being placed at column > 0 and row > 0
    else:
        for tile in comp_bottoms[tiling[new_pos-TILES_PER_ROW_COL]]:
            if basetiles[tile][0] in basetiles_set:
                continue
            if tile not in comp_rights[tiling[new_pos-1]]:
                continue
            if basetiles[tile][1] == dense_score:
                if dense_tile_cnt == dense_limit:
                    continue
                else:
                    dense_cnt = dense_tile_cnt + 1
            else:
                dense_cnt = dense_tile_cnt
            tiling.append(tile)
            basetiles_set.add(basetiles[tile][0])
            ret = recurs_placetiles(new_pos+1, tiling, basetiles_set, comp_rights, comp_bottoms, \
                                    basetiles, dense_cnt, dense_score, dense_limit)
            if ret == True:
                return True
            basetiles_set.remove(basetiles[tile][0])
            tiling.pop()
    #no solution found yet
    return False

#A tile contains four 4-bit binaries.
#Only 2,3,4,5,6,9,10,11,12,13 in 4-bit binary form contain at most two consecutive bits that are same.
#Create qualifying tiles, marking each tile's score (number of same-color adjacent pairs, horizontal and vertical).
tiles_list = []
for num0 in (2,3,4,5,6,9,10,11,12,13):
    row0 = format(num0, '04b')
    for num1 in (2,3,4,5,6,9,10,11,12,13):
        row1 = format(num1, '04b')
        for num2 in (2,3,4,5,6,9,10,11,12,13):
            row2 = format(num2, '04b')
            for num3 in (2,3,4,5,6,9,10,11,12,13):
                row3 = format(num3, '04b')
                #if more than two consecutive same-solor bits appear vertically, reject the tile
                if (row1[0] == row2[0] and (row0[0] == row1[0] or row3[0] == row1[0])) or \
                (row1[1] == row2[1] and (row0[1] == row1[1] or row3[1] == row1[1])) or \
                (row1[2] == row2[2] and (row0[2] == row1[2] or row3[2] == row1[2])) or \
                (row1[3] == row2[3] and (row0[3] == row1[3] or row3[3] == row1[3])):
                    continue
                tempstr = row0 + row1 + row2 + row3
                if tempstr.count('0') != TILE_CELLS//2: #half the tile's cells should be black
                    continue
                #a tile's score is the number of same-color pairs in the tile
                score = 0
                for colnum in range(CELLS_PER_ROW - 1):
                    if row0[colnum] == row0[colnum+1]:
                        score += 1
                    if row1[colnum] == row1[colnum+1]:
                        score += 1
                    if row2[colnum] == row2[colnum+1]:
                        score += 1
                    if row3[colnum] == row3[colnum+1]:
                        score += 1
                for colnum in range(4):
                    if row0[colnum] == row1[colnum]:
                        score += 1
                    if row1[colnum] == row2[colnum]:
                        score += 1
                    if row2[colnum] == row3[colnum]:
                        score += 1
                tiles_list.append((tempstr, score))

#Put each tile in its equivalence class bucket.
#The first tile encountered for an equivalence class is the base tile for that class.
#Mark each tile's equivalent base tile (and score, for quick reference).
#Map every base tile to all tiles in that equivalence class (including base tile).
tile_base = dict() #mapping of tile (key) to equivalence class; value also contains tile's score for quick access
equivs = dict() #mapping of equivalence class's base tile to all class members (including base tile)
for tile in tiles_list:
    #this tile can't already be a key in the tile_base, but we can check its 4 reflections
    base_tile = check_reflection(tile[0], equivs)
    if len(base_tile) > 0:
        tile_base[tile[0]] = (base_tile, tile[1])
        equivs[base_tile].add(tile[0])
        continue

    #Clockwise rotate this tile and check if it's already in equivalence class.
    #For each rotation, check the 4 reflections.
    equiv_found = False
    oldstr = tile[0][:]
    for rotate in range(3):
        newstr = ''
        for i in range(CELLS_PER_ROW*3, TILE_CELLS):
            for j in range(0, 13, CELLS_PER_ROW):
                newstr += oldstr[i-j]
        if newstr in equivs: #if rotated tile already exists in an equivalence class
            tile_base[tile[0]] = (newstr, tile[1])
            equivs[newstr].add(tile[0])
            equiv_found = True
            break
        else:
            base_tile = check_reflection(newstr, equivs)
            if len(base_tile) > 0: #if some reflection already exists in an equivalence class
                tile_base[tile[0]] = (base_tile, tile[1])
                equivs[base_tile].add(tile[0])
                equiv_found = True
                break
            else:
                oldstr = newstr[:]
    if equiv_found == False: #tile creates a new equivalence class
        tile_base[tile[0]] = (tile[0], tile[1])
        temp = set()
        temp.add(tile[0]) #add base tile to equivalence class's member set
        equivs[tile[0]] = temp

#Populate min heap with equivalence class scores to later extract cheapest classes.
#Note: for bonus puzzle, equivalence classes that don't have exactly 4 members can be ignored.
score_minheap = [] #min heap to extract equivalence classes having low scores
for base_tile in equivs:
    if BONUS == True:
        if len(equivs[base_tile]) == 4: #constraint only for bonus puzzle
            heapq.heappush(score_minheap, tile_base[base_tile][1])
    else:
        heapq.heappush(score_minheap, tile_base[base_tile][1])

#Determine the highest score that will be unavoidable while filling grid.
#Also determine how many highest-score equivalence classes will be needed.
DENSE_TILE_SCORE = heapq.heappop(score_minheap)
DENSE_TILE_LIMIT = 1
for i in range(1, TILES_PER_ROW_COL**2):
    temp = heapq.heappop(score_minheap)
    if temp != DENSE_TILE_SCORE:
        DENSE_TILE_SCORE = temp
        DENSE_TILE_LIMIT = 1
    else:
        DENSE_TILE_LIMIT += 1

#Make a reduced tiles list.
#Equivalence classes with score > DENSE_TILE_SCORE can be discarded.
#In bonus problem, equivalence classes that don't have exactly 4 members can be discarded.
tiles_list1 = []
for tile in tiles_list:
    base_tile = tile_base[tile[0]][0]
    if tile_base[base_tile][1] > DENSE_TILE_SCORE:
        continue
    #equivalence classes used for bonus problem must have exactly 4 members
    if BONUS == True and len(equivs[base_tile]) != 4:
        continue
    tiles_list1.append(tile)

#Grid will be filled with tiles left to right, top to bottom.
#Hence determine tiles that will be compatible to each tile, on the right and below.
#For minimum total score, a tile is "compatible" to another if joining the tiles
#won't add any same-color pair at joining edge.
compatible_rights = dict() #map of tile to tiles that can be attached to its right
compatible_bottoms = dict() #map of tile to tiles that can be attached to its bottom
for tile in tiles_list1:
    rights = OrderedDict() #tiles that can be attached to this tile's right
    bottoms = OrderedDict() #tiles that can be attached to this tile's bottom
    for next_tile in tiles_list1:
        #only non-equivalent tiles allowed to be attached
        if tile_base[next_tile[0]][0] == tile_base[tile[0]][0]:
            continue

        compatible = True
        for i in range(0, 13, CELLS_PER_ROW):
            if tile[0][i+CELLS_PER_ROW-1] == next_tile[0][i]:
                compatible = False
                break
        if compatible == True:
            rights[next_tile[0]] = None
            
        compatible = True
        for i in range(CELLS_PER_ROW):
            if tile[0][i+(CELLS_PER_ROW*3)] == next_tile[0][i]:
                compatible = False
                break
        if compatible == True:
            bottoms[next_tile[0]] = None
    compatible_rights[tile[0]] = rights
    compatible_bottoms[tile[0]] = bottoms

print("Start: Bonus flag =", BONUS, datetime.now())
#find a solution
tile_layout = [] #to capture the solution grid
base_set = set() #track equivalence classes already included in grid to prevent reuse
ret = False
for start_tile in tiles_list1:
    tile_layout.append(start_tile[0]) #first tile in grid, on top-left
    base_set.add(tile_base[start_tile[0]][0])
    dense_cnt = 0
    if start_tile[1] == DENSE_TILE_SCORE:
        dense_cnt += 1
    ret = recurs_placetiles(1, tile_layout, base_set, compatible_rights, compatible_bottoms, \
                            tile_base, dense_cnt, DENSE_TILE_SCORE, DENSE_TILE_LIMIT)
    if ret == True:
        print("A solution found", datetime.now())
        break
    #if this start tile didn't give a solution, clean up, and start again with new tile
    base_set.remove(tile_base[start_tile[0]][0])
    tile_layout.pop()
if ret == False:
    print("No sol found for theoretical minimum")
    exit(1)

#verify solution independently of the solution-finding code above; check that all constraints are satisfied
base_set = set()
grid = [[0]*TILES_PER_ROW_COL*CELLS_PER_ROW for _ in range(TILES_PER_ROW_COL*CELLS_PER_ROW)]
idx = 0
error = False
for tile in tile_layout:
    if tile.count('0') != TILE_CELLS//2:
        print("ERROR: tile", tile, "does not contain half blacks")
        error = True
        break

    if BONUS == True and check_num_equiv(tile) == False:
        print("ERROR: equiv class not having exactly 4 members as required in bonus puzzle", tile)
        error = True
        break
    
    #if tile repeated
    if tile in base_set:
        print("ERROR: tile", tile, "repeated")
        error = True
        break
    
    #we can check its 4 reflections
    temp = check_reflection(tile, base_set)
    if len(temp) > 0:
        print("ERROR: tile", tile, "already represented by", temp)
        error = True
        break

    #rotate this tile and check
    #for each rotation, check the 4 reflections
    equiv_found = False
    oldstr = tile[:]
    for rotate in range(3):
        newstr = ''
        for i in range(CELLS_PER_ROW*3, TILE_CELLS):
            for j in range(0, 13, CELLS_PER_ROW):
                newstr += oldstr[i-j]
        if newstr in base_set:
            print("ERROR: tile", tile, "already represented by", newstr)
            error = True
            equiv_found = True
            break
        else:
            temp = check_reflection(newstr, base_set)
            if len(temp) > 0:
                print("ERROR: tile", tile, "already represented by", temp)
                error = True
                equiv_found = True
                break
            else:
                oldstr = newstr[:]
    if equiv_found == True:
        break

    base_set.add(tile)

    #populate a grid for further verification
    row = (idx//TILES_PER_ROW_COL)*CELLS_PER_ROW
    col = (idx%TILES_PER_ROW_COL)*CELLS_PER_ROW
    for chridx in range(TILE_CELLS):
        temprow = row + (chridx//CELLS_PER_ROW)
        tempcol = col + (chridx%CELLS_PER_ROW)
        grid[temprow][tempcol] = tile[chridx]

    idx += 1

if error == False:
    tot_score = 0
    #verify no more than 2 consecutive same-color squares in any row, and update total grid score
    for row in range(TILES_PER_ROW_COL*CELLS_PER_ROW):
        for col in range((TILES_PER_ROW_COL*CELLS_PER_ROW) - 2):
            if grid[row][col] == grid[row][col+1]:
                if grid[row][col] == grid[row][col+2]:
                    print("ERROR: more than two consecutive same-color squares")
                    print(grid)
                    error = True
                    break
                else:
                    tot_score += 1
        if error == True:
            break
        if grid[row][(TILES_PER_ROW_COL*CELLS_PER_ROW) - 2] == \
           grid[row][(TILES_PER_ROW_COL*CELLS_PER_ROW) - 1]:
            tot_score += 1
    if error == False:
        #verify no more than 2 consecutive same-color squares in any column, and update total grid score
        for col in range(TILES_PER_ROW_COL*CELLS_PER_ROW):
            for row in range((TILES_PER_ROW_COL*CELLS_PER_ROW) - 2):
                if grid[row][col] == grid[row+1][col]:
                    if grid[row][col] == grid[row+2][col]:
                        print("ERROR: more than two consecutive same-color squares")
                        print(grid)
                        error = True
                        break
                    else:
                        tot_score += 1
            if error == True:
                break
            if grid[(TILES_PER_ROW_COL*CELLS_PER_ROW) - 2][col] == \
               grid[(TILES_PER_ROW_COL*CELLS_PER_ROW) - 1][col]:
                tot_score += 1

#if no errors found, print the solution
if error == False:
    print("Solution verified", datetime.now())
    print("Answer:")
    #print answer in specified format
    print(tot_score)
    for row in range(TILES_PER_ROW_COL*CELLS_PER_ROW):
        tempstr = ''
        for col in range(TILES_PER_ROW_COL*CELLS_PER_ROW):
            tempstr += grid[row][col]
        print(tempstr)
    
print("End", datetime.now())

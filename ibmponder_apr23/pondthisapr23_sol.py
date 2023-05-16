'''
IBM Ponder This challenge Apr 23
https://research.ibm.com/haifa/ponderthis/challenges/April2023.html
Sanandan Swaminathan, submitted April 4, 2023

Main puzzle (24 x 24 grid, using 292 steps):

[(1, 24), (18, 24), (21, 24), (23, 24), (1, 23), (11, 23), (14, 23), (15, 23), (16, 23), (18, 23), (19, 23), (24, 23), (1, 22), (2, 22), (9, 22), (11, 22), (12, 22), (18, 22), (23, 22), (24, 22), (6, 21), (8, 21), (11, 21), (12, 21), (14, 21), (15, 21), (16, 21), (22, 21), (24, 21), (1, 20), (2, 20), (5, 20), (22, 20), (4, 19), (5, 19), (17, 19), (18, 19), (20, 19), (7, 18), (10, 18), (12, 18), (21, 18), (2, 17), (4, 17), (5, 17), (10, 17), (12, 17), (13, 17), (14, 17), (17, 17), (18, 17), (19, 17), (22, 17), (3, 16), (18, 16), (23, 16), (1, 15), (4, 15), (14, 15), (17, 15), (21, 15), (24, 15), (2, 14), (6, 14), (12, 14), (14, 14), (17, 14), (18, 14), (20, 14), (1, 13), (3, 13), (7, 13), (14, 13), (17, 13), (18, 13), (20, 13), (24, 13), (1, 12), (9, 12), (15, 12), (24, 12), (10, 11), (23, 11), (7, 10), (12, 10), (24, 10), (6, 9), (11, 9), (12, 9), (19, 9), (1, 8), (4, 8), (6, 8), (10, 8), (16, 8), (2, 7), (5, 7), (7, 7), (19, 7), (21, 7), (22, 7), (2, 6), (4, 6), (6, 6), (15, 6), (16, 6), (19, 6), (20, 6), (23, 6), (2, 5), (4, 5), (5, 5), (7, 5), (12, 5), (15, 5), (18, 5), (19, 5), (22, 5), (23, 5), (3, 4), (5, 4), (10, 4), (11, 4), (15, 4), (17, 4), (20, 4), (6, 3), (9, 3), (11, 3), (12, 3), (13, 3), (15, 3), (17, 3), (18, 3), (19, 3), (4, 2), (8, 2), (14, 2), (20, 2), (23, 2), (5, 1), (6, 1), (7, 1), (14, 1), (16, 1), (19, 1), (20, 1), (21, 1), (24, 1), (7, 24), (9, 24), (11, 24), (12, 24), (13, 24), (15, 24), (20, 24), (13, 23), (17, 23), (3, 22), (8, 22), (13, 22), (18, 21), (6, 20), (9, 20), (11, 20), (16, 20), (20, 20), (1, 19), (7, 19), (8, 19), (13, 19), (22, 19), (2, 18), (8, 18), (11, 18), (22, 18), (20, 17), (10, 16), (11, 16), (13, 16), (20, 16), (22, 16), (18, 15), (19, 15), (1, 14), (19, 14), (22, 14), (24, 14), (2, 13), (4, 13), (10, 13), (11, 13), (5, 12), (17, 12), (22, 12), (4, 11), (6, 11), (14, 11), (15, 11), (24, 11), (9, 10), (14, 10), (19, 10), (1, 9), (1, 7), (4, 7), (13, 7), (7, 6), (21, 6), (24, 6), (11, 5), (1, 4), (4, 4), (8, 4), (18, 4), (23, 4), (24, 4), (10, 3), (23, 3), (24, 3), (2, 2), (3, 2), (11, 2), (15, 2), (3, 1), (3, 23), (16, 22), (4, 21), (5, 21), (19, 21), (21, 20), (21, 19), (23, 19), (13, 18), (1, 17), (3, 17), (2, 16), (21, 16), (24, 16), (2, 15), (3, 15), (6, 13), (4, 12), (12, 12), (23, 12), (5, 11), (12, 11), (10, 9), (3, 7), (1, 5), (14, 5), (1, 3), (16, 2), (22, 2), (19, 24), (22, 23), (4, 22), (22, 22), (16, 17), (3, 14), (4, 1), (9, 1), (5, 23), (5, 8), (11, 8), (9, 6), (1, 20), (1, 21), (1, 20), (1, 1), (2, 11), (2, 10), (21, 10), (2, 11), (7, 13), (7, 12), (8, 12), (7, 13), (5, 3), (5, 2), (13, 2), (5, 3), (9, 20), (10, 20), (10, 7), (12, 7), (12, 19), (9, 20), (14, 18), (15, 18), (15, 7), (14, 18)]

Each cell that is 0 initially must be toggled an odd number of times, and cells that are initially 1 must be toggled an even number of times. We can toggle a 0 cell without impacting the parities of the number of toggles of all other cells. To do this in an even by even grid, we can click the desired 0 cell and all other 46 cells in its row and column (47 clicks). Apart from the target 0 cell which gets toggled an odd number of times, other cells in its row and column get toggled an even number of times, thus not changing their state. My program calculates the number of times each cell needs to be clicked (this includes cells that are initially 0 or 1) in order to toggle every cell that was initially 0. These numbers are reduced mod2 since clicking a cell an even number of times has the same effect as not clicking it, and clicking an odd number of times is the same as clicking the cell just once. The target number of total clicks was 280. We have a 24x24 grid of cells, some of which need to be clicked once and some don't. I scan through the lightbulbs grid to click the cells that need 1 click (as long as the bulb is off), toggling the row and column. I make multiple passes through the grid. The program completed immediately. It made 5 passes and performed 266 steps. There were 14 cells that still needed to be clicked, but they were all in state 1 after 266 steps. I added 26 ending steps manually to get all lightbulbs to the 1 state. Thus, my solution has 266+26 = 292 steps.

My approach doesn't quite scale for the bonus "*" puzzle. My program reports that 429 clicks are needed, and 429 is the maximum number of steps allowed. So, unlike the main puzzle, I can't use any extraneous/redundant step. My program covers 421 steps, leaving 8 cells (all in 1 state) that still need to be clicked (in 8 steps). It feels like some sort of Hamiltonian path is needed through the 429 cells that need to be clicked, though their states change.

'''

N=30 #24 for main puzzle, 30 for bonus "*"

#starting grid for main puzzle
'''
str = '000001000000000001110011'+ \
'110100010110101000010011'+ \
'011101110000001101001110'+ \
'000110111000110101101100'+ \
'101101011010010011101010'+ \
'111000100101110100101000'+ \
'110001011100000000000101'+ \
'100000010001100000000010'+ \
'000110010010110110101001'+ \
'011101101011111011100000'+ \
'011000101010111011111100'+ \
'100011110010000100100111'+ \
'000111010010100010001110'+ \
'011001010001001111110101'+ \
'110001000010111000100000'+ \
'000000101100101000101001'+ \
'111001010010010011110110'+ \
'100000110001111111011010'+ \
'110100000011100100110010'+ \
'101000110111001110010000'+ \
'110000000010011100100101'+ \
'111111011011111100010101'+ \
'000000000110101011100000'+ \
'110001111100000011001111'
'''

#starting grid for bonus "*" puzzle
str = '110001000000100101110011001000'+ \
'010100001100011101010111100110'+ \
'000110011010011111100010100010'+ \
'111101110110011101110100110001'+ \
'000110001000100011001101100010'+ \
'101111001110110010111101001111'+ \
'001110000101101001101000001101'+ \
'111001110000101011111111110100'+ \
'110000000000110111111001100100'+ \
'111001110100111110001110111011'+ \
'111010100010010100000001101100'+ \
'010111110011001111110100001001'+ \
'010100111011000001100000011010'+ \
'010001010110111100100111001101'+ \
'111111010001011100101100110110'+ \
'101000110110010111111011001001'+ \
'111011000100101111101001100010'+ \
'101001100011010100010000100001'+ \
'111111100111111110010111110010'+ \
'010000010000011001001010010011'+ \
'111010110011011111101100110110'+ \
'011100110001101001100000000110'+ \
'111110100101010000100011011010'+ \
'111100011111000011110001001111'+ \
'111000111111101011111011100100'+ \
'101011000011001110101011000011'+ \
'001101011101000001100101101001'+ \
'010010100000011011100101010001'+ \
'010111101001110100010110010010'+ \
'110000011010111110100110000010'

#populate input grid into NxN array
t = [ [0]*N for i in range(N)]
cnt=0
row=0
for chr in str:
    col = cnt%N
    t[row][col] = int(chr)
    cnt += 1
    if col == N-1:
        row +=1
print("input grid", t)

rownumzeros = [0]*N
colnumzeros = [0]*N
#count number of OFF (0) in each row
for i in range(N):
    numzeros=0
    for j in range(N):
        if t[i][j] == 0:
            numzeros += 1
    rownumzeros[i] = numzeros
#count number of OFF (0) in each column
for i in range(N):
    numzeros=0
    for j in range(N):
        if t[j][i] == 0:
            numzeros += 1
    colnumzeros[i] = numzeros
print("rownumzeros", rownumzeros, "colnumzeros", colnumzeros)

#to flip a single zero cell without impacting any other cell (only when NxN is an even by even grid), we can flip that zero cell and all other cells in that row and column (at opportune moments).
flipsneeded = [[0]*N for i in range(N)]
for i in range(N):
    for j in range(N):
        flips = rownumzeros[i]+colnumzeros[j]
        if t[i][j]==0:
            flips -= 1
        flipsneeded[i][j]=flips%2 #any odd number of flips of a cell is as good as just 1 flip; any even number of flips of a cell is as good as no flip
print("flipsneeded", flipsneeded)

fliptot=0 #running total of flips needed
for i in range(N):
    for j in range(N):
        if flipsneeded[i][j]==1:
            fliptot += 1
print("total flips needed", fliptot)

sol_list=[] #list to hold flipped cells in order (each cell converted into the desired (x,y) format

def flip_adhoc_zero(row,col):
    t[row][col]=1
    sol_list.append((col+1, N-row))
    for m in range(N):
        if m!=row:
            t[m][col]=(t[m][col]+1)%2
    for m in range(N):
        if m!=col:
            t[row][m]=(t[row][m]+1)%2

passes=0
prevfliptot=fliptot
#keep scanning the grid from top left to bottom right. Flip if applicable. Make multiple passes through the grid to cover as many flips needed as possible with straight scane.
while fliptot>0:
    for i in range(N):
        for j in range(N):
            if flipsneeded[i][j]==1 and t[i][j]==0:
                flip_adhoc_zero(i,j)
                flipsneeded[i][j]=0
                fliptot -= 1
    passes += 1
    print(passes,fliptot)
    if prevfliptot == fliptot: #scans have stopped giving any net change in grid
        break
    else:
        prevfliptot=fliptot

print("modified grid", t, "Flips still needed", flipsneeded, "Number of flips still needed", fliptot)

'''
#added manually after reviewing above results. Satisfy the remaining flips needed without impacting other parities.
#manual additions for main puzzle
flip_adhoc_zero(4,0)
flip_adhoc_zero(3,0)
flip_adhoc_zero(4,0)
flip_adhoc_zero(23,0)

flip_adhoc_zero(13,1)
flip_adhoc_zero(14,1)
flip_adhoc_zero(14,20)
flip_adhoc_zero(13,1)

flip_adhoc_zero(11,6)
flip_adhoc_zero(12,6)
flip_adhoc_zero(12,7)
flip_adhoc_zero(11,6)

flip_adhoc_zero(21,4)
flip_adhoc_zero(22,4)
flip_adhoc_zero(22,12)
flip_adhoc_zero(21,4)

flip_adhoc_zero(4,8)
flip_adhoc_zero(4,9)
flip_adhoc_zero(17,9)
flip_adhoc_zero(17,11)
flip_adhoc_zero(5,11)
flip_adhoc_zero(4,8)

flip_adhoc_zero(6,13)
flip_adhoc_zero(6,14)
flip_adhoc_zero(17,14)
flip_adhoc_zero(6,13)
'''

#check if there are still any flips needed somehow
for i in range(N):
    for j in range(N):
        if flipsneeded[i][j] == 1:
            print(i,j)
'''
print("final state of grid", t)
print("solution list in desired format", sol_list)
print("number of steps in solution", len(sol_list))

#verify solution
print("checking solution")
#populate input grid into NxN array
t = [ [0]*N for i in range(N)]
cnt=0
row=0
for chr in str:
    col = cnt%N
    t[row][col] = int(chr)
    cnt += 1
    if col == N-1:
        row +=1
print("input grid", t)
#play the steps, and flag if any attempt to turn on an on bulb
for cell in sol_list:
    col = cell[0] - 1
    row = N - cell[1]
    if t[row][col] == 1:
        print("error in solution", cell)
        break
    else:
        t[row][col]=1
        for m in range(N):
            if m!=row:
                t[m][col]=((t[m][col])+1)%2
        for m in range(N):
            if m!=col:
                t[row][m]=((t[row][m])+1)%2
#check if all NxN bulbs are on
for i in range(N):
    for j in range(N):
        if t[i][j] == 0:
            print("off light found",i,j)
            break
print("done")
'''


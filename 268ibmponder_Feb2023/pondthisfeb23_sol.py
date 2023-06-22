'''
IBM Ponder This challenge main and bonus *, Feb 23
https://research.ibm.com/haifa/ponderthis/challenges/February2023.html
Sanandan Swaminathan, submitted February 11, 2023

Main puzzle (n = 20, number of ways = 48):

[(0, 10), (1, 0), (2, 2), (3, 4), (4, 1), (5, 11), (6, 8), (7, 14), (8, 19), (9, 17), (10, 15), (11, 9), (12, 3), (13, 16), (14, 18), 
(15, 7), (16, 12), (17, 6), (18, 13), (19, 5)]

Bonus "*" puzzle (n = 26, number of ways = 0):

[(0, 13), (1, 0), (2, 2), (3, 4), (4, 1), (5, 3), (6, 8), (7, 10), (8, 15), (9, 17), (10, 19), (11, 22), (12, 24), (13, 18), (14, 20), 
(15, 25), (16, 9), (17, 11), (18, 6), (19, 23), (20, 12), (21, 16), (22, 5), (23, 7), (24, 14), (25, 21)]

I wrote a python program. It ran for about 5 minutes to solve the main puzzle, and then I changed it for the bonus "*" puzzle for 
which the program ran in only 15 seconds. First, it generates n-queen solutions fast. For this I used bitwise operators. I used 
symmetry in one direction to halve the solution space, but even without the symmetry the n-queen generation was very quick. For each 
n-queen solution generated, it then generates the safe squares list. I have a fixed set of bitmasks for each of the left and right 
diagonals of an n x n board (where all the cells of each left diagonal have a distinct coordinate sum, and the same idea for right 
diagonals). By using the diagonal bitmasks of the n queens, I generate an ordered list of safe squares. For the main puzzle, I used 
backtracking to find the number of ways (upto 48) to place the 20 kings. If exactly 48 ways are found, we get the 20-queens answer for 
the main puzzle.
 
For the bonus "*" question (I used n = 26), I reduce the safe square list and the number of kings remaining to be placed. If a safe 
square is connected to zero or exactly one safe square, then a king can be put in that safe square, and the safe square can be removed 
from the picture. If it's connected to exactly one safe square, then that other safe square can also be removed. After this pruning, I 
use my backtracking function to look for one way to place the remaining kings in the remaining safe squares. If a first way to place 
the kings cannot be found, we get the 26-queens answer for the bonus "*" question.

'''

import math
import copy
from datetime import datetime

N=26 #20 for main puzzle
NUMKINGS = 26 #20 for main puzzle
TCOMBS = 0 #48 for main puzzle
BONUSFLAG = True #False for main puzzle
queenslist = []
queensolfound = pow(2,N) - 1
firstrowexcl = pow(2,N//2) - 1
queensolcnt=0
kingcombs=0
binstrallones = pow(2,N**2) - 1

#create bitmasks for every left and right diagonal to extract ordered list of safe cells based on the diagonals covered by the N queens
#every left diagonal has an associated constant based on (x,y) coords, and same with right diags
queenld = [0]*((2*N) - 1)
queenld[0] = pow(2, N*(N-1))
queenld[(2*N) - 2] = pow(2, N-1)
for startcellx in range(N-1):
    diagconst = startcellx + N - 1
    diagval = 0
    for cellval in range(startcellx, startcellx + (N+1)*(N-1-startcellx) + 1, N+1):
        diagval += pow(2,cellval)
    queenld[diagconst] = diagval

for startcelly in range(1,N-1,1):
    diagconst = N-1 - startcelly
    diagval = 0
    cellstart = N*startcelly
    for cellval in range(cellstart, cellstart + (N+1)*(N-1-startcelly) + 1, N+1):
        diagval += pow(2,cellval)
    queenld[diagconst] = diagval

queenrd = [0]*(2*N - 1)
queenrd[0] = pow(2, 0)
queenrd[(2*N) - 2] = pow(2, (N**2)-1)
for startcellx in range(1,N,1):
    diagconst = startcellx
    diagval = 0
    for cellval in range(startcellx, startcellx + (N-1)*(startcellx) + 1, N-1):
        diagval += pow(2,cellval)
    queenrd[diagconst] = diagval

for startcelly in range(1,N-1,1):
    diagconst = N-1 + startcelly
    diagval = 0
    cellstart = N*(startcelly+1) - 1
    for cellval in range(cellstart, cellstart + (N-1)*(N-1-startcelly) + 1, N-1):
        diagval += pow(2,cellval)
    queenrd[diagconst] = diagval

#ordered safe list allows us to only search through safe cells for solution (ignoring queen and non-safe cells
def make_safelist(queenlist,slist,covcells,bonus):
    elimpos = 0
    #do bitwise OR of all diags covered by N queens since safe cells are those that cannot have diagonal queen attack,
    #then flip to get ordered list of safe cells
    for queen in queenlist:
        elimpos |= queenld[queen[1]+N-1-queen[0]] | queenrd[queen[0]+queen[1]]
    safecells = ~(elimpos) & binstrallones # not needed in python, but no harm: & done with bit string of N 1's to capture all N bits even with leading 0's
    cntones = bin(safecells).count('1')

    # in main puzzle, we need 48 ways to place 20 kings, so we need at least 22 safe cells
    # in bonus puzzle, not having enough safe cells is good (False for bonus will be handled as success by caller)
    if bonus == False:
        if cntones < NUMKINGS + 2:
            return False
    else:
        if cntones < NUMKINGS:
            return False

    # queens list is NxN grid with origin at bottom right.
    # But coverage matrix is (N+2)x(N+2) including margin cells to allow carefree array ops, and array rownum is top to bottom, 
    # colnum is left to right.
    # Hence put safe cells at correct places in coverage matrix. Queens grid is not relevant for kings search. Non safe cells also 
    # not relevant.
    while safecells != 0:
        safebit = safecells & -safecells #bin string and 2's complement gives the rightmost set cell
        num = int(math.log2(safebit))
        saferownum = N - (num//N)
        safecolnum = N - (num%N)
        slist.append((saferownum, safecolnum))
        covcells[saferownum][safecolnum] = 1
        safecells = safecells^safebit #this safe cell has been processed into the coverage matrix, so discrad that bit and proceed extracting safe cells to the left
    return True

def build_neighbors(nlist, nlist2, slist, covcells, bonus):
    for safecell in slist:
        neighborlist = []
        temprownum = safecell[0]
        tempcolnum = safecell[1] - 1 #look at cell to west of this safe cell to see if it's also a safe cell which mean's it's a connected cell
        if covcells[temprownum][tempcolnum] == 1:
            neighborlist.append((temprownum,tempcolnum))
        temprownum -= 1 #look at northwest cell
        if covcells[temprownum][tempcolnum] == 1:
            neighborlist.append((temprownum,tempcolnum))
        for i in range(2): #look at north and northeast cells
            tempcolnum += 1
            if covcells[temprownum][tempcolnum] == 1:
                neighborlist.append((temprownum,tempcolnum))
        nlist.append(neighborlist)

        #for main puzzle, we only care about safe neighbors that are ahead of this safe cell since we will do king search backtracking 
        #in order.
        #for extra credit puzzle, we can prune the safe list by placing king on any safe cell with 0 or 1 neighbor safe cell, but we 
        #need to look all
        #around this safe cell for neighbors before we can decide if this safe cell has degree 1
        if bonus == True:
            neighborlist = []
            for i in range(2): #look east and southeast
                temprownum += 1
                if covcells[temprownum][tempcolnum] == 1:
                    neighborlist.append((temprownum,tempcolnum))
            for i in range(2): #look south and southwest
                tempcolnum -= 1
                if covcells[temprownum][tempcolnum] == 1:
                    neighborlist.append((temprownum,tempcolnum))
            nlist2.append(neighborlist)

#used for bonus puzzle. We can prune the safe list and remaining kings by placing king on any safe cell with 0 or 1 neighbor safe cell,
#but we need to look all
#around this safe cell for neighbors before we can decide if this safe cell has degree 1. We could also extend this to get the Maximum 
#Independent Set (MIS)
#which would tell us if max kings is less than N, but just pruning the safe list and reducing the number of kings to be placed by 
#backtracking is enough to solve the bonus in a performant manner.
def count_simple_kings(nlist, nlist2, slist, covcells, slistlen):
    kingcnt = 0
    delsafe = []
    for i in range(slistlen):
        saferownum = slist[i][0]
        safecolnum = slist[i][1]
        #the single safe neighbor of a degree 1 safe cell or the safe cell itself (where a king is placed). These cells can be removed from safe list.
        if covcells[saferownum][safecolnum] == 2:
            delsafe.append(i)
        #check all around this safe cell to see if it happens to be connected to 0 or 1 safe neighbor. If so,
        elif covcells[saferownum][safecolnum] == 1:
            ncnt = 0
            nrownum = saferownum
            ncolnum = safecolnum
            for n in nlist[i]:
                if covcells[n[0]][n[1]] == 1:
                    ncnt += 1
                    if ncnt > 1:
                        break
                    nrownum = n[0]
                    ncolnum = n[1]
            if ncnt > 1: #this safe cell is not degree 0 or 1
                continue
            for n in nlist2[i]:
                if covcells[n[0]][n[1]] == 1:
                    ncnt += 1
                    if ncnt > 1:
                        break
                    nrownum = n[0]
                    ncolnum = n[1]
            if ncnt < 2:
                kingcnt += 1
                if kingcnt >= NUMKINGS: #already found more kings than needed, so we can move to next N-queen config for our search
                    return kingcnt
                delsafe.append(i)
                covcells[saferownum][safecolnum] = 2 #not needed as this king cell will be deleted below
                if ncnt > 0:
                    covcells[nrownum][ncolnum] = 2 #this will be safe neighbor ahead that will get picked up for delete later in the loop
    #prune the safe list
    cnt = 0
    for i in delsafe:
        x=i-cnt
        slist.pop(x)
        nlist.pop(x)
        cnt += 1
    return kingcnt

#backtracking search through ordered safe list to place remaining kings
def recur_kingsearch(kingsrem,covcells,safestartidx,safelistlen,safearr,nlist,tgtcombs):
    global kingcombs
    for i in range(safestartidx,safelistlen-kingsrem+1,1):
        if covcells[safearr[i][0]][safearr[i][1]] == 1:
            if kingsrem == 1:
                kingcombs += 1
                if kingcombs > tgtcombs:
                    return False
                continue
            updatetracker = [] #to reset only specific cells that get updated to 2 (blocked) in this function instance
            for neighbor in nlist[i]:
                neighborrow = neighbor[0]
                neighborcol = neighbor[1]
                if covcells[neighborrow][neighborcol] == 1:
                    covcells[neighborrow][neighborcol] = 2
                    updatetracker.append(1)
                else:
                    updatetracker.append(0)
            if recur_kingsearch(kingsrem-1,covcells,i+1,safelistlen,safearr,nlist,tgtcombs) == False:
                return False
            for j in range(len(updatetracker)):
                if updatetracker[j] == 1:
                    covcells[nlist[i][j][0]][nlist[i][j][1]] = 1
    return True

#find N-queen solution; for each solution, create ordered safe list and look for desired king solution
def queenrecurse(leftdiag, rightdiag, col, excludes, qlist, currrow, targetcombs, bonus):
    global kingcombs
    if col == queensolfound:
        global queensolcnt
        queensolcnt += 1
        if queensolcnt%10000000 == 0:
            print(queensolcnt, datetime.now())
        safelist = []
        covmatrix = [[0]*(N+2) for _ in range(N+2)] # including margin cells to allow carefree array ops
        if make_safelist(qlist, safelist, covmatrix, bonus) == False: #fewer than needed safe cells
            if bonus == True:
                print(qlist)
                return True
            else:
                return False

        slistlen = len(safelist)

        #build list of left or top neighbor lists for the cells in safelist since kings will be filled in order
        neighborlist = []
        neighborlist2 = []
        build_neighbors(neighborlist, neighborlist2, safelist, covmatrix, bonus)
        remkings = NUMKINGS
        if bonus == True: #count degree 1 cells and also prune safe list
            kcnt = count_simple_kings(neighborlist, neighborlist2, safelist, covmatrix, slistlen)
            slistlen = len(safelist)
            remkings -= kcnt
            if slistlen < remkings:
                print(qlist)
                return True
           
        #for main puzzle, there are all NUMKINGS to be placed.
        #For bonus puzzle, there may be fewer to place but proceed to next N-queen config if NUMKINGS already placed.
        if remkings > 0:
            kingcombs = 0
            if recur_kingsearch(remkings,covmatrix,0,slistlen,safelist,neighborlist,targetcombs) == False:
                return False
            if kingcombs < targetcombs: #can happen in main puzzle
                return False
            else: #target number of king placement ways found
                print(qlist)
                return True

    #start n-queens search from bottom row of grid. Use excludes bitmask to exclude half of row 0 (to take advantage of at least one 
    #symmetry)
    #left diag, right diag and col bitmasks start as 0's
    posscells = ~(leftdiag | rightdiag | col | excludes) & queensolfound #possible locations to place initial queen in row0
    while posscells != 0:
        queenbit = posscells & -posscells #bin string and 2's complement gives the rightmost set cell where queen can be placed
        colnum = int(math.log2(queenbit)) #convert into actual location
        qlisttemp = qlist.copy()
        qlisttemp.append((currrow,colnum))
        posscells = posscells^queenbit #to move to next possible queen location option

        #with a queen placed in a row, recurse to place queen in next row.
        #Update the N-bit masks for diags with queen having been placed, and shift the diag masks to become valid for next row.
        #Update N-bit column mask also as this queen has occupied a column.
        if queenrecurse((leftdiag|queenbit)>>1, (rightdiag|queenbit)<<1, col|queenbit, 0, qlisttemp, currrow+1, targetcombs, bonus) == True:
            return True
    return False

print(datetime.now())
print(N,NUMKINGS,TCOMBS,BONUSFLAG)
ret = queenrecurse(0, 0, 0, firstrowexcl, queenslist, 0, TCOMBS, BONUSFLAG)
print (ret)
print("queen sol #", queensolcnt)
print(datetime.now())


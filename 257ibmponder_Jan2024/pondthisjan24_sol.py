'''
My IBM Ponder This January '24 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/January2024.html
Sanandan Swaminathan, submitted December 31, 2023

For main challenge, the program tries permutations of 4 of the 16 numbers in the top row. If the top row
is satisfied, it tries permutations of 4 of the remaining 12 numbers in next row, and so on. If an equation
is not satisfied at any point, it tries another perm. If the 4th row is satisfied, it checks the 4 column
equations. This loop ran for a couple of minutes, and found 84 solutions.

For the bonus *, it looks for deranged pairs among the solutions. For any deranged pair, it recursively
tries sign changes. At any point, if an equation is not satisfied for both solutions in the pair, it
backtracks. If the number of sign cells remaining to be tried is less than the number of sign changes still
needed, it backtracks. Once a working pair of deranged solutions is found, the sign changes are captured
while going back up the tree. The bonus * portion completed instantaneously. It turns out that there are
3 different deranged solution pairs that allow exactly 12 sign changes while still giving the same grid
results for both solutions (grid resuts different from the original grid results). No deranged solution
pair allows more than 12 sign changes. One of the pairs allows 4 different ways to make the 12 sign changes.
'''

from datetime import datetime
from itertools import permutations

numset = {_ for _ in range(1,17)} #set of nums 1-16
solutions = [] #to hold list of 16-num lists that satisfy the original board
progress = 0 #program progress meter
print("Starting", datetime.now())

#for main puzzle, try perms in each row that satisfy relevant equations
for row0 in permutations(numset, 4): #perms of 4 of 16 nums for top row
    progress += 1
    if progress%10000 == 0:
        print(datetime.now(), progress)
    if row0[0]+row0[1]-row0[2]-row0[3]==5: #if top row's equation is satisfied
        #get 12 remaining nums for the given 4-num perm of the top row
        numset1 = numset - set(row0)
        for row1 in permutations(numset1, 4): #perms of 4 of 12 remaining nums
            if row1[0]+row1[1]+row1[2]-row1[3]==10: #if 2nd row's equation satisfied
                numset2 = numset1 - set(row1) #get 8 remaining nums
                for row2 in permutations(numset2, 4): #perms of 4 of 8 remaining nums
                    if row2[0]-row2[1]+row2[2]+row2[3]==9: #if 3rd row's equation satisfied
                        numset3 = numset2 - set(row2) #get 4 remaining nums
                        for row3 in permutations(numset3): #perms for bottom row
                            #check bottom row's equation and all 4 column equations
                            if (row3[0]-row3[1]+row3[2]-row3[3]==0) and \
                               (row0[0]+row1[0]+row2[0]-row3[0]==17) and \
                               (row0[1]+row1[1]-row2[1]-row3[1]==8) and \
                               (row0[2]-row1[2]-row2[2]+row3[2]==11) and \
                               (row0[3]+row1[3]+row2[3]+row3[3]==48):
                                #one solution found, capture this 16-num solution
                                templist = []
                                for num in row0:
                                    templist.append(num)
                                for num in row1:
                                    templist.append(num)
                                for num in row2:
                                    templist.append(num)
                                for num in row3:
                                    templist.append(num)
                                solutions.append(templist)
                 
print("Main answer: A solution", solutions[0])
print("Main answer: Number of solutions:", len(solutions))
print("Main done", progress)
print("Starting bonus *", datetime.now())

#sign 0 for +, 1 for -
row_signs = [[0,1,1],[0,0,1],[1,0,0],[1,0,1]]
col_signs = [[0,0,1,0],[0,1,1,0],[1,1,0,0]]

#recursive function called first when the 4 rows have processed
def process_col(deranged_pair, col_num, num_cells_left, num_chg_left, row_sign_changes, col_sign_changes):
    if num_chg_left <= 0:
        return True
    if num_cells_left < num_chg_left:
        return False
    # operate on the top two numbers in the column, for both deranged solutions
    for i in (0,1): # 1 means flip the sign, 0 means don't
        chg0 = res01 = res02 = 0
        if i==0:
            if col_signs[0][col_num] == 0: #if original sign was +
                res01 = deranged_pair[0][col_num] + deranged_pair[0][col_num+4]
                res02 = deranged_pair[1][col_num] + deranged_pair[1][col_num+4]
            else:
                res01 = deranged_pair[0][col_num] - deranged_pair[0][col_num+4]
                res02 = deranged_pair[1][col_num] - deranged_pair[1][col_num+4]
        else:
            if col_signs[0][col_num] == 0:
                res01 = deranged_pair[0][col_num] - deranged_pair[0][col_num+4]
                res02 = deranged_pair[1][col_num] - deranged_pair[1][col_num+4]
            else:
                res01 = deranged_pair[0][col_num] + deranged_pair[0][col_num+4]
                res02 = deranged_pair[1][col_num] + deranged_pair[1][col_num+4]
            chg0 += 1
        # operate on the result of the top two nums in the column and the 3rd num
        for j in (0,1):
            chg1 = chg0
            res11=res01
            res12=res02
            if j==0:
                if col_signs[1][col_num] == 0:
                    res11 += deranged_pair[0][col_num+8]
                    res12 += deranged_pair[1][col_num+8]
                else:
                    res11 -= deranged_pair[0][col_num+8]
                    res12 -= deranged_pair[1][col_num+8]
            else:
                if col_signs[1][col_num] == 0:
                    res11 -= deranged_pair[0][col_num+8]
                    res12 -= deranged_pair[1][col_num+8]
                else:
                    res11 += deranged_pair[0][col_num+8]
                    res12 += deranged_pair[1][col_num+8]
                chg1 += 1
            # operate on result of the top 3 nums and the bottom num in the column
            for k in (0,1):
                chg2 = chg1
                res21=res11
                res22=res12
                if k==0:
                    if col_signs[2][col_num] == 0:
                        res21 += deranged_pair[0][col_num+12]
                        res22 += deranged_pair[1][col_num+12]
                    else:
                        res21 -= deranged_pair[0][col_num+12]
                        res22 -= deranged_pair[1][col_num+12]
                else:
                    if col_signs[2][col_num] == 0:
                        res21 -= deranged_pair[0][col_num+12]
                        res22 -= deranged_pair[1][col_num+12]
                    else:
                        res21 += deranged_pair[0][col_num+12]
                        res22 += deranged_pair[1][col_num+12]
                    chg2 += 1
                if res21 == res22: # if the column result is the same for both solutions
                    #recurse to next column: there are 3 less unprocessed + - cells remaining.
                    #Min number of + - cells still to be changed has reduced by changes in this col
                    if process_col(deranged_pair, col_num+1, num_cells_left-3, num_chg_left-chg2, \
                                   row_sign_changes, col_sign_changes) == True:
                        #solution found, capture the state of + - cells in this column and return
                        col_sign_changes[0][col_num] = i
                        col_sign_changes[1][col_num] = j
                        col_sign_changes[2][col_num] = k
                        return True
    return False

#recursive function for processing of rows
def process_row(deranged_pair, row_num, num_chg_left, row_sign_changes, col_sign_changes):
    if row_num == 4: #all 4 rows processed, proceed to process columns
        return process_col(deranged_pair, 0, 12, num_chg_left, row_sign_changes, col_sign_changes)
    
    offset = row_num*4
    # operate on the leftmost two numbers in the row, for both deranged solutions
    for i in (0,1): # 1 means flip the sign, 0 means don't
        chg0 = res01 = res02 = 0
        if i==0:
            if row_signs[row_num][0] == 0: #if original sign was +
                res01 = deranged_pair[0][offset] + deranged_pair[0][offset+1]
                res02 = deranged_pair[1][offset] + deranged_pair[1][offset+1]
            else:
                res01 = deranged_pair[0][offset] - deranged_pair[0][offset+1]
                res02 = deranged_pair[1][offset] - deranged_pair[1][offset+1]
        else:
            if row_signs[row_num][0] == 0:
                res01 = deranged_pair[0][offset] - deranged_pair[0][offset+1]
                res02 = deranged_pair[1][offset] - deranged_pair[1][offset+1]
            else:
                res01 = deranged_pair[0][offset] + deranged_pair[0][offset+1]
                res02 = deranged_pair[1][offset] + deranged_pair[1][offset+1]
            chg0 += 1
        # operate on the result of the leftmost two nums in the row and the 3rd num
        for j in (0,1):
            chg1 = chg0
            res11=res01
            res12=res02
            if j==0:
                if row_signs[row_num][1] == 0:
                    res11 += deranged_pair[0][offset+2]
                    res12 += deranged_pair[1][offset+2]
                else:
                    res11 -= deranged_pair[0][offset+2]
                    res12 -= deranged_pair[1][offset+2]
            else:
                if row_signs[row_num][1] == 0:
                    res11 -= deranged_pair[0][offset+2]
                    res12 -= deranged_pair[1][offset+2]
                else:
                    res11 += deranged_pair[0][offset+2]
                    res12 += deranged_pair[1][offset+2]
                chg1 += 1
            # operate on the result of the leftmost 3 nums and the rightmost num in the row
            for k in (0,1):
                chg2 = chg1
                res21=res11
                res22=res12
                if k==0:
                    if row_signs[row_num][2] == 0:
                        res21 += deranged_pair[0][offset+3]
                        res22 += deranged_pair[1][offset+3]
                    else:
                        res21 -= deranged_pair[0][offset+3]
                        res22 -= deranged_pair[1][offset+3]
                else:
                    if row_signs[row_num][2] == 0:
                        res21 -= deranged_pair[0][offset+3]
                        res22 -= deranged_pair[1][offset+3]
                    else:
                        res21 += deranged_pair[0][offset+3]
                        res22 += deranged_pair[1][offset+3]
                    chg2 += 1
                if res21 == res22: # if the row result is the same for both solutions
                    #Recurse to next row: min number of + - cells still to be changed
                    #has reduced due to changes in this row.
                    if process_row(deranged_pair, row_num+1, num_chg_left-chg2, \
                                   row_sign_changes, col_sign_changes) == True:
                        #solution found, capture the state of + - cells in this row and return
                        row_sign_changes[row_num][0] = i
                        row_sign_changes[row_num][1] = j
                        row_sign_changes[row_num][2] = k
                        return True
    return False

#convert the + - changes to desired list format
def convert_bonus_result_to_signs(row_sign_changes,col_sign_changes):
    change_list = [] #to hold list of 24 + - signs reflecting the modified board
    #grid has 7 rows, alternating between row equations and column signs
    for i in range(7):
        row = i//2
        if i%2 == 0: #an equation row
            for col in range(3):
                if row_sign_changes[row][col] == 0: # 0 -> sign not flipped, 1 -> flipped
                    if row_signs[row][col] == 0: #0 -> sign was +, 1 -> sign was -
                        change_list.append('+')
                    else:
                        change_list.append('-')
                else:
                    if row_signs[row][col] == 0:
                        change_list.append('-')
                    else:
                        change_list.append('+')
        else: #columnar equation
            for col in range(4):
                if col_sign_changes[row][col] == 0:
                    if col_signs[row][col] == 0:
                        change_list.append('+')
                    else:
                        change_list.append('-')
                else:
                    if col_signs[row][col] == 0:
                        change_list.append('-')
                    else:
                        change_list.append('+')
    return change_list

row_sign_changes = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]] #to capture changes in row signs
col_sign_changes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]] #to capture changes in column signs
solfound = False
#look for deranged pairs among solutions, i.e. no cell has the same number in both solutions
for i in range(len(solutions)-1):
    for j in range(i+1,len(solutions)):
        deranged = True
        for k in range(16):
            if solutions[i][k] == solutions[j][k]: #cell match, the 2 solutions are not deranged
                deranged=False
                break
        if deranged == True:
            #call recursive routine to see if the deranged pair still works after at least 12 + - changes
            if process_row((solutions[i], solutions[j]), 0, 12, row_sign_changes, col_sign_changes) == True:
                print("One answer for bonus *:", (solutions[i], solutions[j]))
                #convert + - cells to desired list format
                print("Bonus * new signs list:", \
                      f"[{','.join(convert_bonus_result_to_signs(row_sign_changes,col_sign_changes))}]")
                #comment out the next 2 lines if interested in all deranged pairs that work
                #(there are 3 such deranged pairs, but only 1 is asked for)
                #([8, 13, 5, 11, 10, 14, 1, 15, 3, 12, 2, 16, 4, 7, 9, 6], [12, 8, 9, 6, 14, 10, 2, 16, 4, 7, 1, 11, 13, 3, 5, 15])
                #([13, 12, 6, 14, 5, 9, 4, 8, 1, 10, 7, 11, 2, 3, 16, 15], [14, 8, 2, 15, 4, 16, 1, 11, 5, 9, 3, 10, 6, 7, 13, 12])
                #([15, 10, 8, 12, 13, 7, 1, 11, 3, 5, 2, 9, 14, 4, 6, 16], [16, 12, 9, 14, 10, 6, 2, 8, 4, 7, 1, 11, 13, 3, 5, 15])
                #Btw, by tweaking the process_col function, not returning True as soon as at least 12 sign
                #changes work for some deranged pair, and instead printing the pair in that function when
                #column beyond last column is reached, we can find the max number of sign changes the pair
                #will allow. It turns out that all 3 deranged pairs given above allow exactly 12 sign changes,
                #no more. For each of the first two deranged pairs, there is one way to make 12 sign changes.
                #For the last deranged pair, there are 4 different ways to make 12 sign changes.
                #In total, we can say that there are 6 possible solutions for the bonus *.
                solfound = True
                break
    if solfound==True:
        break
print("Bonus * done", datetime.now())

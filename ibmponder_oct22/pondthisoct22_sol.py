'''
IBM Ponder This challenge and bonus *, Oct 22
https://research.ibm.com/haifa/ponderthis/challenges/October2022.html
Sanandan Swaminathan, submitted October 10, 2022

Main puzzle (n = 6):

1 2 3 4 5 6
2 3 1 6 4 5
5 4 6 1 3 2
4 1 2 5 6 3
6 5 4 3 2 1
3 6 5 2 1 4
2 3 1 6 4 5
3 6 5 2 1 4
4 1 2 5 6 3
1 2 3 4 5 6
5 4 6 1 3 2
6 5 4 3 2 1
3 6 5 2 1 4
1 2 3 4 5 6
6 5 4 3 2 1
2 3 1 6 4 5
4 1 2 5 6 3
5 4 6 1 3 2
4 1 2 5 6 3
6 5 4 3 2 1
1 2 3 4 5 6
5 4 6 1 3 2
3 6 5 2 1 4
2 3 1 6 4 5
5 4 6 1 3 2
4 1 2 5 6 3
3 6 5 2 1 4
6 5 4 3 2 1
2 3 1 6 4 5
1 2 3 4 5 6
6 5 4 3 2 1
5 4 6 1 3 2
2 3 1 6 4 5
3 6 5 2 1 4
1 2 3 4 5 6
4 1 2 5 6 3
124

Bonus "*" puzzle (n = 5):

1 2 3 4 5
3 4 5 1 2
5 1 2 3 4
2 3 4 5 1
4 5 1 2 3
1 2 3 4 5
3 4 5 1 2
5 1 2 3 4
2 3 4 5 1
4 5 1 2 3
1 2 3 4 5
3 4 5 1 2
5 1 2 3 4
2 3 4 5 1
4 5 1 2 3
1 2 3 4 5
3 4 5 1 2
5 1 2 3 4
2 3 4 5 1
4 5 1 2 3
1 2 3 4 5
3 4 5 1 2
5 1 2 3 4
2 3 4 5 1
4 5 1 2 3
84

'''

from copy import copy, deepcopy
from itertools import permutations
from datetime import datetime

def score_ls_cube(arr):
    score=0
    diagscore=0
    checkarr=[-1]*N
    for layer in range(0,N):
        for rownum in range(0,N):
            checkarr=[-1]*N
            incscore = True
            for colnum in range(0,N):
                if checkarr[arr[rownum][colnum][layer]] != -1:
                    incscore = False
                    break
                else:
                    checkarr[arr[rownum][colnum][layer]] = 1
            if incscore == True:
                score += 1
   
        for colnum in range(0,N):
            checkarr=[-1]*N
            incscore = True
            for rownum in range(0,N):
                if checkarr[arr[rownum][colnum][layer]] != -1:
                    incscore = False
                    break
                else:
                    checkarr[arr[rownum][colnum][layer]] = 1
            if incscore == True:
                score += 1
   
        checkarr=checkarr=[-1]*N
        incscore = True
        for leftdiag in range(0,N):
            if checkarr[arr[leftdiag][leftdiag][layer]] != -1:
                incscore = False
                break
            else:
                checkarr[arr[leftdiag][leftdiag][layer]] = 1
        if incscore == True:
            score += 1
            diagscore += 1
   
        checkarr=[-1]*N
        incscore = True
        for rightdiag in range(0,N):
            if checkarr[arr[N-1-rightdiag][rightdiag][layer]] != -1:
                incscore = False
                break
            else:
                checkarr[arr[N-1-rightdiag][rightdiag][layer]] = 1
        if incscore == True:
            score += 1
            diagscore += 1
     
    for colnum in range(0,N):
        for rownum in range(0,N):
            checkarr=[-1]*N
            incscore = True
            for layer in range(0,N):
                if checkarr[arr[rownum][colnum][layer]] != -1:
                    incscore = False
                    break
                else:
                    checkarr[arr[rownum][colnum][layer]] = 1
            if incscore == True:
                score += 1
   
        checkarr=[-1]*N
        incscore = True
        for leftdiag in range(0,N):
            if checkarr[arr[leftdiag][colnum][N-1-leftdiag]] != -1:
                incscore = False
                break
            else:
                checkarr[arr[leftdiag][colnum][N-1-leftdiag]] = 1
        if incscore == True:
            score += 1
            diagscore += 1
   
        checkarr=[-1]*N
        incscore = True
        for rightdiag in range(0,N):
            if checkarr[arr[N-1-rightdiag][colnum][rightdiag]] != -1:
                incscore = False
                break
            else:
                checkarr[arr[N-1-rightdiag][colnum][rightdiag]] = 1
        if incscore == True:
            score += 1
            diagscore += 1
       
    for rownum in range(0,N):
        checkarr=[-1]*N
        incscore = True
        for leftdiag in range(0,N):
            if checkarr[arr[rownum][leftdiag][N-1-leftdiag]] != -1:
                incscore = False
                break
            else:
                checkarr[arr[rownum][leftdiag][N-1-leftdiag]] = 1
        if incscore == True:
            score += 1
            diagscore += 1
   
        checkarr=[-1]*N
        incscore = True
        for rightdiag in range(0,N):
            if checkarr[arr[rownum][rightdiag][rightdiag]] != -1:
                incscore = False
                break
            else:
                checkarr[arr[rownum][rightdiag][rightdiag]] = 1
        if incscore == True:
            score += 1
            diagscore += 1

    checkarr=[-1]*N
    incscore = True
    for superdiag in range(0,N):
        if checkarr[arr[superdiag][superdiag][superdiag]] != -1:
            incscore = False
            break
        else:
            checkarr[arr[superdiag][superdiag][superdiag]] = 1
    if incscore == True:
        score += 1
        diagscore += 1
    checkarr=[-1]*N
    incscore = True
    for superdiag in range(0,N):
        if checkarr[arr[superdiag][N-1-superdiag][superdiag]] != -1:
            incscore = False
            break
        else:
            checkarr[arr[superdiag][N-1-superdiag][superdiag]] = 1
    if incscore == True:
        score += 1
        diagscore += 1
    checkarr=[-1]*N
    incscore = True
    for superdiag in range(0,N):
        if checkarr[arr[superdiag][superdiag][N-1-superdiag]] != -1:
            incscore = False
            break
        else:
            checkarr[arr[superdiag][superdiag][N-1-superdiag]] = 1
    if incscore == True:
        score += 1
        diagscore += 1
    checkarr=[-1]*N
    incscore = True
    for superdiag in range(0,N):
        if checkarr[arr[superdiag][N-1-superdiag][N-1-superdiag]] != -1:
            incscore = False
            break
        else:
            checkarr[arr[superdiag][N-1-superdiag][N-1-superdiag]] = 1
    if incscore == True:
        score += 1
        diagscore += 1
    return(diagscore,score)

def recur_ls_build(latinsqr,ls_rows,ls_cols,ls_maindiag, ls_antidiag,nextpos):
    global totcnt
    if nextpos==N*N:
        all_latinsqrs_list.append(deepcopy(latinsqr))
        totcnt += 1
        return
   
    tmp_latinsqr = deepcopy(latinsqr)
    tmp_ls_rows = deepcopy(ls_rows)
    tmp_ls_cols = deepcopy(ls_cols)
    tmp_ls_maindiag = deepcopy(ls_maindiag)
    tmp_ls_antidiag = deepcopy(ls_antidiag)
    rownum=int(nextpos/N)
    colnum=nextpos%N

    for trydig in range(0,N):
        if tmp_ls_rows[rownum][trydig]==-1 and tmp_ls_cols[colnum][trydig]==-1 \
        and (rownum!=colnum or (rownum==colnum and tmp_ls_maindiag[trydig]==-1)) \
        and (rownum!=N-1-colnum or (rownum==N-1-colnum and tmp_ls_antidiag[trydig]==-1)):
                    tmp_ls_rows[rownum][trydig]=1
                    tmp_ls_cols[colnum][trydig]=1
                    if rownum==colnum:
                        tmp_ls_maindiag[trydig]=1
                    if rownum==N-1-colnum:
                        tmp_ls_antidiag[trydig]=1
                    tmp_latinsqr[rownum][colnum]=trydig
                    recur_ls_build(tmp_latinsqr,tmp_ls_rows,tmp_ls_cols,tmp_ls_maindiag, tmp_ls_antidiag,nextpos+1)
                    tmp_ls_rows[rownum][trydig]=-1
                    tmp_ls_cols[colnum][trydig]=-1
                    if rownum==colnum:
                        tmp_ls_maindiag[trydig]=-1
                    if rownum==N-1-colnum:
                        tmp_ls_antidiag[trydig]=-1
                    tmp_latinsqr[rownum][colnum]=-1

def recur_lscube_build(latincube,row_start_dig_pos,layer):
    global best_diagscore, best_diag_totscore, best_diag_lscube, best_score, best_lscube, trx_ctr
    if layer==N:
        daigscore,score = score_ls_cube(latincube)
        if diagscore>best_diagscore:
            best_diagscore=diagscore
            best_diag_totscore=score
            best_diag_lscube=deepcopy(latincube)
        if diagscore==best_diagscore and score>best_diag_totscore:
            best_diag_totscore=score
            best_diag_lscube=deepcopy(latincube)
        if score>best_score:
            best_score=score
            best_lscube=deepcopy(latincube)
        trx_ctr += 1
        if trx_ctr%1000000 == 0:
            print(datetime.now().time(), trx_ctr/1000000)
            print(best_score, best_diagscore, best_diag_totscore)
        return

    digits = [-1]*N
    for i in range(0,N):
        digits[i]=i
    perm = permutations(digits)
    for i in list(perm):
        row=0
        for j in i:
            for col in range(0,N):
                latincube[row][col][layer]=latincube[row_start_dig_pos[j]][col][0]
            row += 1
        recur_lscube_build(latincube,row_start_dig_pos,layer+1)

print(datetime.now().time())
N=6
print("starting for N = ",N)
totcnt=0
all_latinsqrs_list = []
row_start_dig_pos = [-1]*N
ls_cube = [[[-1]*N for _ in [-1]*N] for layer in [-1]*N]
best_diag_lscube = [[[-1]*N for _ in [-1]*N] for layer in [-1]*N]
best_lscube = [[[-1]*N for _ in [-1]*N] for layer in [-1]*N]
ls_rows = [[-1]*N for _ in [-1]*N]
ls_cols = [[-1]*N for _ in [-1]*N]
ls_maindiag = [-1]*N
ls_antidiag = [-1]*N
latinsqr = [[-1]*N for _ in [-1]*N]
for i in range(0,N):
    latinsqr[0][i]=i
for i in range(0,N):
    ls_rows[0][i]=1
for i in range(0,N):
    ls_cols[i][i]=1
ls_maindiag[0]=1
ls_antidiag[N-1]=1
recur_ls_build(latinsqr,ls_rows,ls_cols,ls_maindiag,ls_antidiag,N)
print("number of diag LS: ",len(all_latinsqrs_list))
print("\n")
best_diagscore=0
best_diag_totscore=0
best_score=0
lscnt=0
for ls in all_latinsqrs_list:
    tuplecnt=0
    for ls_row in ls:
        row_start_dig_pos[ls_row[0]]=tuplecnt
        for col in range(0,N):
            ls_cube[tuplecnt][col][0] = ls_row[col]
        tuplecnt += 1

    for layer in range(1,N):
        for row in range(0,N):
            for col in range(0,N):
                ls_cube[row][col][layer]=ls[row_start_dig_pos[ls[row][layer]]][col]
    diagscore,score = score_ls_cube(ls_cube)
    print(diagscore,score)
    if diagscore>best_diagscore:
        best_diagscore=diagscore
        best_diag_totscore=score
        best_diag_lscube=deepcopy(ls_cube)
    if diagscore==best_diagscore and score>best_diag_totscore:
        best_diag_totscore=score
        best_diag_lscube=lscnt
    if score>best_score:
        best_score=score
        best_lscube=deepcopy(ls_cube)
    lscnt +=1
print("best_score=",best_score,", best_diagscore=",best_diagscore,", best_diag_totscore=",best_diag_totscore)
print("printing cube with overall best score...")
print("\n")
for layer in range(0,N):
    for row in range(0,N):
        for col in range(0,N):
            if col != N-1:
                print(best_lscube[row][col][layer]+1,end=" ")
            else:
                print(best_lscube[row][col][layer]+1)
print(best_score)
print("")
print("\nprinting cube with best diag score and then best overall score...\n")
for layer in range(0,N):
    for row in range(0,N):
        for col in range(0,N):
            if col != N-1:
                print(best_diag_lscube[row][col][layer]+1,end=" ")
            else:
                print(best_diag_lscube[row][col][layer]+1)
print(best_score)
print("")
print(datetime.now().time())
print("Done for N=",N)

'''
trx_ctr=0
best_diagscore=0
best_diag_totscore=0
best_score=0
ls_cube = deepcopy(best_lscube)
for tuplecnt in range(0,N):
    row_start_dig_pos[best_lscube[tuplecnt][0][0]] = tuplecnt

print(datetime.now().time())
recur_lscube_build(ls_cube,row_start_dig_pos,1)
print(best_score, best_diagscore, best_diag_totscore)
print("printing permuted cube with overall best score")
for layer in range(0,N):
    for row in range(0,N):
        for col in range(0,N):
            print(best_lscube[row][col][layer]+1,end=",")
        print("\n")
print("printing permuted cube with best diag score and then best overall score")
for layer in range(0,N):
    for row in range(0,N):
        for col in range(0,N):
            print(best_diag_lscube[row][col][layer]+1,end=",")
        print("\n")
'''

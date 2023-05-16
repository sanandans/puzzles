'''
IBM Ponder This challenge and bonus *, Aug 22
https://research.ibm.com/haifa/ponderthis/challenges/August2022.html
Sanandan Swaminathan, submitted August 9, 2022

2,524,614,399   (for the main puzzle, n = 2^24, number of ways mod N = 3141592653)

920,321,499     (for the bonus "*" puzzle, n = 2^256, number of ways mod N = 3141592653)

First, I drew a state diagram with the following 10 states:
1) Two dancers on stage, both having 2 units of time remaining
2) Two dancers, both having 1 unit of time remaining
3) Two dancers, both having 0 units of time remaining
4) One dancer on stage (so, has no units remaining)
5) Two dancers, the left dancer with 1 unit remaining, the other with 2 units remaining
6) Two dancers, the left dancer with 2 units remaining, the other with 1 unit remaining
7) Two dancers, the left dancer with 0 units remaining, the other with 1 unit remaining
8) Two dancers, the left dancer with 0 units remaining, the other with 2 units remaining
9) Two dancers, the left dancer with 2 units remaining, the other with 0 units remaining
10) Two dancers, the left dancer with 1 unit remaining, the other with 0 units remaining

The number of ways to transition from a state to another state can be captured in a 10x10 matrix T (shown below):
[0, 1, 0, 2, 2, 2, 0, 0, 0, 0],
[0, 0, 1, 2, 0, 0, 0, 2, 2, 0],
[0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
[6, 0, 0, 3, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 0, 2, 1, 2, 0, 0],
[0, 0, 0, 2, 2, 0, 0, 0, 2, 1],
[0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
[0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
[0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 0, 0, 0, 2, 0, 0]

When the dance starts, the initial state can only be either two dancers on stage, both having two units of time remaining (State 1 above), or a single dancer on stage (State 4 above). The puzzle is asking us to find the number of walks of length n-1 in the graph from the start states (where edges and vertices can be repeated). Once we find the number of walks with starting state as State 1 (say, dancers A and B on stage) or 4 (say, dancer A on stage), we can multiply the number of walks for State 1 by 12 (as there are 12 permutations of A,B,C,D), and the number of walks for state 4 by 4 (as the single starting dancer could be A, B, C or D).

For matrix T, the entries of T^(n-1) give the number of walks of length n-1 for each starting vertex/ending vertex pair. Summing the values in the first row of T^(n-1) gives us the total number of walks starting from State 1. We multiply this number by 12 since there are 12 permutations for the starting pair of dancers. Similarly, the sum of the values in the fourth row of T^(n-1) gives us the total number of walks starting from State 4. We multiply this by 4 since there are 4 possibilities of a single starting dancer. Of course, all calculations need to be performed mod N.
Also, T^((2^x) -1) = (T^(2^0)*(T^(2^1))*(T^(2^2)...T^(2^(x-1)).
Since n-1 = (2^x) -1 in the given puzzles, we can use matrix exponentiation for fast computation.

I wrote a short python program that completed immediately for both the main and bonus puzzles. It has a short loop that squares the previous matrix (mod N) and also multiplies the previous matrix by the squared matrix (mod N) to keep building the result matrix. For n = 2^24, only 23 loop iterations (46 matrix multiplications) are needed. For n = 2^256, only 255 iterations (510 matrix multiplications) are needed.
'''

N = 3141592653
D = 10
L = 255 # L=2 for n=2^3, L=6 for n=2^7, L=23 for n=2^24, L=255 for n=2^256
 
def multiply(a, b, res):
    mul=[[0 for x in range(D)] for y in range(D)]
    for i in range(D):
        for j in range(D):
            mul[i][j] = 0;
            for k in range(D):
                mul[i][j] += ((a[i][k] * b[k][j])%N)
    for i in range(D):
        for j in range(D):
            res[i][j] = ((mul[i][j])%N)

res = [
    [0, 1, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0, 0, 2, 2, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 1, 2, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 2, 1],
    [0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 2, 0, 0]
    ]
sqr = [
    [0, 1, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0, 0, 2, 2, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 1, 2, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 2, 1],
    [0, 0, 0, 2, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 2, 0, 0]
    ]
for i in range(L):
    multiply(sqr,sqr,sqr)
    multiply(res,sqr,res)
ctr=0
for i in range(D):
     ctr += (12*res[0][i] + 4*res[3][i])
ctr %= N
print(ctr) # prints 17342172 for n=2^3, 2484449895 for n=2^7, 2524614399 for n=2^24, 920321499 for n=2^256


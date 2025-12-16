'''
My IBM Ponder This October '25 challenge main and bonus * solutions (both complete immediately)
https://research.ibm.com/haifa/ponderthis/challenges/October2025.html
Sanandan Swaminathan, submitted September 30, 2025

Since we are dealing with finding paths through the cells of a maze, one of the first things that
jumps to mind is treating the cells as the nodes of an undirected, unweighted, simple graph. If
two orthogonally adjacent cells are connected (i.e. there is no wall between them), then we can consider
that connection as an undirected edge. Basically we are told to choose edges (from all possible edges)
such that we can get from any cell to any cell by traversing exactly one path, i.e. there is no other
path between those two cells. Of course, this is precisely what a spenning tree is. So, if there are
n x m cells in the maze, we need to choose exactly nm - 1 edges from all possible edges without causing
a cycle (in our maze, a cycle would mean there are two ways to get from one cell in the cycle to another
in the cycle).

One standard way to calculate the number of spanning trees efficiently is to use Kirchhoff's matrix tree
theorem...
https://en.wikipedia.org/wiki/Kirchhoff%27s_theorem
Of course, Kirchhoff's matrix tree theorem gives the number of spanning trees without adjusting for
possible symmetries (like with reflection or rotation). But the problem description clearly states that
we don't need to worry about rotations and reflections. This makes sense if we treat the maze as a graph
with labeled vertices - each spanning tree is distinct even if two spanning trees "look" the same by
rotation or reflection. The Kirchhoff process to calculate the number of spanning trees in a general
graph is: set up the Laplacian matrix (diagonal degree matrix minus adjacency matrix), remove any row i
and column i (same row number and column number), then calculate the determinant of the remaining matrix.
The determinant value is the number of distinct spanning trees rooted at node i (i.e. the number of
spanning trees of the graph). They are distinct spanning trees upto rotation and reflection (i.e. they
are all the spanning trees if we consider the graph as fixed with labeled vertices). My short program
below uses the Kirchhoff process for the main puzzle. I used numpy's linalg.slogdet function to calculate
the determinant. Since this function gives the natural log value of the determinant, the program converts
that result into the desired base 10 scientific notation.

In the bonus puzzle, the 342 x 357 grid is too large to use the Laplacian matrix approach directly since
we are interested in fast computation with low memory footprint. This needed an even more efficient way
than Kirchhoff's matrix tree theorem to compute the number of spanning trees. I saw a promising mathematical
way in a research paper at https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r25/pdf
using eigenvalues without creating the gigantic matrix. For an n x m grid, the number of spanning trees is
the product of 1/nm and all 4 - 2cos(a * pi / n) - 2cos(b * pi / m) terms, using all (a, b) pairs such that
0 <= a < n, and 0 <= b < m, except (a, b) = (0, 0). For precision reasons, I took log to base 10 to change
the product to a sum, and eventually changed the result to the desired scientific notation. I used python's
mpmath for precision purposes.

As the puzzle mentions, the number of spanning trees is exponential on the number of nodes in the graph. If
the graph was a complete graph Kn with labeled vertices (a rectangular maze is not a complete graph, of
course), Cayley's formula tells us that the number of distinct spanning trees is n^(n-2). Even with the
rectangular grid graphs in this puzzle, the number of spanning trees (i.e. the number of distinct mazes for
the fixed grid with labeled cells) is a staggering 1175-digit number (for the main puzzle) and a 61572-digit
number (for the bonus puzzle)!
'''

import numpy as np
import math
from mpmath import *
from datetime import datetime

print(datetime.now(), "start main puzzle")
#set ROWS, COLS to 42, 57 for main puzzle, and to 3, 3 or 10, 15 for the given examples
#for bonus puzzle, do not set here; set the values later in the program
ROWS = 42
COLS = 57
TOT_CELLS = ROWS*COLS

#Function to calculate the approximate scientific notation for e^x
def approx_exp_scientific(x):
    exponent_10 = x * np.log10(np.e) #use the property e^x = 10^(x * log10(e)) to avoid overflow
    mantissa_log, exponent_int = math.modf(exponent_10) #split the base-10 exponent into integer and fractional parts
    mantissa = np.power(10, mantissa_log) #mantissa is 10 raised to the fractional part
    return mantissa, int(exponent_int)

#set up and populate adjacency matrix and diagonal degree matrix
adj_mat = [[0 for _ in range(TOT_CELLS)] for _ in range(TOT_CELLS)]
diag_deg_mat = [[0 for _ in range(TOT_CELLS)] for _ in range(TOT_CELLS)]
for cell in range(TOT_CELLS):
    if (cell+1)%COLS != 0:
        adj_mat[cell][cell+1] = 1
        adj_mat[cell+1][cell] = 1
        diag_deg_mat[cell][cell] += 1
        diag_deg_mat[cell+1][cell+1] += 1
    if cell < TOT_CELLS - COLS:
        adj_mat[cell][cell+COLS] = 1
        adj_mat[cell+COLS][cell] = 1
        diag_deg_mat[cell][cell] += 1
        diag_deg_mat[cell+COLS][cell+COLS] += 1

laplacian_mat = np.array(diag_deg_mat) - np.array(adj_mat)
temp_mat = np.delete(laplacian_mat, 0, axis=0)
cofactor_mat = np.delete(temp_mat, 0, axis=1)
sign, logabsdet = np.linalg.slogdet(cofactor_mat)
mantissa, exponent = approx_exp_scientific(logabsdet)
print("Main Puzzle: ROWS =", ROWS, "COLS =", COLS)
print("ANSWER: Number of distinct mazes:", f"e^{logabsdet} approximately = {mantissa:.4f}e+{exponent} approximately\n")

print(datetime.now(), "done main, start bonus puzzle")
mp.dps = 50
#for bonus puzzle, set ROWS, COLS here
ROWS = 342
COLS = 357
log10_res = -1 * mp.log10(ROWS*COLS)

for row in range(ROWS):
    for col in range(COLS):
        if row == 0 and col == 0:
            continue
        log10_res += mp.log10(4 - 2*mp.cos(mp.pi*row/ROWS) - 2*mp.cos(mp.pi*col/COLS))

mantissa_log, exponent_int = math.modf(log10_res) #split the base-10 exponent into integer and fractional parts
mantissa = np.power(10, mantissa_log) #the mantissa is 10 raised to the fractional part
print("Bonus Puzzle: ROWS =", ROWS, "COLS =", COLS)
print("ANSWER: Number of distinct mazes:", f"{mantissa:.4f}e+{int(exponent_int)} approximately")
print(datetime.now(),"done bonus puzzle")

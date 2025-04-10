'''
My IBM Ponder This March '25 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/March2025.html
Sanandan Swaminathan, submitted March 4, 2025

This puzzle reminded me of an electric circuits undergrad course, without capacitors and inductors muddying
the waters here :). Of course, it's more of a graph theory and linear algebra problem. If we just had to
find the effective resistance between two nodes in a resistor circuit, we could apply a 1 amp current/1 volt
battery across the nodes, set up equations with Kirchhoff's laws, maybe put them in matrix form, and
solve. Here, we need to find effective resistances across all node pairs, and we need to find these
for different graphs until a minimal edge solution is found. An efficient way to do this is to use
the Laplacian matrix (see "resistance distance" at https://en.wikipedia.org/wiki/Resistance_distance).
Here, the edge weights represent "conductance" (1/resistance); multiple edges in parallel between two
adjacent nodes means higher conductance. Apart from circuit analysis, the Laplacian method has several
applications including data science. For example, the "weighted circuit" could represent a social network,
and the "effective resistance" between two arbitrary nodes could represent the effective dislike/affinity
between two adjacent or non adjacent people. Or, in eCommerce, the edge weights could represent correlation
between two adjacent products (nodes) or how often they were bought together, and effective correlation
strength between adjacent or non adjacent products could be determined.

The procedure I used was as follows:
a) Generate simple (no self loops, no multi edges), connected, non-isomorphic, unweighted, undirected graphs.
If there were disconnected components in the graph, the resistance between nodes in different components would be
undefined. As per a constraint given AFTER the example in the puzzle, we only generate graphs with minimum vertex
degree of 2. It seems this constraint is not applicable to a specific statement in the example, the statement
about an optimal solution with N = 5 (10 distinct pairwise resistances) and 8 edges. But more on that later. Also,
we pick an arbitrary limit for the maximum number of edges to be tried to bound the search, and raise it depending
on the results. I used sagemath's nauty_geng() function to extract the desired graphs to be evaluated.
b) For each simple graph, create the degree matrix D and adjacency matrix A. Laplacian L = D - A. Take the
inverse of L + ((1/M) * (M x M matrix of 1's)). M is the total number of vertices in the graph (M >= N, where N = 10
in the main puzzle, and N = 12 in the bonus puzzle). There are N "specified vertices" and M-N "additional vertices"
(M-N >= 0). Technically, we should be taking the Moore-Penrose pseudoinverse (sympy's pinv() function), but we have
a square matrix that will be invertible given a connected resistor network, so regular inv() suffices (and faster).
The effective resistances of all pairs of nodes can be seen from the inverse matrix X. The effective resistance for
node pair (i,j) is X[i,i] + X[j,j] - 2*X[i,j].
c) If M > N, we can check if there is any combination of N "specified vertices" that gives N*(N-1)/2 distinct,
pairwise effective resistances.
d) We can then expand the simple graph by adding multiple edges on existing edges in all possible combinations.
Of course, we do this only upto our arbitrary limit on the maximum number of edges for a given run of the program.
e) For every new configuration of the multi-edged graph, we can calculate the pairwise effective resistances
again. However, calculating the whole matrix inverse again is expensive. When there are only small perturbations
in the underlying Laplacian matrix, as is the case when an edge is added on an existing edge, we can take
advantage of the Sherman-Morrison formula (see https://en.wikipedia.org/wiki/Sherman%E2%80%93Morrison_formula).
The formula lets us determine the new inverse using the old inverse without doing a fresh inverse. If an edge
(resistor) is being added on an existing edge between nodes i and j, the Laplacian matrix L is only changing
in 4 cells: L[i,i] and L[j,j] increase by 1, and L[i,j] and L[j,i] reduce by 1. Hence we can choose two vectors
u and v containing [...1...-1...] such that L + (u * transpose of v) will represent the new Laplacian matrix. Since
we know L's previous inverse, the perturbed L's inverse can be found with the Sherman-Morrison formula without
calculating the whole inverse again, making it significantly faster. We have to calculate the inverse of the Laplacian
matrix only once per starting graph; all multi-edge additions after that just use Sherman-Morrison.

For the main puzzle (N = 10), I ran the program with graphs containing M = 10 and 11 vertices in parallel. I set
the arbitrary limit on total number of edges as 15, and found a solution with 11 vertices (10 "specified vertices",
1 "additional vertex") and 15 edges (no multi edges). We don't need to try with more vertices. We can see that there
can't be a solution with less than 15 edges. If a secified vertex A (having minimum degree 2) is only connected to
specified vertices B and C, then consider the net resistance BCnet between B and C if the AB and AC edges (resistors)
were removed. Now consider the triangle of resistances BCnet, AB and AC. Clearly, across AB and AC we would see the same
effective resistance which violates the requirement. To adhere to the requirement of distinct effective resistances
between all specified vertex pairs, A would either need to be connected to at least three specified vertices, or A
would need to be connected to at least two "additional vertices", or A would need to be connected to at least one specified
vertex and at least one additional vertex. Now consider the total number of edges T connected to the N "specified vertices".
If A was connected to at least three specfied vertices, then A's share in T would be at least 3 * 1/2 = 3/2. If A was
connected to at least two additional vertices, then A's share in T would be at least 2. If A was connected to at least one
specified vertex and at least one additional vertex, then A's share in T would be at least 1 + 1/2 = 3/2. Thus, the total
number of edges T connected to the N "specified vertices" would be at least 3N/2. Hence, with N = 10, we can't satisfy the
requirements with less than 15 edges.

For the bonus puzzle (N = 12), I ran the program with graphs containing M = 12 and 13 vertices in parallel, with the
arbitrary limit on number of edges set as 20. 3 planar solutions and at least 1 non-planar solution were found with 13
vertices (12 "specfied vertices", 1 "additional vertex") and 18 edges. We don't need to try with more vertices. We can't have
a solution with less than 3N/2 = 18 edges. For the bonus puzzle, note that there is also a graph planarity check to identify
the three planar solutions and at least one non-planar solution (13 vertices with 18 edges itself gave 5 non-planar solutions
apart from the 3 planar solutions needed). Note that there is no need to check if the solutions are mutually non-isomorphic
since that is ensured by the way the graphs were generated (using nauty_geng) and multi edges were added. Of course, networkx
module's is_isomorphic() function could be used to check isomorphism if desired. As it turned out, neither the main nor bonus
solutions found had any multi edges, and in both cases, there was exactly one "additional vertex".

Note that the program uses 1 ohm resistors as edges, though this can obviously be scaled to any R, like in the give example
with R = 47 ohms. The actual effective resistance values in a circuit obviously depend on the value of R, but we are only
interested in seeing if there are comb(N, 2) = N*(N-1)/2 distinct pairwise effective resistances in N specified nodes, and
any value of R will give the same yes/no answer (edge weights with R = 1 simplify things).

Also note: If the main puzzle had asked us to find all solutions, or if the bonus puzzle had asked us to find all non-planar
solutions, we would just tweak the program runs when running with higher M. We would simply search with the current best edge
limit as the limit to capture any potential solutions with higher M. All solutions can easily be found, but I didn't bother with
it since the main puzzle only asks for 1 minimal edge solution, and the bonus puzzle only asks for all 3 planar and at least
1 non-planar minimal edge solution.

A note on solutions with 8 edges for the given example (N = 5): When I ran the program with N = 5, and M = 5, 6, 7, 8, 9
vertices with max number of edges as 9, I found several solutions having 9 edges (including the given example with the given 10
pairwise effective resistances). But I didn't find any solution with 8 edges as mentioned in the example. Then I realized that
the constraint "no vertex may be connected to only one neighbor" is mentioned AFTER the example. So, it seems that that constraint
is only applicable to the main and bonus puzzles, but NOT to the example. Tricky way to impose the additional constraint! When I
removed the restriction of min vertex degree 2 in the starting simple, connected graphs, there were many solutions with 8 edges
with N = 5 and M = 6, 7, 8 vertices (but not with fewer than 8 edges). Of course, in these graphs, there is at least one "dangling
resistor" (a node adjacent to only one other neighbor node, whether with single edge or multi edges). One example of such a solution
with N = 5, and 8 edges, is as follows (nodes 1 through 5 are specified vertices, and node 6 is an additional vertex):
[(1, 4), (1, 4), (1, 5), (6, 4), (6, 5), (2, 5), (2, 5), (3, 5)]
Note how vertex 3 is only connected to one neighbor 5, and vertex 2 is also connected to only one neightbor 5 (with two edges). But
this graph does give 10 distinct pairwise effective resistances between nodes 1 through 5 just using 8 edges, as mentioned in the
puzzle. Pesky little mystery about the example solved!

The answers found for the main and bonus puzzles were as follows (main puzzle's search completed in about 2 minutes, and the bonus
took a couple of hours):

An edge list solution (main puzzle asks for only one solution) for MAIN puzzle (having N = 10, M = 11 vertices
with vertices numbered 1 through 10 as specified vertices and vertex 11 additional, every vertex connected to
more than one neighbor, 15 edges with no multi edges, 45 distinct pairwise effective resistances between specified
vertices 1 through 10):

[(1, 5), (1, 8), (1, 9), (2, 6), (2, 8), (2, 10), (3, 7), (3, 9), (3, 10), (4, 8), (4, 11), (5, 9), (5, 10),
(6, 11), (7, 11)]

8 edge list solutions for BONUS * puzzle, including all 3 planar solutions (well, 3 planar solutions were found with 18 edges,
so it must be "all 3 planar solutions" as mentioned in the puzzle), and 5 non-planar (bonus puzzle asks for only one non-planar)
solutions. These solutions have N = 12, M = 13 vertices with vertices numbered 1 through 12 as specified vertices and vertex 13
additional, every vertex connected to more than one neighbor, 18 edges with no multi edges, 66 distinct pairwise effective
resistances between specified vertices 1 through 12:

All 3 PLANAR solutions:

[(1, 7), (1, 9), (1, 10), (2, 8), (2, 10), (2, 12), (3, 9), (3, 10), (3, 11), (4, 9), (4, 13), (5, 11),
(5, 13), (6, 12), (6, 13), (7, 13), (8, 11), (8, 12)]

[(1, 6), (1, 9), (1, 10), (2, 7), (2, 10), (2, 12), (3, 8), (3, 11), (3, 12), (4, 9), (4, 11), (4, 12),
(5, 10), (5, 13), (6, 9), (6, 11), (7, 13), (8, 13)]

[(1, 6), (1, 8), (1, 10), (2, 7), (2, 11), (2, 12), (3, 8), (3, 9), (3, 11), (4, 9), (4, 10), (4, 12),
(5, 11), (5, 13), (6, 13), (7, 13), (8, 10), (9, 12)]

5 NON-PLANAR solutions:

[(1, 7), (1, 9), (1, 10), (2, 8), (2, 10), (2, 11), (3, 9), (3, 11), (3, 12), (4, 9), (4, 13), (5, 10),
(5, 13), (6, 12), (6, 13), (7, 11), (7, 12), (8, 13)]

[(1, 6), (1, 9), (1, 11), (2, 7), (2, 9), (2, 10), (3, 8), (3, 11), (3, 12), (4, 9), (4, 10), (4, 12),
(5, 11), (5, 13), (6, 10), (6, 12), (7, 13), (8, 13)]

[(1, 6), (1, 9), (1, 10), (2, 7), (2, 10), (2, 12), (3, 8), (3, 11), (3, 12), (4, 9), (4, 10), (4, 11),
(5, 9), (5, 13), (6, 11), (6, 12), (7, 13), (8, 13)]

[(1, 6), (1, 8), (1, 10), (2, 7), (2, 11), (2, 12), (3, 8), (3, 11), (3, 12), (4, 9), (4, 10), (4, 11),
(5, 9), (5, 13), (6, 13), (7, 13), (8, 10), (9, 12)]

[(1, 6), (1, 10), (1, 11), (2, 7), (2, 11), (2, 12), (3, 8), (3, 9), (3, 11), (4, 8), (4, 13), (5, 9),
(5, 13), (6, 10), (6, 12), (7, 13), (8, 10), (9, 12)]

'''

from sympy import *
from itertools import combinations
import networkx as nx
from datetime import datetime
#from time import perf_counter

'''
To run the program, feed the appropriate graphs file in the driver section of this program
based on desired run parameters. Each file would pertain to a fixed number of vertices M.
Hence the program can be run in parallel for different M. Pick an arbitrary limit E on the
number of edges, so a file would contain simple (no self loops, no multi edges), connected,
non-isomorphic, unweighted, undirected graphs with min vertex degree 2 having M vertices
and between M and E edges (M-1 edges would give spanning trees but not give min vertex
degree 2 for every vertex). Multi edges will be added by this program.
Set M and N below as appropriate. Set edge_limit below to an arbitrary limit for the bonus
puzzle or to limit+1 for the main puzzle. If a feasible graph is found during a run of the
program, and the number of edges needed has been lowered, then subsequent graphs in the run
only need to be tried with upto the reduced number of edges for the bonus puzzle (which asks
for multiple solutions), and only upto reduced number of edges - 1 for the main puzzle (which
asks for only one solution).
If solution(s) is/are found, try with higher number of vertices (upto new edge_limit-1) and
appropriate edge_limit to see if there is any solution with more "additional vertices" that
give a solution with fewer edges. In the case of the bonus puzzle, if all 3 planar solutions
and at least 1 non-planar solution were not found in a given run, then set the edge_limit to
the edge_limit found since there could be more solutions at that edge_limit with more vertices.
If it turns out that we don't find any solution with the arbitrary limit that we started with
for the number of edges, we can repeat the process with a raised edge limit. This wasn't needed
with the starting limits of 15 and 20 picked for the main and bonus puzzles respectively.

Note: If the main puzzle asked us to find all solutions, or if the bonus puzzle asked us to find
all non-planar solutions, we would just tweak the program runs when running with higher M. We
would simply search with the current best edge_limit as the limit to capture other potential solutions
that have the same number of edges with higher M.

Having planned the strategy to find enough answers for the main and bonus puzzle asap, it turned out
that sufficient solutions were found pretty early in the process: with 11 vertices and 15 edges for the
main puzzle, and with 13 vertices and 18 edges for the bonus.
'''
BONUS = False #set to False for main, True for bonus
M = 11 #number of vertices: answers found with 11 for main, 13 for boFnus
edge_limit = 16 #set to desired limit + 1 for main (solution found turned out to have 15 edges, edge_limit init 16)
if BONUS:
    edge_limit = 18 #set to desired limit for bonus (all the solutions turned out to have 18 edges)
N = 10 #number of "specified vertices": set to 10 for main, 12 for bonus as given in the puzzle

NEEDED_PAIRS = (N*(N-1))//2
possible_solutions = []
included_nodes_combs = []
for comb in combinations([_ for _ in range(M)], N):
    included_nodes_combs.append(comb)

uvT_vectors = [[None for _ in range(M)] for _ in range(M)]
for i in range(M):
    for j in range(i+1, M):
        u = Matrix([0 for _ in range(M)])
        u[i] = 1
        u[j] = -1
        vT = Matrix([0 for _ in range(M)])
        vT[i] = 1
        vT[j] = -1
        vT = vT.T
        uvT_vectors[i][j] = (u, vT)

phi = Rational(1,M) * ones(M,M)

def print_result(Amatrix, comb):
    global edge_limit
    node_label_map = [-1]*M
    for i in range(N):
        node_label_map[comb[i]] = i+1
    extra_node_label = N+1
    for i in range(M):
        if node_label_map[i] == -1:
            node_label_map[i] = extra_node_label
            extra_node_label += 1
    edge_list = []
    for row in range(M):
        for col in range(row + 1, M):
            for repeat_multiedge in range(Amatrix[row,col]):
                edge_list.append((node_label_map[row], node_label_map[col]))
    print(datetime.now(), "Edge list:", edge_list)
    print("Number of edges:", len(edge_list))
    possible_solutions.append(edge_list)
    if len(edge_list) < edge_limit:
        edge_limit = len(edge_list)
    return

def calculate_pairs(X_inv, Amatrix):
    resistances = [[None for _ in range(M)] for _ in range(M)]
    resistance_set = set()
    for i in range(M):
        for j in range(i+1, M):
            resistances[i][j] = X_inv[i,i] + X_inv[j,j] - (2*X_inv[i,j])
            resistance_set.add(resistances[i][j])
    if len(resistance_set) < NEEDED_PAIRS:
        return

    for comb in included_nodes_combs:
        equiv_resistance_set = set()
        num_pairs_exist = True
        for i in range(N-1):
            for j in range(i+1,N):
                if resistances[comb[i]][comb[j]] in equiv_resistance_set:
                    num_pairs_exist = False
                    break
                equiv_resistance_set.add(resistances[comb[i]][comb[j]])
            if num_pairs_exist == False:
                break
        if num_pairs_exist:
            print_result(Amatrix, comb)
    return
    
def recurs_add_edge(X_inv, Amatrix, edgelist, edgelistlen, rem_edges, curr_pos):
    if rem_edges <= 0:
        return
    for edge_idx in range(curr_pos, edgelistlen):
        updated_X_inv = X_inv
        for extra_edge in range(1, rem_edges+1):
            vtx = uvT_vectors[edgelist[edge_idx][0]][edgelist[edge_idx][1]][1] * updated_X_inv
            updated_X_inv = updated_X_inv - ((updated_X_inv * uvT_vectors[edgelist[edge_idx][0]][edgelist[edge_idx][1]][0] * vtx)/ \
                                             (1 + (vtx * uvT_vectors[edgelist[edge_idx][0]][edgelist[edge_idx][1]][0])[0,0]))
            Amatrix[edgelist[edge_idx][0], edgelist[edge_idx][1]] += 1
            calculate_pairs(updated_X_inv, Amatrix)
            recurs_add_edge(updated_X_inv, Amatrix, edgelist, edgelistlen, rem_edges - extra_edge, edge_idx+1)
        Amatrix[edgelist[edge_idx][0], edgelist[edge_idx][1]] -= rem_edges
    return

'''
One way to generate simple, non-isomorphic graphs is to use sagemath's nauty_geng() function.
Parameters that can be passed include number of vertices, minimum number of
edges, maximum number of edges, connected, minimum vertex degree (and many others).
Simple graphs can also be downloaded from http://combos.org/nauty , but there's a
cap of 100k graphs per query, insufficient for the bonus problem.
This whole program could be written in sagemath python to avoid extracting graphs
into data files, but sagemath python typically contains an older python dist that
may not be as convenient.

To extract desired graphs into a file with sagemath, I wrote a short sagemath snippet
extract_graphs.sage (given below), and ran it in the terminal with the command:
sage extract_graphs.sage
Change the first two lines based on the graphs that need to be extracted for a given
run of the program.

with open("<directory path>/file_11v_upto15e_sage.txt", 'w') as fp:
    for g in graphs.nauty_geng("11 11:15 -c -d2"): #num nodes, min edges:max edges, connected, min vertex degree 2
        #mylist = list(g.adjacency_matrix())
        print(g.edges(sort=True, labels=False), file=fp)
'''

#file_11v_upto15e_sage.txt gives answer for main, file_13v_upto18e_sage.txt gives answers for bonus
datafilename = "file_11v_upto15e_sage.txt"
print(datetime.now(), "start", "N", N, "M", M, "Datafile name", datafilename)
if BONUS:
    print("Edge limit", edge_limit)
else:
    print("Edge limit", edge_limit-1)
cnt = 0
datafile = open(datafilename,"r")
for graph_edges in datafile:
    cnt+=1
    if cnt%1000 == 0:
        print(cnt, datetime.now())
    edge_list = eval(graph_edges)
    D_mat = zeros(M,M)
    A_mat = zeros(M,M)
    for edge in edge_list:
        A_mat[edge[0], edge[1]] += 1
        A_mat[edge[1], edge[0]] += 1
        D_mat[edge[0], edge[0]] += 1
        D_mat[edge[1], edge[1]] += 1
    #technically, we should find the Moore-Penrose pseudoinverse, i.e. sympy's pinv() function, but for this
    #problem with square matrix resistor network invertible, the regular inverse inv() suffices and is faster
    X_inv_mat = (D_mat - A_mat + phi).inv()
    calculate_pairs(X_inv_mat, A_mat)
    if BONUS:
        recurs_add_edge(X_inv_mat, A_mat, edge_list, len(edge_list), edge_limit - len(edge_list), 0)
    else:
        recurs_add_edge(X_inv_mat, A_mat, edge_list, len(edge_list), edge_limit - 1 - len(edge_list), 0)
datafile.close()

if len(possible_solutions) > 0:
    print("Number of edges:", edge_limit)
    sol_cnt = 0
    if not BONUS:
        for sol in possible_solutions:
            if len(sol) == edge_limit:
                print(sol)
                sol_cnt += 1
        print("Found:", sol_cnt)
    else:
        for sol in possible_solutions:
            if len(sol) == edge_limit and nx.is_planar(nx.Graph(sol)):
                print(sol)
                sol_cnt += 1
        print("PLANAR count:", sol_cnt)
        sol_cnt = 0
        for sol in possible_solutions:
            if len(sol) == edge_limit and not nx.is_planar(nx.Graph(sol)):
                print(sol)
                sol_cnt += 1
        print("NON PLANAR count:", sol_cnt)
else:
    print("No solution found, try changing number of vertices and file, with same edge_limit,", \
          "or raise edge limit and repeat process")

print(datetime.now(), "end: simple graph count", cnt, "N", N, "M", M, "Datafile name", datafilename)

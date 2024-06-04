'''
My IBM Ponder This May '24 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/May2024.html
Sanandan Swaminathan, submitted May 6, 2024

This was a particularly knotty/naughty/NAUTY problem. I eventually settled on thinking of it as
a regular bipartite graph with N^2 + N + 1 nodes in each partition. But before that,
I was trying to attack it in different ways. In the bonus * puzzle, there are comb(73, 9)
possibilities for the 9 symbols on a card (or a symbol on 9 cards). So we are looking for distinct
card decks containing 73 cards from comb(73, 9) cards, i.e. search comb(comb(73, 9), 73) to
find sets that meet the conditions.
This makes it intractable to treat it like trying to find maximum sized (73) maximal cliques
in the k-regular graph. When treating it as a Levi graph of 73 points (symbols) and 73 lines (cards),
the issue is with the duplication in counting that occurs. In puzzles, I generally don't get
exposed to projective planes beyond the simplest type - Fano planes, so this was an interesting
learning opportunity. Incidence matrix and Graeco-Latin squares (mutually orthogonal Latin
squares) help with construction. But the key thing in this puzzle is to count isomorphisms
of a solution - the size of the automorphism group of a solution graph.
I found that the pynauty package has that exact function - given a graph (colored or not), it
reports the automorphism group size (well, it goes beyond that by providing a generator that can
be used to generate the actual isomorphic graphs, but we only need the count). So, my program
just generates a single working graph, and feeds it to pynauty to get the number of isomorphisms.
Of course, the number of distinct ways to create the card deck is simply (N^2 + N + 1)! / number
of isomorphisms. This takes care of all the duplicate counting occurring in the permutations.

The program completed instantaneously for both the main and bonus * puzzles, which is really a testament
to how fast NAUTY is.

Answers: Number of ways to make distinct decks:
Main puzzle (N = 4): 422378820864000
Bonus * puzzle (N = 8): 90399509839271079668491458784005740889517921781547218950513473999637402251071324160000000000000000

'''

from pynauty import *
import math
from datetime import datetime

print("Start", datetime.now())
N = 8 # N is a prime power, N = 4 for main puzzle, N = 8 for bonus * puzzle
# N+1 symbols per card; a symbol appears on N+1 cards in a deck
# S is number of cards in a deck, and total number of different symbols
S = (N*N) + N + 1 
edges = [[False]*S for _ in range(S)] # rows indicate "from" card, cols indicate "to" cards; only forward edges needed
symbol_dict = {} # key is symbol, value is list of cards having that symbol
for sym in range(S):
    symbol_dict[sym] = []

# Pre-fill some rows and columns in the S x S incidence matrix for the graph
sym_to_cards_matrix = [[0]*S for _ in range(S)]
for sym in range(N+1):
    sym_to_cards_matrix[sym][0] = 1

sym = 0
card = 1
while sym < N+1 and card < S:
    sym_to_cards_matrix[sym][card] = 1
    if card%N == 0:
        sym += 1
    card += 1

card = 1
sym = N+1
while card < N+1 and sym < S:
    sym_to_cards_matrix[sym][card] = 1
    if sym%N == 0:
        card += 1
    sym += 1

card = N+1
sym = N+1
while sym < (N*2)+1 and card < S:
    sym_to_cards_matrix[sym][card] = 1
    card += N
    if card >= S:
        sym += 1
        card = sym

card = N+1
sym = (N*2)+1
while card < (N*2)+1 and sym < S:
    sym_to_cards_matrix[sym][card] = 1
    card += 1
    if sym%N == 0:
        card = N+1
    sym += 1

# Populate the forward edges (between cards), and the lists of cards for the symbols
for sym in range(S):
    for card in range(S):
        if sym_to_cards_matrix[sym][card] == 1:
            for prevcard in symbol_dict[sym]:
                edges[prevcard][card] = 1
            symbol_dict[sym].append(card)

# Recursive function to find a single graph that satisfies the conditions.
# Cards are populated in N x N blocks (groups).
# Groups are numbered from 0 after the sentinel (0th) card.
def recursFindBipartite(group, sym):
    if group > N:
        # If we've reached the end of the grid for both cards and symbols, we've
        # found a solution.
        if sym == S-1:
            return True
        else:
            if recursFindBipartite(2, sym+1):
                return True
            else:
                return False

    start_card = (group*N)+1
    for card in range(start_card, start_card+N):
        edge_match = False
        for prevcard in symbol_dict[sym]:
            if edges[prevcard][card] == 1:
                edge_match = True
                break
        if edge_match == False:
            for prevcard in symbol_dict[sym]:
                edges[prevcard][card] = 1
            symbol_dict[sym].append(card)
            if recursFindBipartite(group+1, sym):
                return True
            symbol_dict[sym].pop(-1)
            for prevcard in symbol_dict[sym]:
                edges[prevcard][card] = 0
    return False

# Start the recursion from group 2 (since sentinel card, and groups 0 and 1 are already pre-filled)
recursFindBipartite(2, (2*N)+1)

# Prepare adjacency dict of the working graph found. This is fed to pynauty to determine automorphisms.
edges_dict = {}
for sym, cardlist in symbol_dict.items():
    # in the bipartite graph, let us label cards from 0 to S-1, and symbols from S to 2S -1.
    edges_dict[sym+S] = cardlist

# We don't need vertex or edge coloring. Simply divide the automorphism group size for the
# uncolored bipartite graph by 2.
g = Graph(number_of_vertices=2*S, directed=False, adjacency_dict = edges_dict, vertex_coloring = [])
result = autgrp(g)
automorph_grpsize = int(result[1])//2
print("Number of isomorphisms", automorph_grpsize)
print("Answer: with number of cards and symbols", S, ", symbols per card and cards per symbol", N+1, \
      ", N =", N, "...")
print("Number of distinct ways to make the deck:", math.factorial(S)//automorph_grpsize)
print("End", datetime.now())

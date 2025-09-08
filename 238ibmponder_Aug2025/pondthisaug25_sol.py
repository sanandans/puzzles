'''
My IBM Ponder This August '25 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/August2025.html
Sanandan Swaminathan, submitted July 31, 2025

This is a cute game theory puzzle, especially because the answers jumped out immediately without any
programming despite the seemingly intractable search space (especially given the huge grid dimensions in
the bonus * puzzle). IBM Research's puzzles almost always need some programming trick to attack the large
search space without expending heavy compute resources, but not this one. Still, I've written a short code
snippet below to compute f(a, b), the grid value, for grids of arbitrary dimensions. The program completes
instantaneously for both the main and bonus * puzzles. 

All we need are the prime factorizations of the number of rows and columns, so O(sqrt(N)) performance where
N is the larger grid dimension. For my submission, I simply plonked the given numbers into an online prime
factorization calculator. For both the main and bonus * puzzles, the answers are 1 + the highest prime factor
of the respective b number. That just happens to be the case with these specific puzzles. Once the pattern
became clear, the general formula for any a and b became obvious, and that is what I use in the generalized
code snippet below.

In the main puzzle, the starting grid has 2663**2 × 7703**4 × 8089**3 × 11491**3 × 12401 × 17389 rows.
The "exponent sum" (sum of exponents) is 14. There are 149**3 × 3407**5 × 3847**4 × 5981**3 × 6607 columns.
The exponent sum is 16. Alice can always win this game by taking advantage of having larger exponent sum,
whether she starts the game or not. If she starts, she can split the grid vertically into 6607 identical grids,
each having 149**3 × 3407**5 × 3847**4 x 5981**3 columns. This is like 6607 separate games with Bob playing
next. Note that Alice has an exponent sum advantage of 1 in each of them. Say Bob plays in the leftmost vertical
sub grid. He can horizontally split it into 17389 identical sub grids, or 12401 × 17389 sub grids, or any factor
of a (> 1). Whatever he does, Alice would still have greater degree of freedom (number of moves) in all those sub
grids, and Alice would win each of them. She will never let her exponent sum in smaller sub grids that will get
created fall below Bob's. The same thing would occur in the 6606 other identical vertical grids that Alice had
created in her first move. Hence Alice would win the overall game if she started.

On the other hand, if Bob starts the game, whatever number of identical horizontal grids he splits the
original grid into, Alice would have exponent sum advantage in each of them, even greater than the initial
exponent sum difference, hence Alice would win the overall game if Bob started it.

To counter Alice’s advantage, we can introduce 1 + 6607 = 6608 extra 2 x 1 pieces (which can only be used by Bob).
If Alice starts this new game, and she splits the big grid into 6607 identical vertical sub grids, Bob could
simply split one of the 2 x 1 pieces. Then, Alice would need to cut in one of the 6607 sub grids. Let’s say she
splits the leftmost one into 5981 identical sub grids. Note that in each of these sub grids, both players now
have the same degree of freedom, so the second player would win each of these smaller games. Again, Bob could
simply split a second 2 x 1 piece. Every time Alice splits one of the 6607 sub grids for the first time, Bob
would split a 2 x 1 piece. But if Alice ever plays in one of the sub grids that have equal exponent sum for both
players, Bob would do his next move's cuts in that sub grid. Bob would finish every smaller game, hence Bob
would win though Alice started the game. Even if Alice’s very first move split the original grid into
5981 x 6607 identical vertical sub grids (or some such factor of the number of columns), it would only hasten
reaching the state where both players have the same exponennt sum in the smaller games. Even if Alice initially
only created a small number of identical vertical sub grids, like 149, Bob would still win (even more
comfortably).

On the other hand, if Bob started the game, he wouldn’t make his first move in the big grid because that would
only intensify the exponent sum advantage that Alice would have in each of the resulting identical sub grids. If
Bob split a 2 x 1 piece, Alice could respond by creating 6607 identical vertical sub grids from the big grid,
and still have an exponent sum advantage of 1 in each of those sub grids. Again, Bob would split a 2 x 1 piece.
Alice would respond by splitting one of the 6607 sub grids into 5981 identical sub grids. Both players would
have the same exponent sum in these 5981 smaller games. If Bob plays in one of them, then Alice would play in
one of the resulting sub grids. Instead, if Bob splits a 2 x 1 piece, Alice could respond by splitting one of
the other 6606 sub grids into 5981 smaller games. Alice would finish every smaller game, and Bob would consume
the 6608 2 x 1 pieces just before Alice splits the last of the 6607 sub grids. Thus, Alice would win the game
though Bob started it. We can see that no combination of moves by Bob can prevent Alice from prevailing.

Thus, 6608 extra 2 x 1 pieces ensure that whoever starts the game loses. We can also see that, if there are
less than 6608 extra 2 x 1 pieces, then Alice would win regardless of whether she starts the game or not. On
the other hand, if there are more than 6608 extra 2 x 1 pieces, then Bob would win regardless of whether he
starts the game or not. Nash equilibrium to achieve the "whoever starts loses" outcome occurs only when there
are exactly 6608 extra 2 x 1 pieces.

In the bonus puzzle, the starting grid has 109**2 × 3001**3 × 5591**3 × 5839 × 5981 × 7211**8 × 8089 × 11897**2 ×
12893**11 × 13859**3 × 14431**5 × 15061**3 × 16183 × 16607**3 × 17293 × 17341 rows. The exponent sum is 49.
There are 151**3 × 239**2 × 1229**3 × 4691**11 × 5879**7 × 7351 × 8317**3 × 8501 × 10133**7 × 16339 × 16883**6 ×
16903**6 columns. The exponent sum is 51. Again, Alice has the exponent sum advantage, and would win, whether she
starts the game or not. Similar to the main puzzle, adding 1 + 16903 = 16904 extra 2 x 1 pieces will ensure that
whoever starts the game loses. We can also see that, if there are less than 16904 extra 2 x 1 pieces, then Alice
would win regardless of whether she starts the game or not. On the other hand, if there are more than 16904 extra
2 x 1 pieces, then Bob would win regardless of whether he starts the game or not. Nash equilibrium to achieve the
"whoever starts loses" outcome occurs only when there are exactly 16904 extra 2 x 1 pieces.

We can see that the logic generalizes to any grid size. If the exponent sum difference is 0, then the grid's value
is 0 (whoever starts the game with such a grid loses). If number b's exponent sum is 1 more than number a's, then
the grid value is 1. Alice would win with such a grid whether she starts or not. If she starts, she would split
it using a single prime factor, causing sub games having equal exponent sum. Alice would win each of these sub
games. If Bob plays first, no matter how many identical sub grids he cuts the big grid into, Alice would have
exponent sum advantage of 2 in each of them, hence would win each of them. To compensate for Alice's advantage,
a single 2 x 1 piece has to be added (which only Bob can use with his horizontal cut). That makes the big grid's
value 1. If number a's exponent sum is 1 more than number b's, the grid value is -1. Bob would win with such a grid
whether he starts or not. To compensate, a 1 x 2 piece has to be added to the game (which only Alice can use with
her vertical cut). That makes the big grid's value -1. Now consider exponent sum difference > 1. WLOG, assume number
b's exponent sum is 2 or more higher than number a's. Then the grid value is based on b's prime factorization. Imagine
listing out b's prime factorization (listing a prime factor multiple times if its exponent > 1), in ascending order
of prime factors. Now use the numbers in the list in order from right to left. If b's exponent sum is 2 more than a's,
then the grid value would be 1 + highest number from the list. If b's exponent sum is 3 more than a's, then the grid
value would be 1 + (highest number * (1 + next number in lisr)). Note that the list can contain the same prime
factor multiple times if it has exponent > 1 in b's prime factorization. If b's exponent sum is 4 more than a's,
then the grid value would be 1 + (highest number * (1 + (next number * (1 + next next number)))). And so on for
any exponent sum difference. The recursive structure occurs because a cut splits a grid into smaller identical grids
with exponent sum difference reduced by 1 (to satisfy the requirement that "whoever starts loses"). Of course, if number
a's exponent sum is greater than number b's, then the grid value calculation remains the same except it uses a's prime
factorization, and the calculated grid value is multiplied by -1 (since we need extra 1 x 2 pieces to counter Bob's
advantage in such a grid instead of extra 2 x 1 pieces). The short program below calculates the grid value f(a, b)
for any given (a, b). It will complete fast for any arbitrary size grid... well, as fast as finding the prime
factorizations of the grid dimensions.
'''

from sympy import factorint
from datetime import datetime

def recurs_calc_value(larger_degsum_pf, pf_degree_diff):
    if pf_degree_diff == 1:
        return 1
    prime_factor = larger_degsum_pf[-1][0]
    larger_degsum_pf[-1][1] -= 1
    if larger_degsum_pf[-1][1] == 0:
        del larger_degsum_pf[-1]
    return 1 + (prime_factor * recurs_calc_value(larger_degsum_pf, pf_degree_diff - 1))

def calc_grid_value(a, b):
    a_prime_factorization_list = []
    a_degsum = 0
    for pf_tuple in sorted(factorint(a).items()):
        a_degsum += pf_tuple[1]
        a_prime_factorization_list.append([pf_tuple[0], pf_tuple[1]])
    b_prime_factorization_list = []
    b_degsum = 0
    for pf_tuple in sorted(factorint(b).items()):
        b_degsum += pf_tuple[1]
        b_prime_factorization_list.append([pf_tuple[0], pf_tuple[1]])
    if a_degsum == b_degsum:
        return 0
    elif a_degsum > b_degsum:
        return -1 * recurs_calc_value(a_prime_factorization_list, a_degsum - b_degsum)
    else:
        return recurs_calc_value(b_prime_factorization_list, b_degsum - a_degsum)

print(datetime.now(), "Start")
print("Main puzzle grid value f(a, b) =", calc_grid_value(4323855975562114726518487102722055842514310244656547479, \
                      470147284842004245175081008799131351685318626829460321))
print("Bonus * puzzle grid value f(a, b) =", calc_grid_value(3396061787351437365560785267965234012799064104044242529256561027187645540909306599628231712601016121941243125433481313447172851850524777447140380830407565706177350759478762583119838528311717009, \
                      7464746477226496222046301003339284704063450899406727072696371142567730009951170882833599768380584465924066413849500475118418591755457666001930720494110499599758793660468148459835668058314279))
print(datetime.now(), "Done")

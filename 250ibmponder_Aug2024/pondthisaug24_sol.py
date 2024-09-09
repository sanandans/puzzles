'''
My IBM Ponder This August '24 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/August2024.html
Sanandan Swaminathan, submitted July 31, 2024

I interpreted the puzzle's game rules as follows:
A) Unlike the NYT Connections game, the player can get multiple sets correct in a single step. For example,
in the main puzzle, when the player initially partitions the 16 elements into 4 sets containing 4 elements each,
the player may get 4, 2, 1 or 0 sets correct in that single step.
B) In any step, the player partitions only the elements that remain in the game. For example, if the player got
2 sets out of 4 sets correct in the first step, the player will only partition the remaining 8 elements into 2
sets of 4 elements each for the second step. The new guess will not include any element that has already been
removed from the game (due to the element being in a previously correctly guessed set).
C) Unlike the NYT Connections game, there is no hint like "one away" if a guessed set has all but one correct
elements.

The program first progressively calculates the number of permutations to get a particular result, where a result
is the pair (number of correct sets, number of incorrect sets). For the main puzzle, it processes the results in
the order (2, 0), (0, 2), (3, 0), (1, 2), (0, 3), (4, 0), (2, 2), (1, 3), (0, 4), and similarly for the bonus
puzzle. For example, consider the result (1, 2) for the main puzzle, which could be the result when there are
12 elements to be partitioned into 3 sets containing 4 elements each (which means one set has already been guessed
correctly and eliminated from the game). Number of ways of getting exactly 1 set out of 3 sets correct can be
calculated as follows: There are comb(3, 1) ways to pick a set that will be correct. There are perm(3, 1) ways to
place the correct set in the result. There are (4!)^1 ways to permute the elements in the correct set (since order
of elements within a set doesn't matter). The remaining 8 elements need to be partitioned incorrectly, and the (0, 2)
result computed previously gives the number of ways to do this. The number of ways to get a (1, 2) result is the
product of the above numbers. Number of ways to get a (3, 0) result is comb(3, 3) * perm(3, 3) * (4!)^3. To find
the number of ways to get a (0, 3) result, we add the (3, 0) and (1, 2) results and subtract from 12!.

Once the number of ways to get the various results has been calculated, the program then progressively calculates
the expected value of the number of steps when there are 2 sets to be determined, then 3 sets, then 4 sets (and upto
10 sets in the case of the bonus puzzle). For example, for the main puzzle...

EV (when 2 sets remain) = 1 + [ ( Number of ways to get (0, 2) result / 8! ) * EV when 2 sets remain ].
This gives the EV when 2 sets remain.

EV (when 3 sets remain) = 1 + [ ( Number of ways to get (1, 2) result / 12! ) * EV when 2 sets remain ] +
[ ( Number of ways to get (0, 3) result / 12! ) * EV when 3 sets remain ].
This gives the EV when 3 sets remain.

EV (when 4 sets remain) = 1 + [ ( Number of ways to get (2, 2) result / 16! ) * EV when 2 sets remain ] +
[ ( Number of ways to get (1, 3) result / 16! ) * EV when 3 sets remain ] +
[ ( Number of ways to get (0, 4) result / 16! ) * EV when 4 sets remain ].
This gives us the EV when 4 sets remain, which is the answer for the main puzzle.

For the bonus puzzle, this procedure continues until we get to the EV when 10 sets remain (a set contains 5
elements in this case).

The answers I got were:

Main puzzle (EV of steps to correctly guess 4 sets, each set containing 4 elements):
161133385 / 785993 , or approximately 205.00613237013562 on average (rounded value 205 steps).

Bonus * puzzle (EV of steps to correctly guess 10 sets, each set containing 5 elements):
567777578484650345575013398126266942370695717108420029991493778656957940683502610301031303575093671980338942954400960945247498 /
9354695679658699224192571660497696297578331480009893187416894211332580459941193845964513086442538003235025006577882575623 
or approximately 60694.39326810526 on average (rounded value 60694 steps).

The program completes instantaneously for both puzzles. To run for the main puzzle, set BONUS variable to
False; to run for the bonus puzzle, set it to True.
'''

from math import perm, comb, factorial
from fractions import Fraction
from datetime import datetime

print("Start:", datetime.now())
BONUS = True #set to False for main puzzle, True for bonus puzzle
NUM_PER_SET = 4 #number of elements per set
if BONUS:
    NUM_PER_SET = 5
NUM_SETS = 4 #total number of sets
if BONUS:
    NUM_SETS = 10

#2d array for number of ways to achieve various results, where a result denotes a pair
#[number of correct sets][number of incorrect sets]
num_ways_matrix = [[0 for _ in range(NUM_SETS+1)] for _ in range(NUM_SETS+1)]
num_ways_matrix[0][0] = 1 #this is for an initial lookup when result (2, 0) is being computed
exp_vals = [0]*(NUM_SETS+1) #expected values for different remaining number of sets
pos_cnt = [0]*(NUM_SETS+1) #total number of ways to split into sets with at least 1 correct set

#progressively calculate the number of ways to get various results
for set_cnt in range(2, NUM_SETS+1):
    temp = 0
    for correct_cnt in range(set_cnt, 0, -1):
        if correct_cnt == set_cnt-1:
            continue
        incorrect_cnt = set_cnt-correct_cnt
        num_ways_matrix[correct_cnt][incorrect_cnt] = comb(set_cnt, correct_cnt) * perm(set_cnt, correct_cnt) * \
                                          ((factorial(NUM_PER_SET))**correct_cnt) * num_ways_matrix[0][incorrect_cnt]
        temp += num_ways_matrix[correct_cnt][incorrect_cnt]
    num_ways_matrix[0][set_cnt] = factorial(set_cnt*NUM_PER_SET) - temp
    pos_cnt[set_cnt] = temp

#progressively calculate the expected value of the number of steps when number of sets remaining is 2, 3, 4...
for set_cnt in range(2, NUM_SETS+1):
    temp = Fraction(factorial(set_cnt*NUM_PER_SET))
    for correct_cnt in range(set_cnt - 2, 0, -1):
        incorrect_cnt = set_cnt-correct_cnt
        temp += num_ways_matrix[correct_cnt][incorrect_cnt] * exp_vals[incorrect_cnt]
    exp_vals[set_cnt] = temp/pos_cnt[set_cnt]

ev = exp_vals[NUM_SETS].numerator/exp_vals[NUM_SETS].denominator
print("Answer (for BONUS = " + str(BONUS) + "):", \
      str(exp_vals[NUM_SETS].numerator) + ' / ' + str(exp_vals[NUM_SETS].denominator), \
      ', or approximately', ev, 'steps on average (rounded value ' + str(round(ev)) + ' steps)')
print("End:", datetime.now())

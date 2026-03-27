'''
My IBM Ponder This February '26 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/blog/ponder-this-february-2026
Sanandan Swaminathan, submitted February 2, 2026

We can consider the general problem with 5 mean and 2 dice where each dice provides equi-probable
outcomes from 1 through n (in the main puzzle, n = 2, practically a fair coin, and the dice are d6
in the bonus puzzle, but the same logic works for any n). Consider the various states the game can
be in. To continue the game at any point, either all 5 men should be at the same location,
or the men are split into groups of 2 and 3 where one of the two groups is ahead. Let E(x, y) denote
the expected number of rolls if the game is in a state where the ahead group contains x men, and
it is ahead of the group containing the remaining 5-x men by y cells. Note that, in a valid game state,
x can only be 2, 3, or 5, and y >= 0. E(x, y) includes the final, game-ending roll. For each state, for
each two-dice outcome, we would make a move with the intention of continuing the game for as long as
possible. The game starts in state (x, y) = (5, 0).

When in state (5,0), the game can only proceed by getting doubles (both dice show some d), and we
would move two men ahead by 2d to go to state (2, 2d). When in state (3, z), the game can only
proceed by getting doubles (both dice show some d), and we would move the two men who are behind ahead
by 2d. After the move, we might still have 3 men ahead, or there might be 2 men ahead now, or we get
to state (5, 0) again.

There is more case work involved when the state is (2, z). If the dice show different numbers, and the
sum of the two numbers happens to be z, then the state would change to (3, z). If we get doubles (both
dice show some d), and z + 2d < 12, then we should simply move the 2 men who are ahead further ahead by
2d so that we have a chance of surviving the next roll if it is not doubles. If z + 2d >= 12, we can
check if z is equal to d or 2d or 4d. These scenarios provide us an opportunity to reach a state where
3 men are ahead in a group. This gives a chance for the 2 men who will then be behind to hopefully get
ahead later, thereby bringing non-doubles rolls back into the picture. For example, if the current state
is (2, 2), and the dice show 2 and 2, we have a choice to go to state (2, 6) or (3, 4). In this case, we
would prefer to go to (2, 6) to have a chance with a non-doubles next roll like 1-5, 2-4, 5-1, 4-2. Now
consider the example of the current state being (2, 4), and the dice show 4 and 4. We have a choice to go
to state (2, 12) or (3, 8). If we go to (2, 12), we are relying on doubles rolls unless we manage to later
get a third man into the group of 2 ahead. But if we go to (3, 8), a few doubles would get us back to a
state where non-doubles rolls are permissible again.
Hence, if the current state is (2, z), and both dice show d, and z + 2d >= 12, then we consider the
following sub cases:
If z == d, then we go to state (3, 2z)
If z == 2d, then we go to state (3, z/2)
If z == 4d, then we go to state (3, z)
If we get any other doubles, then we have no choice but to go to the state (2, z + 2d).

Also, if we reach a state where a group of 2 men is ahead by more than 4n cells (for example, 24 in the
bonus puzzle), then the game can only continue as long as we keep getting doubles. I call this state
(2, 4n+1). Note that we cannot reach a state where a group of 3 men is ahead by more than 4n cells.
E(2, 4n+1) = 1 + (1/n)*E(2, 4n+1)
E(2, 4n+1) = n/(n-1)

Based on the optimum moves described above, the program generates the transition matrix with the
probabilities of going from one state to another. In the main puzzle, there are 12 states, including
(5, 0) and (2, 9), leading to a 12 x 12 transition matrix. In the bonus puzzle, there are 44 states including
(5, 0) and (2, 25). So, it's a 44 x 44 transition matrix.
In effect, we have 12 and 44 simultaneous equations for the main and bonus puzzles respectively with the
variables being the expected number of rolls from the various states. The equations can be expressed in the
common matrix-vector form Ax = b. The program calculates the inverse of matrix A, and multiplies it by vector
b to get the expected number of total rolls from each state. The expected number of rolls from state (5, 0)
minus 1 (the final, game-ending roll) is the desired answer. The program completes instantaneously for both
the main and bonus * puzzles. There's a boolean flag provided in case we wish to print the expected value
equations to review them for correctness of strategy implementation. Intuitively, the low answer values seem
reasonable. The answer is just 0.212008 rolls approximatelt for the bonus puzzle (excluding the final, game-ending
roll), and this is reasonable since the game will end with the very first roll five-sixth of the time.

Answers:
Main puzzle (each die has only two equi-probable outcomes, 1 and 2):
38643 / 37723 , or approx 1.024388
( 76366 / 37723 is the expected number of two-dice rolls in the game, hence
(76366 / 37723) - 1 = 38643 / 37723 is the expected number of rolls before the final roll).

Bonus * puzzle (each die has six equi-probable outcomes, 1 through 6):
666945281308130947393378290610337684171436121400818033523 / 3145854282951008317812602474580783762466266380786580139075 ,
or approx 0.212008
( 3812799564259139265205980765191121446637702502187398172598 / 3145854282951008317812602474580783762466266380786580139075
is the expected number of rolls including the final roll).
'''

from fractions import Fraction
from sympy import *
from collections import OrderedDict
from datetime import datetime

DIEFACE_MAXVAL = 6 # set to 2 for main puzzle, 6 for bonus puzzle
PRINT_EV_EQUATIONS = False # set to True to see the EV equations, False otherwise

def calc_transition_probs(state):
    global max_state_idx
    transition_dict = OrderedDict()
    if state[0] == 5:
        for double in range(1, DIEFACE_MAXVAL+1):
            next_state = (2, double*2)
            if next_state not in states_dict:
                max_state_idx += 1
                states_dict[next_state] = max_state_idx
                states_queue.append(next_state)
            if next_state not in transition_dict:
                transition_dict[next_state] = outcome_prob
            else:
                transition_dict[next_state] += outcome_prob
    elif state[0] == 3:
        for double in range(1, DIEFACE_MAXVAL+1):
            ahead_group_size = 3
            ahead_dist = state[1] - (double * 2)
            if ahead_dist == 0:
                ahead_group_size = 5
            elif ahead_dist < 0:
                ahead_group_size = 2
                ahead_dist *= -1
            next_state = (ahead_group_size, ahead_dist)
            if next_state not in states_dict:
                max_state_idx += 1
                states_dict[next_state] = max_state_idx
                states_queue.append(next_state)
            if next_state not in transition_dict:
                transition_dict[next_state] = outcome_prob
            else:
                transition_dict[next_state] += outcome_prob
    else: # state[0] is 2
        if state[1] in diff_dice_probs:
            next_state = (3, state[1])
            if next_state not in states_dict:
                max_state_idx += 1
                states_dict[next_state] = max_state_idx
                states_queue.append(next_state)
            transition_dict[next_state] = diff_dice_probs[state[1]]
        for double in range(1, DIEFACE_MAXVAL+1):
            ahead_group_size = 2
            ahead_dist = state[1] + (double*2)
            if ahead_dist > max_singles_sum:
                if state[1] == double:
                    ahead_group_size = 3
                    ahead_dist = state[1] * 2
                elif state[1] == double * 2:
                    ahead_group_size = 3
                    ahead_dist = state[1]//2
                elif state[1] == double * 4:
                    ahead_group_size = 3
                    ahead_dist = state[1]
                elif ahead_dist > max_reach:
                    ahead_dist = max_reach + 1
            next_state = (ahead_group_size, ahead_dist)
            if next_state not in states_dict:
                max_state_idx += 1
                states_dict[next_state] = max_state_idx
                states_queue.append(next_state)
            if next_state not in transition_dict:
                transition_dict[next_state] = outcome_prob
            else:
                transition_dict[next_state] += outcome_prob
    state_transitions[state] = transition_dict

print(datetime.now(), "Start: Max value of one die =", DIEFACE_MAXVAL)
outcome_prob = Fraction(1, DIEFACE_MAXVAL * DIEFACE_MAXVAL)
max_singles_sum = (2*DIEFACE_MAXVAL) - 1
max_reach = DIEFACE_MAXVAL * 4
diff_dice_probs = dict()
for die1 in range(1, DIEFACE_MAXVAL+1):
    for die2 in range(1, DIEFACE_MAXVAL+1):
        if die1 == die2:
            continue
        die_sum = die1 + die2
        if die_sum in diff_dice_probs:
            diff_dice_probs[die_sum] += outcome_prob
        else:
            diff_dice_probs[die_sum] = outcome_prob

states_dict = dict()
states_dict[(2, max_reach + 1)] = 0
start_state = (5,0)
states_queue = [start_state,]
max_state_idx = 1
states_dict[start_state] = max_state_idx
state_transitions = OrderedDict()
while len(states_queue) > 0:
    calc_transition_probs(states_queue.pop(0))

dim = len(states_dict)
A_mat = zeros(dim, dim)
A_mat[0, 0] = 1
if PRINT_EV_EQUATIONS:
    print("Expected value equations for state transitions:")
for state, transitions in state_transitions.items():
    A_mat[states_dict[state], states_dict[state]] = 1
    if PRINT_EV_EQUATIONS:
        print("E{} = 1".format(state), end=" ")
    for next_state, prob in transitions.items():
        A_mat[states_dict[state], states_dict[next_state]] = prob * -1
        if PRINT_EV_EQUATIONS:
            print("+ ({})E{}".format(prob, next_state), end = " ")
    if PRINT_EV_EQUATIONS:
        print()
e_final = Fraction(1,1)/(Fraction(1,1) - (Fraction(DIEFACE_MAXVAL, 1) * outcome_prob))
if PRINT_EV_EQUATIONS:
    print("E(2, {}) = {}".format(max_reach + 1, e_final))

b_vec = ones(dim, 1)
b_vec[0, 0] = e_final
res = A_mat.inv() * b_vec
print("Expected number of total two-dice rolls when max value of one die is {}: {} / {} , or approx {}".format \
      (DIEFACE_MAXVAL, res[1].numerator, res[1].denominator, round(res[1].numerator/res[1].denominator, 6)))
print("ANSWER: Expected number of two-dice rolls excluding the final, game-ending roll when max value of one die is {}: {} / {} , or approx {}".format \
      (DIEFACE_MAXVAL, res[1].numerator - res[1].denominator, res[1].denominator, round((res[1].numerator - res[1].denominator)/res[1].denominator, 6)))
print(datetime.now(), "done")

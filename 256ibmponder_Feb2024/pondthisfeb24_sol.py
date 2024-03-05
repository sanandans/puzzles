'''
My IBM Ponder This February '24 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/February2024.html
Sanandan Swaminathan, submitted February 1, 2024

The game continues until Alice or Bob wins (one of them will eventually win). The program first calculates the probabilities
for a single round. Then, a system of equations is formulated. In the main puzzle, consider a13 as Alice's probability of
winning the game when both Alice and Bob still have 13 consecutive rounds to win (which is the situation when the game starts
as well as whenever there is a draw). Let a12, a11, ... a2, a1 be Alice's probability of winning the game when Alice has 12,
11, ... 2, 1 consecutive rounds to win (last round was won by Alice). Let b12, b11, ... b2, b1 be Alice's probability of winning
the game when Bob has 12, 11, ... 2, 1 consecutive rounds to win (last round was won by Bob).

a13 = (114399 / 460800) * a12 + (230400 / 460800) * b12 + (116001 / 460800) * a13
This can be rewritten as...
460800*a13 - 114399*a12 - 230400*b12 - 116001*a13 = 0

Similarly,
460800*a12 - 114399*a11 - 230400*b12 - 116001*a13 = 0

And so on...

460800*a2 - 114399*a1 - 230400*b12 - 116001*a13 = 0

460800*a1 - 114399 - 230400*b12 - 116001*a13 = 0 (Alice wins the game if she wins the round when having just 1 round to win).

And...

460800*b12 - 114399*a12 - 230400*b11 - 116001*a13 = 0

460800*b11 - 114399*a12 - 230400*b10 - 116001*a13 = 0

And so on...

460800*b2 - 114399*a12 - 230400*b1 - 116001*a13 = 0

460800*b1 - 114399*a12 - 116001*a13 = 0 (when Bob has just 1 round to win, Alice can win the game only if
she wins the next round or it's a draw).

Such a system of equations can be formulated for the bonus puzzle also, the only differences being the probabilities of Bob winning
a round or a round getting drawn, and the number of equations (25 equations for main puzzle, 599 equations for bonus puzzle).
I use the python sympy module. The program creates the needed sympy symbols (variables) and the equations by looping (25 variables
and equations for the main puzzle, and 599 variables and equations for the bonus puzzle). Then it uses sympy's solve() function to
get the answer, which is the value of a13 for the main puzzle, and the value of a300 for the bonus puzzle.

The program completed instantaneously for the main puzzle, and ran for about 45 seconds to find the bonus * answer.

We could also consider the equations in Ax = b matrix form, and in a loop, set up the A and b matrices, then use numpy's
linalg.solve() or scipy's linalg.solve() to get the answer, or sympy's linear algebra functions. We could also have solved this
using the usual Markov chain by setting up the transition matrix (with two absorbing states - Alice wins the overall game or
Bob wins), then set up the standard QR0I matrix. N matrix = inverse of I - Q. Then relevant cell in N*R matrix will give us the
desired probability. We could also do N time column vector of 1's to get the expected number of tosses for the game to end.

Rather than use the Ax=b or Markov chain way, wanted to try a different way using symbolic math where the equations
themselves are generated programmatically.
'''

from sympy import symbols, solve
from datetime import datetime

print("Start time:", datetime.now())
#set BONUS flag to False to find the answer for the main puzzle, set to True for the bonus * answer
#BONUS flag is the only setting to be toggled to find main or bonus * answers
BONUS = True
N = 13 #main needs 13 consecutive rounds to be won, bonus needs 300 consecutive rounds to be won
if BONUS == True:
    N = 300

#populate number of occurrences of possible sums, min sum 5, max sum 59 with that Dungeons and Dragons dice set,
#where the dice are: d4 (shows numbers 1-4), d6 (shows 1-6), d8 (shows 1-8), d10 (shows 0-9), d12 (shows 1-12), d20 (shows 1-20).
sum_arr = [0]*60
for d4 in range(1,5):
    for d6 in range(1,7):
        for d8 in range(1,9):
            for d10 in range(0,10):
                for d12 in range(1,13):
                    for d20 in range(1,21):
                        sum_arr[d4+d6+d8+d10+d12+d20] += 1
tot_ways = sum(sum_arr)
alice_wins = 0
bob_wins = 0
relevant_primes = {5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59} #dice sums that win a round for Alice
for i in range(5, 60):
    if i in relevant_primes:
        alice_wins += sum_arr[i]
    else:
        #in main puzzle, Bob wins a round if dice sum is nonprime even; in bonus puzzle, with nonprime odd sum
        if (BONUS == False and i%2 == 0) or (BONUS == True and i%2 == 1):
            bob_wins += sum_arr[i]           
draws = tot_ways - alice_wins - bob_wins
print(alice_wins, bob_wins, draws, tot_ways)

#declare the variables (symbols) to be passed to sympy's solve() function, and create a list of those symbols
tempstr = '['
for i in range(N,0,-1):
    exec("a" + str(i) + " = symbols('a" + str(i) + "')")
    tempstr += 'a' + str(i) + ','
for i in range(N-1,0,-1):
    exec("b" + str(i) + " = symbols('b" + str(i) + "')")
    tempstr += 'b' + str(i) + ','
tempstr = tempstr[0:len(tempstr)-1] + ']'
exec("var_list = tempstr") #var_list is the symbols list to be passed to sympy's solve() function

alice_wins_str = str(alice_wins)
bob_wins_str = str(bob_wins)
draws_str = str(draws)
tot_ways_str = str(tot_ways)
#formulate the equations to be solved, and put them in the equations list to be passed to sympy's solve() function
eqs_list = []
for i in range(N,1,-1):
    eqs_list.append(tot_ways_str + '*a' + str(i) + ' - ' + alice_wins_str + '*a' + str(i-1) + ' - ' + bob_wins_str + \
                    '*b' + str(N-1) + ' - ' + draws_str + '*a' + str(N))
eqs_list.append(tot_ways_str + '*a1 - ' + alice_wins_str + ' - ' + bob_wins_str + '*b' + str(N-1) + ' - ' + draws_str + \
                '*a' + str(N))
for i in range(N-1,1,-1):
    eqs_list.append(tot_ways_str + '*b' + str(i) + ' - ' + alice_wins_str + '*a' + str(N-1) + ' - ' + bob_wins_str + \
                    '*b' + str(i-1) + ' - ' + draws_str + '*a' + str(N))
eqs_list.append(tot_ways_str + '*b1 - ' + alice_wins_str + '*a' + str(N-1) + ' - ' + draws_str + '*a' + str(N))

results = solve(eqs_list,var_list, dict=True) #solve the equations to get the desired answer
print("Answer")
if BONUS == False:
    #in main puzzle, we are seeking a13, the probability of Alice winning when both players start with
    #needing 13 consecutive round wins
    answer = [solution[a13] for solution in results]
    print(answer) #this will give exact probability
    print(answer[0].evalf()) #use if desiring an approx answer in float form
else:
    #in bonus puzzle, we are seeking a300, the probability of Alice winning when both players start with
    #needing 300 consecutive round wins
    answer = [solution[a300] for solution in results]
    print(answer) #this will give exact probability
    print(answer[0].evalf()) #use if desiring an approx answer in float form
print("End time:", datetime.now())

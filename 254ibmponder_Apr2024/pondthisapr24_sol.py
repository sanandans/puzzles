'''
My IBM Ponder This April '24 challenge main and bonus * min solutions
(and closed forms for ALL solutions for both)
https://research.ibm.com/haifa/ponderthis/challenges/April2024.html
Sanandan Swaminathan, submitted April 1, 2024

Firstly, an assumption that is not explicitly stated in the puzzle. I assume that the target rod
is fixed w.r.t the initial filled rod; it is the rod immediately clockwise from the initial rod. The
puzzle mentions clockwise-located, but not that the target rod remains the same even after every
winning state. If rods A, B, C are clokwise, with A being initially filled, then B is the target rod.
Once all the disks have moved to B (winning state), I assume the target rod for the next win remains B,
and not rod C which is clockwise adjacent to B.

The program converts the initial state into a base n+1 number. The smallest (topmost) disk is considered
to have a digit value of n, the next disk has a digit value n-1, and so on, with the largest disk having
digit value 1. An empty rod has the value 0. The rods are referenced mod 3. Moving a disk leads to the
source rod's value getting divided by base, and the target rod's value getting multiplied by base and
adding the disk value being moved. I also track where the smallest disk is located at any time. For move
#0 or #1, we can move the smallest disk to the appropriate rod which we can locate with +1 mod 3 or
-1 mod 3 from the current rod holding the smallest disk. For move #2, the program looks at the unit digits
in the clockwise and counter-clockwise rods, and moves the smaller disk (bigger number) among the two to
the other rod.

To find the smallest number of steps when 2 different sized games finish simultaneously (or 3 different games
in the case of the bonus puzzle), the program plays one game until a win, and sets the number of moves as a
goal for the next game to match or exceed. The games get played in a round robin manner with the goal getting
reset (increased) until all games achieve a common goal.

The program completed in 5 seconds for the main puzzle, and took about 10 minutes to find the bonus * answer.
The answers for the main and bonus * puzzles turned out to be 16511310 and 1169723214 respectively.

By tweaking the program, I also generated lists of winning step sequences for n = 7, n = 10, and n = 9 separately.
For n = 7, the wins occur at steps 1404 mod(11178), 1405 mod(11178), 4203 mod(11178), and 4204 mod(11178).
For n = 10, the wins occur at steps 4429 mod(6656) and 4430 mod(6656).

The GCD of 11178 and 6656 is 2. The moduli are not co-prime, but we can use a variant of the Chinese Remainder
Theorem to find ALL solutions for the main puzzle. ALL solutions for the main puzzle seem to be covered by the
following (here, k is any non-negative integer):

37200384k + 16511310
37200384k + 17975629
37200384k + 20538189
37200384k + 20538190

We can see that 16511310 is the minimum number of steps for the main puzzle.

For the bonus * puzzle, n = 9 has considerably more individual solutions:
86943 mod(234009)
86951 mod(234009)
87669 mod(234009)
87670 mod(234009)
145874 mod(234009)
145897 mod(234009)
146164 mod(234009)
146165 mod(234009)
146232 mod(234009)
146233 mod(234009)
146242 mod(234009)
146251 mod(234009)
146252 mod(234009)

The GCD of 37200384 (the modulus for solutions satisfying the main puzzle) and 234009 (the modulus for
solutions satisfying just the n = 9 game) is 243. We can eliminate several combinations to find the combined
solutions. Take remainders mod 243 of the remainders of the four mod 37200384 and thirteen mod 234009
solutions above. Only 4 of the 52 combinations hame matching remainders mod 243, and can have solutions.
Using the Chinese Remainder Theorem variant (for non-co-prime moduli), we can determine that ALL solutions
for the bonus * puzzle are covered by the following (here, k is any non-negative integer):

35823969792k + 1169723214
35823969792k + 10136480077
35823969792k + 17537892174
35823969792k + 26504649037

We can see that 1169723214 is the minimum number of steps for the bonus * puzzle.
'''

from datetime import datetime

'''
Function to find the minimum steps needed that match or exceed a goal number of steps. The goal would
be 0 at the beginning of a game. The goal can be reset by different-sized games.

Parameters:
rods: array of 3 rods, with one of them holding the disks in winning state. Rod 0 has all the disks
at the start of the game. After the first win, the disks are on rod 1, and they are on rod 1 after every
subsequent win. The rods can be accessed mod 3 since they are in a circle.
move_str: The fixed input string for a given game; it contains move instructions 0, 1, 2.
str_pos: Points to the next move.
str_len: Length of input move string.
num_moves: Number of moves done so far for a given game.
min_pos: Tracks the rod number (0, 1, 2) where the smallest disk is currently located.
base: n+1 (the base used to convert the state of the disks into a number)
n: The number of disks in a given game.
target: The target numeric value that the target rod (rod 1) should have to win. When a game first starts,
rod 0 has a value of target.
goal_moves: Total cumulative steps needed to reach a win in a given game should match or exceed the goal.

Return tuple:
num_moves: Total cumulative moves for a given game reached by this function call.
str_pos+1: Where in the input move string the next search for this game should resume.
min_pos: Location of the smallest disk for a given game for the next search.
'''
def get_win_moves(rods, move_str, str_pos, str_len, num_moves, min_pos, base, n, target, goal_moves):
    while True:
        move = move_str[str_pos]
        num_moves += 1
        if move == '0': #move smallest disk clockwise, adjust the values of the two rods
            rods[min_pos] //= base
            min_pos = (min_pos + 1)%3
            rods[min_pos] = (rods[min_pos] * base) + n
            #win matching or exceeding goal
            if min_pos == 1 and rods[min_pos] == target and num_moves >= goal_moves:
                return (num_moves, str_pos+1, min_pos)
        elif move == '1': #move smallest disk counter clockwise, , adjust the values of the two rods
            rods[min_pos] //= base
            min_pos = (min_pos - 1)%3
            rods[min_pos] = (rods[min_pos] * base) + n
            #win matching or exceeding goal
            if min_pos == 1 and rods[min_pos] == target and num_moves >= goal_moves:
                return (num_moves, str_pos+1, min_pos)
        else: #move non-smallest disk, if possible
            cw = (min_pos+1)%3
            acw = (min_pos-1)%3
            tempx = rods[cw]%base
            tempy = rods[acw]%base
            #if disk clockwise from the smallest is smaller than disk counter clockwise,
            #then move smaller disk to the other rod. Vice-versa if the counter clockwise
            #disk is smaller than the clockwise disk. Only the topmost disks need to be compared,
            #which can be done by comparing the unit digits of the numeric values of the rods.
            #Note that "smaller" disk has a bigger number value. Also note that an empty rod has
            #value 0, so it's equivalent to having the largest disk on it.
            if tempx > tempy: #smaller disk on clockwise rod
                rods[cw] //= base
                rods[acw] = (rods[acw] * base) + tempx
            elif tempx < tempy: #smaller disk on counter clockwise rod
                rods[acw] //= base
                rods[cw] = (rods[cw] * base) + tempy
            #no movement of non-smallest disk possible, but the state might be a win state
            #with cumulative steps so far for this game matching or exceeding goal
            elif rods[1] == target and num_moves >= goal_moves:
                return (num_moves, str_pos+1, min_pos)

        #go to the next move instruction; wrap to the start of move string if end reached
        str_pos = (str_pos+1)%str_len

print("Start", datetime.now())
BONUS = False # set to False for main puzzle, True for bonus * puzzle

#initial setup for first game
game0_n = 7 #number of disks for game0
game0_base = game0_n +1 #base to encode the value of the start state/target state
exponent = 0
game0_target = 0 #start state/target state
for disk in range(game0_n, 0, -1):
    game0_target += disk*(game0_base**exponent)
    exponent += 1
game0_rods = [game0_target, 0, 0] #start values of the three rods
game0_move_str = '12021121120020211202121' #given fixed input move string
game0_str_len = len(game0_move_str) #length of given input move string
game0_str_pos = 0 #to track position in the move string
game0_num_moves = 0 #to track number of moves for a given game
game0_min_pos = 0 #to track location of smallest disk

#initial setup for second game
game1_n = 10
game1_base = game1_n +1
exponent = 0
game1_target = 0
for disk in range(game1_n, 0, -1):
    game1_target += disk*(game1_base**exponent)
    exponent += 1
game1_rods = [game1_target, 0, 0]
game1_move_str = '0211202112002'
game1_str_len = len(game1_move_str)
game1_str_pos = 0
game1_num_moves = 0
game1_min_pos = 0

#initial setup for third game (applicable only for the bonus * puzzle)
game2_n = 9
game2_base = game2_n +1
exponent = 0
game2_target = 0
for disk in range(game2_n, 0, -1):
    game2_target += disk*(game2_base**exponent)
    exponent += 1
game2_rods = [game2_target, 0, 0]
game2_move_str = '20202020021212121121202120200202002121120202112021120020021120211211202002112021120211200212112020212120211'
game2_str_len = len(game2_move_str)
game2_str_pos = 0
game2_num_moves = 0
game2_min_pos = 0

goal = 0 #to track the goal number of steps that the simultaneous games are trying to achieve
goal_match_cnt = 0 #shows how many games so far have matched the current goal at a point in time
GOAL_MATCH_TGT = 2 #for main puzzle, two games need to achieve a common goal
if BONUS:
    GOAL_MATCH_TGT = 3 #for bonus * puzzle, three games need to achieve a common goal

progress = 0 #to track and periodically report progress of the program
    
while True:
    if progress%1000 == 0:
        print(datetime.now(), goal, game0_num_moves, game1_num_moves, game2_num_moves)
    progress += 1

    #play game0 with the aim to get a win needing total steps (so far for this game) >= goal steps
    result_tuple = get_win_moves(game0_rods, game0_move_str, game0_str_pos, game0_str_len, game0_num_moves, \
                                 game0_min_pos, game0_base, game0_n, game0_target, goal)
    #save game0 state for future rounds; the rods array would already have the disks on rod 1 after every win
    game0_num_moves = result_tuple[0]
    game0_str_pos = result_tuple[1]
    game0_min_pos = result_tuple[2]
    
    if game0_num_moves == goal: #if exactly the goal steps have been used to reach a win
        goal_match_cnt += 1
        if goal_match_cnt == GOAL_MATCH_TGT: #if goal has been achieved by last run of all games
            print("Answer", game0_num_moves, "Bonus flag:", BONUS)
            break
    else: #reset goal to the total steps taken by this game in this round
        goal = game0_num_moves
        goal_match_cnt = 1

    #play game1 with the aim to get a win needing total steps (so far for this game) >= goal steps
    result_tuple = get_win_moves(game1_rods, game1_move_str, game1_str_pos, game1_str_len, game1_num_moves, \
                                 game1_min_pos, game1_base, game1_n, game1_target, goal)
    #save game1 state for future rounds; the rods array would already have the disks on rod 1 after every win
    game1_num_moves = result_tuple[0]
    game1_str_pos = result_tuple[1]
    game1_min_pos = result_tuple[2]
    if game1_num_moves == goal: #if exactly the goal steps have been used to reach a win
        goal_match_cnt += 1
        if goal_match_cnt == GOAL_MATCH_TGT: #if goal has been achieved by last run of all game
            print("Answer", game1_num_moves, "Bonus flag:", BONUS)
            break
    else: #reset goal to the total steps taken by this game in this round
        goal = game1_num_moves
        goal_match_cnt = 1

    if BONUS: #if bonus game needs to be played
        #play game2 with the aim to get a win needing total steps (so far for this game) >= goal steps
        result_tuple = get_win_moves(game2_rods, game2_move_str, game2_str_pos, game2_str_len, game2_num_moves, \
                                 game2_min_pos, game2_base, game2_n, game2_target, goal)
        #save game2 state for future rounds; the rods array would already have the disks on rod 1 after every win
        game2_num_moves = result_tuple[0]
        game2_str_pos = result_tuple[1]
        game2_min_pos = result_tuple[2]
        if game2_num_moves == goal: #if exactly the goal steps have been used to reach a win
            goal_match_cnt += 1
            if goal_match_cnt == GOAL_MATCH_TGT: #if goal has been achieved by last run of all game
                print("Answer", game2_num_moves, "Bonus flag:", BONUS)
                break
        else: #reset goal to the total steps taken by this game in this round
            goal = game2_num_moves
            goal_match_cnt = 1

print("End", datetime.now())

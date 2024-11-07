'''
My IBM Ponder This October '24 challenge main and bonus * solutions (both complete fast)
https://research.ibm.com/haifa/ponderthis/challenges/October2024.html
Sanandan Swaminathan, submitted October 3, 2024

Search for the main puzzle's answer completes instantaneously, and the search for the
bonus answer completes in about 30 seconds.

Main puzzle's answer (least X containing the digits except 0 and 5 at least once, B being the
product of X's digits, X being a multiple of B, and B being a perfect square):
X = 1817198712146313216 
(A = 1817198712, B = 146313216)

Bonus * puzzle's answer (least X containing all digits except 0 and 5 at least once, B being the
product of X's digits, X being a multiple of B, and digit product of A being a perfect cube):
X =  8419411123272236924928 
(A = 84194111232 B = 72236924928)

Approach for main puzzle:
Since B must at least be the product of 1,2,3,4,6,7,8,9, it must be at least 2^7 x 3^4 x 7.
Since B has to be a perfect square, it must be at least 2^8 x 3^4 x 7^2. The program iterates
through values of B that are of the form 2^(8+x) * 3^(4+y) * 7^(2+z), where x,y,z are each even.
Arbitrary limits are used to bound the search, though the bounds reduce quickly as valid potential
answers are found. 2^(8+x) * 3^(4+y) * 7^(2+z) is also the digit product of X. As valid B's that lead
to a valid X are found, the limit for B gets lower. B is valid if it only has valid digits, and if
those digits can be provided by the 2^(8+x) * 3^(4+y) * 7^(2+z) digit product. The digits seen in B
are marked off, and the reduced portion of X's digit product is used to search for A.

The process for A first provisions the needed digits that are missing in B (if the remaining digit
product allows it). This forms the base string for A. Any remaining 7's in the digit product are added.
With the remaining portions of the powers of 2 and 3, the various combinations of digits are created.
For example, 2^2 * 3^2 would provide combinations like 49, 433, 229, 2233, 66, and 623. These are
appended to the base string, and these strings serve as a set of base candidates for A. Any
candidate string is discarded if the sum of its length and the current B's length exceeds the length
of the current minimum value of X. Zero and more 1's are added progressively depending on the room
left based on the current minimum X's length. For each permutation of each qualifying candidate "A"
string, X is the concatenation of A and B. If X mod B is 0, and if X is smaller than the current
minimum, it becomes the new minimum. As smaller X's are found, the search for B (and A) gets reduced.

Approach for the bonus * puzzle:
We can basically use the same logic and code for the bonus puzzle. The main difference with the main
puzzle is the initial loops to generate B's. Here, A's digit product needs to be 2^(3x) * 3^(3y) * 7^(3z),
and the number B (the digit product of X) has to be 2^(3x+a) * 3^(3y+b) * 7^(3z+c), with the additional
condition that B has to be at least 2^7 * 3^4 * 7 (the product of the digits 1,2,3,4,6,7,8,9). Any B
larger than the current minimum X is discarded. Compared to the main puzzle, there are additional loops
in the driving code. Main needed three variables x,y,z, but bonus needs six: x,y,z,a,b,c. There is an
additional check needed for the bonus puzzle - that the digit product of the resulting number B turns out
to actually be 2^a * 3^b * 3^c. B does not have to be a square in the bonus puzzle. Once the initial code
generates B's, we can simply use the same functions used for the main puzzle.

For both the main and bonus puzzles, we need to be sure that we have found the least X, i.e. there is
no other arrangement of digits that satisfies the conditions and results in a smaller X. The exponents of
2,3,7 are three variables that are varied as we search for a solution for the main puzzle. In the case of
the bonus puzzles, there are six variables that are varied. Also, zero or more 1's are inserted. Hence, the
search doesn't occur in a sequential manner in terms of the length of X. We overcome this obstacle by
assuming that X is at most a certain number of digits (I assumed 25 to start with). If a solution is found,
and we have ensured that we have covered all possible numbers upto that solution, then we are done. If no
solution is found, we can increase the max length that X could be (and adjust the exponent bounds), and try
again. As it turned out, 25 was more than enough as the max possible length of least X. Least X turned out
to be a 19-digit number for the main puzzle, and a 22-digit number for the bonus puzzle. Since we covered
a larger range in both puzzles, we can be sure that we found the least X for both puzzles even though the
searches were not sequential.
'''

from more_itertools import distinct_permutations
from datetime import datetime

'''
Assume that the least X for main puzzle is at most a 25 digit number. If no solution is found,
progressively increase this bound along with increasing EXP_LIM, and try again.
'''
MIN_NUM_LEN = 25 # arbitrary bound; increase if no solution found
MIN_NUM = (10**MIN_NUM_LEN) - 1 # to hold least X found at any given point
BEST_A = -1 # to hold A of least X found at any given point
BEST_B = -1 # to hold B of least X found at any given point
exp_twos = [3,2,1] # exponents of 2 that give valid digits > 1, i.e. 8,4,2
exp_threes = [2,1] # exponents of 2 that give valid digits > 1, i.e. 9,3

'''
Function to create combinations of digits for a power of 2 in digit product.
e.g. 2^3 can give 8, 42, 222.
'''
def recurs_twos_makecomb(exp_two, inp_str, str_set):
    if exp_two == 0:
        str_set.add("".join(sorted(inp_str)))
        return
    for i in exp_twos:
        if i <= exp_two:
            recurs_twos_makecomb(exp_two - i, inp_str + str(2**i), str_set)
    return

'''
Function to create combinations of digits for a power of 3 in digit product.
e.g. 3^4 can give 99, 933, 3333.
'''
def recurs_threes_makecomb(exp_three, inp_str, str_set):
    if exp_three == 0:
        str_set.add("".join(sorted(inp_str)))
        return
    for i in exp_threes:
        if i <= exp_three:
            recurs_threes_makecomb(exp_three - i, inp_str + str(3**i), str_set)
    return

'''
Function to create combinations of digits with at least one 6 for a combo power of 2
and 3 in digit product.
e.g. 2^3 * 3^3 can give 666, 6623, 649, 6433, 6229, 62233 (not including combos
containing no 6, which are handled by other functions).
'''
def six_makecomb(exp_two, exp_three, inp_str, str_set):
    max_sixes = min(exp_two, exp_three)
    for sixes in range(max_sixes, 0, -1):
        tempstr = inp_str
        for i in range(sixes):
            tempstr += "6"
        rem_two = exp_two - sixes
        rem_three = exp_three - sixes
        if rem_two > 0 and rem_three > 0:
            tempset1 = set()
            recurs_twos_makecomb(rem_two, tempstr, tempset1)
            for item in tempset1:
                recurs_threes_makecomb(rem_three, item, str_set)
        elif rem_two > 0 and rem_three == 0:
            recurs_twos_makecomb(rem_two, tempstr, str_set)
        elif rem_two == 0 and rem_three > 0:
            recurs_threes_makecomb(rem_three, tempstr, str_set)
        elif rem_two == 0 and rem_three == 0:
            str_set.add("".join(sorted(tempstr)))
    return

'''
Function to create the base string containing necessary digits that
have not been seen. Check is done to ensure that the digit product
actually allows the digit to be added.
'''
def make_startstr(dict_pf, dict_digits):
    tempstr = ""
    for key, val in dict_digits.items():
        if not val:
            if key == 1:
                tempstr += "1"
            elif key in (2,3,7):
                if dict_pf[key] > 0:
                    tempstr += str(key)
                    dict_pf[key] -= 1
                else:
                    return (False, "")
            elif key == 4:
                if dict_pf[2] > 1:
                    tempstr += str(key)
                    dict_pf[2] -= 2
                else:
                    return (False, "")
            elif key == 8:
                if dict_pf[2] > 2:
                    tempstr += str(key)
                    dict_pf[2] -= 3
                else:
                    return (False, "")
            elif key == 9:
                if dict_pf[3] > 1:
                    tempstr += str(key)
                    dict_pf[3] -= 2
                else:
                    return (False, "")
            elif key == 6:
                if dict_pf[2] > 0 and dict_pf[3] > 0:
                    tempstr += str(key)
                    dict_pf[2] -= 1
                    dict_pf[3] -= 1
                else:
                    return (False, "")
    for i in range(0, dict_pf[7]):
        tempstr += "7"
    return (True, tempstr)

'''
Function to create all possible base strings without adding free 1's
'''
def base_perms(dict_pf, dict_digits, str_set):
    res, tempstr = make_startstr(dict_pf, dict_digits)
    if not res:
        return False
    if dict_pf[2] > 0 and dict_pf[3] > 0:
        str_set1 = set()
        recurs_twos_makecomb(dict_pf[2], tempstr, str_set1)
        for item in str_set1:
            recurs_threes_makecomb(dict_pf[3], item, str_set)
        six_makecomb(dict_pf[2], dict_pf[3], tempstr, str_set)
    elif dict_pf[2] > 0 and dict_pf[3] == 0:
        recurs_twos_makecomb(dict_pf[2], tempstr, str_set)
    elif dict_pf[2] == 0 and dict_pf[3] > 0:
        recurs_threes_makecomb(dict_pf[3], tempstr, str_set)
    elif dict_pf[2] == 0 and dict_pf[3] == 0:
        str_set.add("".join(sorted(tempstr)))
    return True

'''
Function to mark seen digits, and also to check if the number
violates the digit product.
'''
def process_digits(num, pf_dict, dig_dict):
    while num > 0:
        dig = num%10
        if dig == 0 or dig == 5:
            return False
        dig_dict[dig] = True
        if dig == 2 or dig == 3 or dig == 7:
            if pf_dict[dig] > 0:
                pf_dict[dig] -= 1
            else:
                return False
        elif dig == 4:
            if pf_dict[2] > 1:
                pf_dict[2] -= 2
            else:
                return False
        elif dig == 8:
            if pf_dict[2] > 2:
                pf_dict[2] -= 3
            else:
                return False
        elif dig == 9:
            if pf_dict[3] > 1:
                pf_dict[3] -= 2
            else:
                return False
        elif dig == 6:
            if pf_dict[2] > 0 and pf_dict[3] > 0:
                pf_dict[2] -= 1
                pf_dict[3] -= 1
            else:
                return False
        num //= 10
    return True

'''
Function that looks for an "A" that works, given "B", the remaining digit
product, and the missing digits.
'''
def search_sol(B, dict_pf, dict_digits):
    global MIN_NUM, MIN_NUM_LEN, BEST_A, BEST_B
    B_LEN = len(str(B))
    str_set = set()
    if base_perms(dict_pf, dict_digits, str_set):
        for st in sorted(list(str_set), key=int):
            EXIST_LEN = B_LEN + len(st)
            round = 0
            sol_found = False
            while round <= MIN_NUM_LEN - EXIST_LEN:
                tempstr = st
                for dig_one in range(0,round):
                    tempstr += "1"
                for dig_perm in distinct_permutations(tempstr):
                    A = ''.join(dig_perm)
                    X = int(A + str(B))
                    if X%B == 0 and X < MIN_NUM:
                        sol_found = True
                        MIN_NUM = X
                        MIN_NUM_LEN = len(str(MIN_NUM))
                        BEST_A = int(A)
                        BEST_B = B
                        print(datetime.now(), "NEW MIN FOUND: X =", X, "A =", A, \
                              "B =", B, "X length =", MIN_NUM_LEN)
                if sol_found: #don't need to append any more 1's for this base string
                    break
                round += 1

'''
Function to re-verify the solution against the various constraints of the main and bonus
puzzles.
'''
def verify_sol(x, a, b, bonus_flag):
    dig_dict = {1:False, 2:False, 3:False, 4:False, 6:False, 7:False, 8:False, 9:False}
    pf_dict = {2:0, 3: 0, 7:0}
    digit_product = 1
    num = a
    while num > 0:
        dig = num%10
        if dig == 0 or dig == 5:
            return False
        dig_dict[dig] = True
        digit_product *= dig
        if dig == 2 or dig == 3 or dig == 7:
            pf_dict[dig] += 1
        elif dig == 4:
            pf_dict[2] += 2
        elif dig == 8:
            pf_dict[2] += 3
        elif dig == 9:
            pf_dict[3] += 2
        elif dig == 6:
            pf_dict[2] += 1
            pf_dict[3] += 1
        num //= 10
    if bonus_flag:
        for val in pf_dict.values():
            if val%3 != 0:
                return False
    num = b
    while num > 0:
        dig = num%10
        if dig == 0 or dig == 5:
            return False
        dig_dict[dig] = True
        digit_product *= dig
        if dig == 2 or dig == 3 or dig == 7:
            pf_dict[dig] += 1
        elif dig == 4:
            pf_dict[2] += 2
        elif dig == 8:
            pf_dict[2] += 3
        elif dig == 9:
            pf_dict[3] += 2
        elif dig == 6:
            pf_dict[2] += 1
            pf_dict[3] += 1
        num //= 10
    if not bonus_flag:
        for val in pf_dict.values():
            if val%2 != 0:
                return False
    if b != digit_product:
        return False
    if x%b != 0:
        return False
    if str(a) + str(b) != str(x):
        return False
    for val in dig_dict.values():
        if not val:
            return False
    return True

print(datetime.now(),"Start main puzzle")
LOG_STEP = 10**8 # iterations before printing log
'''
EXP_LIM bounds the (even) exponents of 2,3,7 in the prime factorization of
square number B. We assume X is at most a 25-digit number, and 2^82 has
25 digits while 2^84 has 26 digits. If no solution found, we should increase
the bound for X and hence EXP_LIM also.
3^82 and 7^82 are greater than 25 digit numbers, so 82 is more than safe as
an exponent bound to find least X if it is indeed at most a 25 digit number.
If no solution found for main puzzle, we should increase MIN_NUM_LEN and EXP_LIM,
and try again.
'''
EXP_LIM = 83 # arbitrary bound; increase if no solution found
progress = 0 # progress counter
'''
Product of required digits is 2^7 * 3^4 * 7, but B is a square
number, so min B is 2^8 * 3^4 * 7^2.
'''
for x in range(8, EXP_LIM, 2):
    B_x = 2**x
    for y in range(4, EXP_LIM, 2):
        B_y = B_x * (3**y)
        for z in range(2, EXP_LIM, 2):
            progress += 1
            if progress%LOG_STEP == 0:
                print(datetime.now(),progress)
            B = B_y * (7**z)
            if B > MIN_NUM:
                break
            dict_pf_B = {2:x, 3:y, 7:z}
            dict_digits = {1:False, 2:False, 3:False, 4:False, 6:False, 7:False, \
                           8:False, 9:False}
            if process_digits(B, dict_pf_B, dict_digits):
                search_sol(B, dict_pf_B, dict_digits)

if BEST_A == -1:
    print(datetime.now(),progress, \
          "No main solution found; increase MIN_NUM_LEN and EXP_LIM, and try again")
else:
    if verify_sol(MIN_NUM, BEST_A, BEST_B, False):
        print("Main puzzle: Least X =", MIN_NUM, "A =", BEST_A, "B =", BEST_B, \
              "X length =", MIN_NUM_LEN)
        print(datetime.now(),progress, "Ended main, starting bonus...")
    else:
        print(datetime.now(),progress, "Error verifying main, starting bonus.")

#resetting starting values and limits for bonus run

'''
Assume that the least X for bonus puzzle is at most a 25 digit number. If no solution is found,
progressively increase this bound along with increasing BONUS_A_EXP_LIM and BONUS_B_EXP_LIM, and
try again.
'''
MIN_NUM_LEN = 25 # arbitrary bound; increase if no solution found
MIN_NUM = (10**MIN_NUM_LEN) - 1 # to hold least X found at any given point
BEST_A = -1 # to hold A of least X found at any given point
BEST_B = -1 # to hold B of least X found at any given point
progress = 0 # progress counter
'''
In bonus puzzle, A's digit product is of the form 2^(3x) * 3^(3y) * 7^(3z), and B would
be of the form 2^(3x+a) * 3^(3y+b) * 7^(3z+c).
Assuming X is indeed at most a 25 digit number, the most the exponent of 2 in the
digit product of A could be is 75. This would be 25 8's though that would leave no room
for B. So, we can safely cap the exponents in the search for A at 75.
Exponent limit for 3 would really be 50 (25 9's), and 25 for 7 (25 7's). So, 75 is a more
than safe exponent limit for 3 and 7.
If no solution found for bonus, we should increase MIN_NUM_LEN, BONUS_A_EXP_LIM and
BONUS_B_EXP_LIM, and try again.
'''
BONUS_A_EXP_LIM = 76 # arbitrary bound; increase if no minimum found
'''
BONUS_B_EXP_LIM bounds the exponents of 2,3,7 in the prime factorization of B.
We assume X is at most a 25-digit number, and 2^83 has 25 digits while 2^84 has 26 digits.
3^83 and 7^83 are greater than 25 digit numbers, so 83 is more than safe as
an exponent bound to find least X if it is indeed at most a 25 digit number.
If no solution found for bonus, we should increase MIN_NUM_LEN, BONUS_A_EXP_LIM and
BONUS_B_EXP_LIM, and try again.
'''
BONUS_B_EXP_LIM = 84 # arbitrary bound; increase if no minimum found
'''
Digit product of A needs to be a perfect cube, hence increment exponents
of 2,3,7 in jumps of 3.
'''
for x in range(0, BONUS_A_EXP_LIM, 3):
    a_st = max(x,7)
    for y in range(0, BONUS_A_EXP_LIM, 3):
        b_st = max(y,4)
        for z in range(0, BONUS_A_EXP_LIM, 3):
            c_st = max(z,1)
            for a in range(a_st, BONUS_B_EXP_LIM-x):
                B_a = 2**a
                for b in range(b_st, BONUS_B_EXP_LIM-y):
                    B_b = B_a * (3**b)
                    for c in range(c_st, BONUS_B_EXP_LIM-z):
                        progress += 1
                        if progress%LOG_STEP == 0:
                            print(datetime.now(),progress)
                        B = B_b * (7**c)
                        if B > MIN_NUM:
                            break
                        dict_pf_B = {2:a, 3:b, 7:c}
                        dict_digits = {1:False, 2:False, 3:False, 4:False, 6:False, 7:False, \
                                       8:False, 9:False}
                        if process_digits(B, dict_pf_B, dict_digits):
                            #the remaining prime fac of B should be the digit product of A
                            if dict_pf_B[2] == x and dict_pf_B[3] == y and dict_pf_B[7] == z:
                                search_sol(B, dict_pf_B, dict_digits)

if BEST_A == -1:
    print(datetime.now(),progress, \
          "No bonus solution found; increase MIN_NUM_LEN, BONUS_A_EXP_LIM and BONUS_B_EXP_LIM, and try again")
else:
    if verify_sol(MIN_NUM, BEST_A, BEST_B, True):
        print("Bonus puzzle: Least X =", MIN_NUM, "A =", BEST_A, "B =", BEST_B, \
              "X length =", MIN_NUM_LEN)               
        print(datetime.now(),progress, "Ended bonus.")
    else:
        print(datetime.now(),progress, "Error verifying bonus.")

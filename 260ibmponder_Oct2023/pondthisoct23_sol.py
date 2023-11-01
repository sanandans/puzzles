'''
My IBM Ponder This October '23 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/October2023.html
Sanandan Swaminathan, submitted October 2, 2023

Brute force gets ruled out pretty quickly. Firsly, such a brute force puzzle would be pointless; they wouldn't pose it.
It's a needle in a haystack with a brute force search; a short run with n starting at 845 and increasing by
1201 in each iteration doesn't give an answer through billions. I looked for existing research on this topic and found a nice
paper at https://oeis.org/A002778/a002778_1.pdf. The Binary, Ternary and Even Root families get ruled out as the base number
needs to be a non-palindrome. Looking for "sporadic square palindromes" seemed to be too expensive a brute force search to start with,
even with n constrained to 845(mod 1201). So, I decided to look for a solution in the "Asymmetric Root Family", where the base number
is guaranteed to be a non-palindrome by construction. In this family, a base number n is of the form 1(x)0[9]9[0]1(x')1, clearly non-palindromic,
with [9] representing zero or more 9's, [0] representing the same number of 0's as 9's, (x) representing a string of 1's and
0's of length at least one and containing exactly one or two 1's, and (x') representing the reverse of the (x) string.
The square of such a number is NOT guaranteed to be a palindrome. I looped through increasing lengths of [9] upto 5 (with the
same length for [0]), and increasing lengths of (x) upto 30 (and hence (x')). After checking whether the number n is
845(mod 1201), I check whether the resulting square is a palindrome. My program completed immediately for the main puzzle.
It reported n = 10001000100000000000999900010000000000100010001 as a number that meets the desired conditions.

For the bonus "*" problem, n has to be 1599376 (mod 4281565) by the Chinese Remainder Theorem. I tried searching for a solution
under the Asymmetric Root Family as I did for the main puzzle. I tried with lengths of the substrings [9] (and hence [0]), and
(x) (and hence (x')), upto 200 each. This didn't give an answer for the bonus. To test much larger numbers, like beyond 800 digit long
numbers, I had to tweak my program. I was using bitwise operators and shifting to generate the (x) and (x') substrings, but
the string operations naturally get slow with numbers of very large lengths. So I changed my program to eliminate
string operations. I use appropriate additions and subtractions to generate the numbers in a sequence for increasing lengths
of [9], [0], (x) and (x'). My program still ran for about 35 minutes to find an answer for the bonus * puzzle...

n =  1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009999999999999999999999999999999999999999999
999999999999999999999999999999999999999999999999999999999999999999999999999990000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000001

The above 953-digit number n is not a palindrome, and it is 845 (mod 1201) and also 2256 (mod 3565). Its 1905-digit square
is a palindrome

Regarding the open question posed in the puzzle, an answer can't exist in the Binary, Ternary and Even Root families. It
can't exist in the Asymmetric Root Family which has root numbers in the form 1(x)0[9]9[0]1(x')1; this has at least one 0 digit
to the immediate left of [9]. So, if such a non-palindromic root number with only odd digits exists, it can only be one from
the "sporadic" family. Looking through the list of discovered sporadic square palindromes and their roots at worldofnumbers.com,
there isn't one there. Searching for larger sporadics with non-palindromic root with all odd digits and palindromic square
is expensive - a needle in a haystack. A way doesn't jump out to mathematically prove that a non-palindromic number with only
odd digits can never produce (or, less likely, can produce) a square palindrome. It's a nice open question.

'''
from datetime import datetime

def isPalNum(n):
    x = str(n)
    strl = len(x)
    for i in range(0,strl//2):
        if x[i] != x[strl-1-i]:
            return False
    return True

#For main, ran with NINES_LIM = 5 and X_LIM = 30. For bonus, ran with NINES_LIM = 501 and X_LIM = 501.
#Comment/uncomment two mod checking lines in code depending on main/bonus run
NINES_LIM = 501 #ran with 5 for main, 501 for bonus
X_LIM = 501 #ran with 30 for main, 501 for bonus
found = False
'''
n is of the form 1(x)0[9]9[0]1(x')1,
with [9] representing zero or more 9's, [0] representing the same number of 0's as 9's, (x) representing a string of 1's and
0's of length at least one and containing exactly one or two 1's, and (x') representing the reverse of the (x) string.
Smallest such n would be 1109111. We can keep building n's by fattening the middle [9]9[0] portion, and using appropriate
additions and subtractions to fatten the (x) and (x') portions for a given [9]9[0].
'''
mid_num = 0
mid_addend = 9
for num_nines in range(0,NINES_LIM): #progressively fatten the middle portion of n
    #middle portion will progressively be 9, 990, 99900...
    mid_num = (mid_num*100)+mid_addend
    mid_addend *= 10
    if num_nines%10 == 0: #progress check
        print(datetime.now(), num_nines)
    x_right1_exp = (2*num_nines) + 5 # length of the 0[9]9[0]1(x')1 portion
    snum = (11*(10**x_right1_exp)) + (mid_num*1000) + 110 #number of form 11099900110, for example
    msd_addend = 9*(10**(x_right1_exp+1)) #to move the msd 1 to the left
    x_right1_addend = 9*(10**x_right1_exp) #to move the rightmost 1 of (x) to the left
    xp_left1_subtract = 9 #to move the leftmost 1 of (x') to the right
    
    for x_len in range(1, X_LIM): #progressively fatten the (x) and (x') portions of n
        x_right1_addend_tmp = x_right1_addend
        xp_left1_subtract_tmp = xp_left1_subtract
        basenum = snum + 1 #add the lsd 1
        for right_one in range(0, x_len): #move the rightmost 1 of (x) to left; move leftmost 1 of (x') to right

            #for bonus puzzle, n needs to be 1599376 mod 4281565 by Chinese Remainder Theorem, but faster to check
            #845 mod 1201 and 2256 mod 3565 individually ("and" operation has short-circuiting)
            
            #if basenum%1201 == 845 and isPalNum(basenum**2) == True: #for main puzzle
            if basenum%1201 == 845 and basenum%3565 == 2256 and isPalNum(basenum*basenum) == True: #for bonus puzzle
                print("answer:", basenum)
                print("answer length:", len(str(basenum)))
                print("square palindrome:", basenum**2, "length of square palindrome:", len(str(basenum**2)))
                found = True
                break

            #now that we've checked with a single 1 at some position in (x), check with a second 1 somewhere to its left in (x).
            #Note that the reverse portion (x') also has to be adjusted in sync
            x_left1_start_val = (x_right1_addend_tmp//9)*10 #second 1 starts to the immediate left of the rightmost 1 in (x)
            x_left1_addend = 9*x_left1_start_val #to move the left 1 of (x) to the left
            xp_right1_start = xp_left1_subtract_tmp//9 #second 1 starts to the immediate right of the leftmost 1 in (x')
            xp_right1_subtract = xp_left1_subtract_tmp//10 #to move the rightmost 1 of (x') to the right
            basenum1 = basenum + x_left1_start_val + xp_right1_start #adjust n due to the moves in (x) and (x')
            for left_one in range(right_one+1, x_len): #move the leftmost 1 of (x) to left; move rightmost 1 of (x') to right

                #if basenum1%1201 == 845 and isPalNum(basenum1**2) == True: #for main puzzle
                if basenum1%1201 == 845 and basenum1%3565 == 2256 and isPalNum(basenum1*basenum1) == True: #for bonus puzzle
                    print("answer:", basenum1)
                    print("answer length:", len(str(basenum1)))
                    print("square palindrome:", basenum1**2, "length of square palindrome:", len(str(basenum1**2)))
                    found = True
                    break
                basenum1 += x_left1_addend - xp_right1_subtract #adjust n due to the moves in (x) and (x')
                #set up for next iteration with relatively inexpensive operations for large n
                x_left1_addend *= 10
                xp_right1_subtract //= 10
            if found == True:
                break
            basenum = basenum + x_right1_addend_tmp - xp_left1_subtract_tmp #adjust n due to the moves in (x) and (x')
            #set up for next iteration with relatively inexpensive operations for large n
            x_right1_addend_tmp *= 10
            xp_left1_subtract_tmp //= 10
        if found == True:
            break
        snum = (snum + msd_addend)*10 #(x) and (x') are expanding, so move msd 1 to the left and also extend n on the right end
        #set up for next iteration with relatively inexpensive operations for large n
        msd_addend *= 100
        x_right1_addend *= 10
        xp_left1_subtract *= 10
    if found == True:
        break
print(datetime.now())

'''
#first pass, using bitwise operators and string handling; fast for main puzzle, not fast enough for bonus search

for num_nines in range(0,NINES_LIM):
    print(datetime.now(), num_nines)
    middle_str = "0" + ("9" * (num_nines + 1)) + ("0" * num_nines)
    for x_len in range(0, X_LIM):
        lead_one = 2**(x_len)
        x = 1
        xrev = 2**(x_len-1)
        for one_pos_x in range(0, x_len):
            full_str = bin(x | lead_one)[2:] + middle_str + bin(((xrev | lead_one) << 1) | 1)[2:]
            basenum = int(full_str)
            if basenum%1201 == 845 and isPalNum(basenum*basenum) == True:
            #if basenum%1201 == 845 and basenum%3565 == 2256 and isPalNum(basenum*basenum) == True:
                print(basenum, basenum*basenum, len(str(basenum)))
                found = True
                break
            x <<= 1
            xrev >>= 1
        if found == True:
            break
        xrev_init = 2**(x_len-1)
        for second_one in range(1, x_len):
            x = (2**second_one) | 1
            xrev = (2**(x_len-1-second_one)) | xrev_init
            for shift_num in range(0, x_len-second_one):
                full_str = bin(x | lead_one)[2:] + middle_str + bin(((xrev | lead_one) << 1) | 1)[2:]
                basenum = int(full_str)
                if basenum%1201 == 845 and isPalNum(basenum*basenum) == True:
                #if basenum%1201 == 845 and basenum%3565 == 2256 and isPalNum(basenum*basenum) == True:
                    print(basenum, basenum*basenum, len(str(basenum)))
                    found = True
                    break
                x <<= 1
                xrev >>= 1
            if found == True:
                break
        if found == True:
            break
    if found == True:
        break
print(datetime.now())
'''


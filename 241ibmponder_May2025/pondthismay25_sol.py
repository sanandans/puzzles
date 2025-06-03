'''
My IBM Ponder This May '25 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/May2025.html
Sanandan Swaminathan, submitted April 30, 2025

For the main puzzle, the correct answers for the ten multiple-choice questions are DADBDDCDBC. This can be
quickly deduced from just the last three worksheets, making the other 5 worksheets redundant for the main
puzzle. The last 3 worksheets are:
Worksheet X) DDDBDDCDBD 8/10
Worksheet Y) DADBDDCCCC 8/10
Worksheet Z) CADBDDDDAC 7/10

Let the questions be numbered Q1-Q10. From worksheets X and Y (which scored 8 each), we see that it must
be the case that correct answers for Q1=D, Q3=D, Q4=B, Q5=D, Q6=D, Q7=C. These are the matches in X and Y.
If one of them was incorrect, X and Y can each afford only 1 other wrong answer from the remaining 4
questions where their answers don't match. But if X got exactly one of them wrong, then Y got the other 3
wrong. Hence, Q1=D, Q3=D, Q4=B, Q5=D, Q6=D, Q7=C. Worksheet Z has Q1 and Q7 wrong, so can have only one
other wrong answer. If answer for Q2 is not A, then answers for the last three questions are D,A,C for
worksheet Z to score 7. But then, worksheet Y would have three wrong answers (Q2, Q8, Q9), and cannot have
a score of 8. Thus, Q2=A. If answer for Q8 is not D, then the answers for Q9 and Q10 have to be A and C for
worksheet Z to score 7. But then, worksheet X would have Q2, Q8, Q9 and Q10 wrong, and cannot score 8. Thus,
Q8=D. If answer for Q9 is A, then Q10=D for worksheet X to score 8. But then, worksheet Y would have Q8, Q9
and Q10 wrong, and would not score 8. Thus, Q9 is not A, and Q10 must be C for worksheet Z to score 7. This
means that Q9 = B for worksheet X to score 8. Thus, the correct answers are DADBDDCDBC.

For the bonus puzzle which doesn't have worksheets scoring high percentages, and has 21 questions rather than
10, such an analysis to manually deduce the correct answers for the MC questions is much more convoluted. Hence
I wrote a recursive function to determine the correct answers for the MC questions. Of course, it gives the same
result for the main puzzle as deduced manually above. The backtracking function progresses through the worksheets
in order of high scores to low scores. It starts with a top scoring student, and tries different combinations
of correct answers that would give him his score (the remaining being incorrect answers). It then proceeds to
the next student, and if required, chooses more correct answers, subject to what has already been assumed to be
correct/incorrect. It backtracks when a violation is detected. When the recursion has satisfied all student scores
successfully, we get the string of correct answers for all the MC questions. It turns out to be ACBADBADDDDCBBDCBACCC
for the bonus puzzle (and DADBDDCDBC for the main puzzle).

Once the correct MC answers have been found, we can proceed to the next step, noting that all arithmetic has to be
done modulo p since we are working over prime field Fp (which has elements 0 to p-1) aka Galois finite field GF(p^1).
Note that p would be greater than the largest correct answer among the ten MC questions (which turns out to be 7624).
We can use the first 8 "addition modulo p" equations given since there are 8 variables, x1 to x8. Matrix A is a fixed
8x8 matrix containing the LHS coefficients of the first eight "addition mod p" equations. Matrix b is a fixed 8x1 vector
containing the correct answer values for the first eight equations. The program iterates through prime numbers greater
than the lower bound for p to solve Ax = b (mod p) for each p until a valid list of x's that works for all 10 equations
(including the last two "prodyct mod p" equations) is found. Hence it solves x = ((mod p inverse of A) * b) mod p. If
the eight x values found work for the last two "product modulo p" equations, an answer has been found. The program
completed instantaneously, and reported p = 8999, and the x1 to x8 values as  (2, 5, 7, 13, 269, 331, 353, 1409).

For the bonus puzzle, we have to determine the 20 coefficients a19, a18... a1, a0 of the monic polynomial q(x) (a20 = 1).
A 20x20 matrix, A, is set up for this using the first 20 equations (by substituting the x powers progressively from lower
to higher powers, with all arithmetic in modulo p = 8999). Another matrix b is set up as a vector containing the correct
multiple-choice answers for those 20 questions (reduced by the value of x^20 for each given x, mod p = 8999, since that
is a constant from the perspective of each equation containing the unknowns a19, a18... a1, a0). It then solves
coeffs = ((mod 8999 inverse of A) * b) mod 8999. Here, "coeffs" denotes the vector containing the polynomial's 20 unknown
coefficients a19, a18... a1, a0. Taking the sum of these coefficients plus 1 (coefficient of the x^20 term), modulo p = 8999,
gives us the value of q(1) as 3898 in F_8999. The given 21st question q(4529) = 5503 is also satisfied. The program completed
in about 40 seconds for the bonus puzzle.
'''

from itertools import combinations
from copy import deepcopy
import sympy as sp
from datetime import datetime

#backtracking recursive function to find correct answers for MC questions
def recurs_find_mc_answers(student, curr_corrects, curr_wrongs):
    if student == NUM_STUDENTS:
        return (True, curr_corrects)
    rem_marks = worksheets[student][1]
    potential_new_corrects = []
    for i in range(NUM_QUESTIONS):
        if curr_corrects[i] is None:
            if worksheets[student][0][i] not in curr_wrongs[i]:
                potential_new_corrects.append(i)
        elif curr_corrects[i] == worksheets[student][0][i]:
            rem_marks -= 1
            if rem_marks < 0:
                return (False, curr_corrects)
    if rem_marks > len(potential_new_corrects):
        return (False, curr_corrects)
    elif rem_marks == 0:
        for i in potential_new_corrects:
            curr_wrongs[i].add(worksheets[student][0][i])
            if len(curr_wrongs[i]) == 3:
                for answer in ('A','B','C','D'):
                    if answer not in curr_wrongs[i]:
                        curr_corrects[i] = answer
                        break
        return recurs_find_mc_answers(student+1, curr_corrects, curr_wrongs)

    for comb in combinations(potential_new_corrects, rem_marks):
        new_curr_corrects = deepcopy(curr_corrects)
        new_curr_wrongs = deepcopy(curr_wrongs)
        for i in potential_new_corrects:
            if i in comb:
                new_curr_corrects[i] = worksheets[student][0][i]
            else:
                new_curr_wrongs[i].add(worksheets[student][0][i])
                if len(new_curr_wrongs[i]) == 3:
                    for answer in ('A','B','C','D'):
                        if answer not in new_curr_wrongs[i]:
                            new_curr_corrects[i] = answer
                            break
        ret = recurs_find_mc_answers(student+1, new_curr_corrects, new_curr_wrongs)
        if ret[0]:
            return ret
    return (False, curr_corrects)

#function used to call recursive function to determine correct answers to MC questions
def find_mc_answers():
    current_corrects = [None]*NUM_QUESTIONS
    current_wrongs = [None]*NUM_QUESTIONS
    for i in range(NUM_QUESTIONS):
        current_wrongs[i] = set()
    worksheets.sort(key=lambda x: x[1], reverse=True)
    ret = recurs_find_mc_answers(0, current_corrects, current_wrongs)
    corrects_str = ""
    for ans in ret[1]:
        corrects_str += ans
    for worksheet in worksheets:
        marks = 0
        for i in range(NUM_QUESTIONS):
            if worksheet[0][i] == corrects_str[i]:
                marks += 1
        if marks != worksheet[1]:
            print("ERROR: marks not matching in worksheet ", worksheet)
    return corrects_str

#just to ensure that recurion did its job correctly
def verify_marks():
    for worksheet in worksheets:
        marks = 0
        for question in range(NUM_QUESTIONS):
            if worksheet[0][question] == corrects_str[question]:
                marks += 1
        if marks != worksheet[1]:
            print("ERROR in marks", corrects_str, worksheet, marks)

#calclulating polynomial value for given x value using Horner's rule method
def calc_polynomial_horner_rule(x_val):
    res = 1 #leading coeff a20
    for i in range(NUM_QUESTIONS - 2, -1, -1):
        res = (res*x_val)%p
        res = (res + coeffs[i])%p
    return res

#just raw mod p calculation of polynomial value
def calc_polynomial_field_arithmetic(x_val):
    res = coeffs[0]
    x_pow = 1
    for i in range(1, NUM_QUESTIONS-1):
        x_pow = (x_pow * x_val)%p
        res = (((coeffs[i]*x_pow)%p) + res)%p
    x_pow = (x_pow * x_val)%p
    res = (x_pow + res)%p
    return res

#verify that the prime p found indeed satisfies all the equations of the main puzzle
def verify_main_field_arithmetic(x_vector, p_num):
    for i in range(NUM_QUESTIONS-2):
        res = 0
        for j in range(NUM_QUESTIONS-2):
            res = (((A[i,j]*x[j])%p_num) + res)%p_num
        if res != b[i]:
            print("ERROR in addition equation", i)
        temp = (((x_vector[0]*x_vector[2])%p)*x_vector[4]%p)*x_vector[6]%p_num
        if temp != answer_choices[9][corrects_str[9]]:
            print("ERROR in product equation 9")
        if (((((temp*x_vector[1]*x_vector[3])%p)*x_vector[5])%p)*x_vector[7])%p != answer_choices[8][corrects_str[8]]:
                print("ERROR in product equation 8")

#verify that the coefficients found for the bonus puzzle indeed give the desired polynomial values for all the given x values
def verify_bonus_horner_rule(answer):
    for i in range(NUM_QUESTIONS-1):
        if calc_polynomial_horner_rule(x_vals[i]) != answer_choices[i][corrects_str[i]]:
            print("ERROR in equation:", i)
    if calc_polynomial_horner_rule(x_vals[NUM_QUESTIONS-1]) != answer_choices[NUM_QUESTIONS-1][corrects_str[NUM_QUESTIONS-1]]:
        print("ERROR in equation:", NUM_QUESTIONS-1)
    if calc_polynomial_horner_rule(1) != answer:
        print("ERROR in q(1)")

#verify with raw mod p arithmetic that the coefficients found for the bonus puzzle indeed give the desired polynomial values
def verify_bonus_field_arithmetic(answer):
    for i in range(NUM_QUESTIONS-1):
        if calc_polynomial_field_arithmetic(x_vals[i]) != answer_choices[i][corrects_str[i]]:
            print("ERROR in equation:", i)
    if calc_polynomial_field_arithmetic(x_vals[NUM_QUESTIONS-1]) != answer_choices[NUM_QUESTIONS-1][corrects_str[NUM_QUESTIONS-1]]:
        print("ERROR in equation:", NUM_QUESTIONS-1)
    if calc_polynomial_field_arithmetic(1) != answer:
        print("ERROR in q(1)")
        
print(datetime.now(), "start main puzzle")
#the 8 worksheets given in the main puzzle with student responses and corresponding marks
worksheets = [("BABBDDCDCA", 6), ("DADBDDAACD", 6), ("CADBDBCDCC", 7),\
              ("DACBDDCBCB", 6), ("DCBBDDCDAB", 6), ("DDDBDDCDBD", 8),\
              ("DADBDDCCCC", 8), ("CADBDDDDAC", 7)]
NUM_STUDENTS = len(worksheets)
NUM_QUESTIONS = len(worksheets[0][0])
corrects_str = find_mc_answers()
verify_marks()
print(datetime.now(), "Correct answers to MC questions:", corrects_str)

#the multiple-choice options given in the main puzzle
answer_choices = [{'A': 2416, 'B': 2415, 'C': 2413, 'D': 2412}, \
                  {'A': 7624, 'B': 7622, 'C': 7621, 'D': 7625}, \
                  {'A': 638, 'B': 642, 'C': 633, 'D': 637}, \
                  {'A': 765, 'B': 761, 'C': 759, 'D': 760}, \
                  {'A': 2211, 'B': 2212, 'C': 2217, 'D': 2216}, \
                  {'A': 3497, 'B': 3501, 'C': 3496, 'D': 3499}, \
                  {'A': 4007, 'B': 4010, 'C': 4008, 'D': 4013}, \
                  {'A': 5531, 'B': 5535, 'C': 5538, 'D': 5534}, \
                  {'A': -4, 'B': 1, 'C': 5, 'D': 4}, \
                  {'A': 6544, 'B': 6546, 'C': 6545, 'D': 6550}]
b_arr = []
for i in range(NUM_QUESTIONS-2):
    b_arr.append(answer_choices[i][corrects_str[i]])
p = max(max(b_arr), max(answer_choices[NUM_QUESTIONS-2][corrects_str[NUM_QUESTIONS-2]], \
                        answer_choices[NUM_QUESTIONS-1][corrects_str[NUM_QUESTIONS-1]]))
if p%2 == 0:
    p += 1
b = sp.Matrix(b_arr)
#the LHS coefficients of the first 8 "addition mod p" equations given in the main puzzle
A = sp.Matrix([[0,5,7,0,5,3,0,0], [8,5,0,0,2,0,0,5], [7,4,0,5,2,0,0,0],\
            [7,0,9,0,0,1,1,0], [0,0,8,7,4,3,0,0], [0,0,2,5,0,5,5,0],\
            [0,5,0,4,6,7,0,0], [0,0,7,1,0,8,8,0]])
while True:
    if not sp.isprime(p):
        p += 2
        continue
    x = (A.inv_mod(p)*b) % p
    temp = x[0]*x[2]*x[4]*x[6]
    if temp%p == answer_choices[9][corrects_str[9]] and \
       (temp*x[1]*x[3]*x[5]*x[7])%p == answer_choices[8][corrects_str[8]]:
        print("Values of x1 to x8:", tuple(x))
        print(datetime.now(), "******** ANSWER for main puzzle: p =", p, "********")
        verify_main_field_arithmetic(x, p)
        break
    p += 2

print(datetime.now(), "end main puzzle, start bonus")
#the 11 worksheets given in the bonus puzzle with student responses and corresponding marks
worksheets = [("CCCDDCAADCCCBBDABDBAD", 9), ("ADDACCADDDDBACDDBADCD", 11), \
              ("DCBABBAADDACBBAAAABDC", 12), ("ACAAABABDDDBACAABADDC", 11), \
              ("CABAAAABDBDCCBDCBDBCC", 12), ("DDDADCADDBDABBDBCADCC", 12), \
              ("ACDBBDAADDDABDCBCBCAC", 9), ("AABCBDACDBADBDDCDACCB", 10), \
              ("BABBBBABAABCBDBCDACCA", 9), ("ACCBABADDDDDBBCDDBACC", 12), \
              ("ACDBCBBDBDDCBCCADBCAA", 9)]
NUM_STUDENTS = len(worksheets)
NUM_QUESTIONS = len(worksheets[0][0])
corrects_str = find_mc_answers()
verify_marks()
print(datetime.now(), "Correct answers to bonus MC questions:", corrects_str)

#the multiple-choice options given in the bonus puzzle
answer_choices = [{'A': 5146, 'B': 5142, 'C': 5149, 'D': 5147}, \
                  {'A': 3715, 'B': 3725, 'C': 3720, 'D': 3716}, \
                  {'A': 2547, 'B': 2548, 'C': 2549, 'D': 2550}, \
                  {'A': 6624, 'B': 6628, 'C': 6619, 'D': 6627}, \
                  {'A': 4661, 'B': 4660, 'C': 4659, 'D': 4662}, \
                  {'A': 5112, 'B': 5107, 'C': 5106, 'D': 5102}, \
                  {'A': 3916, 'B': 3921, 'C': 3913, 'D': 3917}, \
                  {'A': 2340, 'B': 2342, 'C': 2345, 'D': 2344}, \
                  {'A': 6210, 'B': 6212, 'C': 6217, 'D': 6215}, \
                  {'A': 3642, 'B': 3644, 'C': 3646, 'D': 3641}, \
                  {'A': 1581, 'B': 1584, 'C': 1586, 'D': 1583}, \
                  {'A': 6543, 'B': 6536, 'C': 6541, 'D': 6544}, \
                  {'A': 3823, 'B': 3828, 'C': 3824, 'D': 3832}, \
                  {'A': 5601, 'B': 5598, 'C': 5602, 'D': 5595}, \
                  {'A': 1272, 'B': 1274, 'C': 1278, 'D': 1275}, \
                  {'A': 4410, 'B': 4420, 'C': 4415, 'D': 4412}, \
                  {'A': 8974, 'B': 8973, 'C': 8976, 'D': 8971}, \
                  {'A': 6723, 'B': 6720, 'C': 6728, 'D': 6721}, \
                  {'A': 8244, 'B': 8247, 'C': 8246, 'D': 8243}, \
                  {'A': 1571, 'B': 1570, 'C': 1569, 'D': 1568}, \
                  {'A': 5504, 'B': 5501, 'C': 5503, 'D': 5506}]
b_arr = []
for i in range(NUM_QUESTIONS-1):
    b_arr.append(answer_choices[i][corrects_str[i]])
#the x values given in the 21 MC questions in the bonus puzzle
x_vals = (5698, 1616, 1338, 7821, 4461, 2156, 7559, 5812, 794, 2595, 1640, 6779, \
          8362, 4605, 420, 8724, 3669, 1869, 7516, 1386, 4529)
A_arr = []
for i in range(NUM_QUESTIONS-1):
    temp_arr = []
    temp_arr.append(1) #for a0 coeff
    val = x_vals[i]
    temp_arr.append(val) #for a1 coeff
    for j in range(NUM_QUESTIONS-3):
        val = (val * x_vals[i])%p
        temp_arr.append(val)
    A_arr.append(temp_arr)
    b_arr[i] = (b_arr[i] - ((val * x_vals[i])%p))%p
A = sp.Matrix(A_arr)
b = sp.Matrix(b_arr)
coeffs = (A.inv_mod(p)*b) % p
if calc_polynomial_horner_rule(x_vals[NUM_QUESTIONS-1]) != answer_choices[NUM_QUESTIONS-1][corrects_str[NUM_QUESTIONS-1]]:
    print("ERROR: bonus polynomial does not give desired answer for last equation")
else:
    ans = (sum(coeffs)+1)%p
    print(datetime.now(), "******** ANSWER for bonus puzzle: q(1) =", ans, "********")
    verify_bonus_horner_rule(ans)
    verify_bonus_field_arithmetic(ans)

poly_str = "x^20 "
for i in range(NUM_QUESTIONS-2, 1, -1):
    poly_str += "+ " + str(coeffs[i]) + "x^" + str(i) + " "
poly_str += "+ " + str(coeffs[1]) + "x + " + str(coeffs[0])
print("Monic polynomial q(x) =", poly_str)

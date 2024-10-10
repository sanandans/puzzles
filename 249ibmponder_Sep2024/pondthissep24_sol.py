'''
My IBM Ponder This September '24 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/September2024.html
Sanandan Swaminathan, submitted August 30, 2024

My first (inefficient) thought for the main puzzle was as follows:
To get 50 sibling pairs, with a > b, we must have a > b >= 51. Let c and d be the integer side
lengths of the side with different lengths in the two triangles with c < d (called c1 and c2 in the
puzzle). For a sibling pair of triangles (a,b,c) and (a,b,d) with c < d, by applying the cosine law,
we have...
c^2 = a^2 + b^2 - 2ab(cosC).
d^2 = a^2 + b^2 - 2ab * cos of (pi - C) = a^2 + b^2 + 2ab(cosC).
Here, uppercase C is the angle between side lengths a and b in the (a,b,c) triangle. The angle
between side lengths a and b in the (a,b,d) triangle would be pi - C since the two triangles must
have the same height with side length a as the base and side length b as the other common-length
side (for the sibling triangles to have the same area).

Adding the equations, we get c^2 + d^2 = 2(a^2 + b^2). Let n = 2(a^2 + b^2). We can use Jacobi’s
two-square theorem to determine the number of integer solutions of the Diophantine equation
c^2 + d^2 = n though Jacobi’s formula includes signed numbers and flipped pairs. The number might
also include solutions that aren’t feasible for a triangle. E.g., in the example provided in the
puzzle, Jacobi/Diophantine would indicate that (24, 23, 1) and (24, 23, 47) is a sibling pair of
triangles though they are degenerate triangles (and we need sibling pairs to have a common nonzero
area). For this puzzle, using the Jacobi two-square theorem, the number of positive divisors of n
that are 1mod4 must exceed the number of positive divisors of n that are 3mod4 by at least 100. We
could keep increasing "a", and for each "a", vary "b". If the number of positive divisors of n for a
given (a, b) is at least 100, we can check if the 1mod4 divisors exceed the 3mod4 divisors by at least
100. We can stop checking divisors as soon as we determine that either the target of 100 cannot be
reached or the target is guaranteed to be achieved. If the number of divisors of n that are 1mod4
exceeds the number that are 3mod4 by at least 100, we can use the sympy diophantine function to get
the actual set of solutions for the Diophantine equation c^2 + d^2 - n = 0. This set would include
signed and flipped pairs, and side lengths that don’t work for a triangle. We can count the number of
feasible solutions, and we are done if exactly 50 valid sibling pairs are found. Otherwise, continue
searching with different (a,b).

Though the above process would be a short piece of code, clearly it's not efficient. And we could be
looking for a needle in a haystack depending on how big the first (a,b) that solves the problem is.
This could be especially non-performant for the bonus problem if we need to keep finding many
solutions having exactly 50 sibling pairs just to hope to find one solution that happens to have at
least two sibling pairs of triangles with integer areas.

My second approach for the main puzzle makes the search for an (a,b) pair having exactly 50 sibling
pairs instantaneous (and is just a dozen lines of code; see below under "main puzzle"). This allows us
to quickly generate as many solutions as desired. To achieve this, I use the sum of squares function
rather than the Jacobi two-square theorem. For details about the sum of squares function, refer to
equation 17 (number of positive integer pairs satisfying c^2 + d^2 = n) at
https://mathworld.wolfram.com/SumofSquaresFunction.html. The idea is to use the sum of squares function
in a reverse manner, so to speak - build n such that the formula will give the desired number of pairs.
Note that we are not just looking for 50 positive integer (c,d) pairs that satisfy the Diophantine
equation c^2 + d^2 = n, but we need each of those (c,d) pairs to satisfy the triangle inequality with
(a,b) as well. A general Diophantine solution with 50 postive integer pairs could have several pairs
that don't satisfy the triangle inequality. The trick is to build n such that it gives 51 positive
integer pairs including a "special" pair that forces the other 50 pairs to satisfy the triangle
inequality.

My algorithm for the main puzzle using the sum of squares function is as follows:
a) To generate exactly 50 sibling pairs (without caring about integer areas), pick n = 2(a^2 + b^2)
such that the prime factorization of n has no 3mod4 prime factors, and the exponent+1 of 1mod4
prime factors multiply to 102. Technically, n can have even powers of 3mod4 prime factors, but they
don't play a real role in our solution (except scaling the answer). Hence, we can just avoid 3mod4 prime
factors in the prime factorization of n that we are building. With even product (102) of exponent+1
of 1mod4 prime factors, we can afford to have any power of 2 (if needed) in the prime factorization of
n without a bad impact to the end result (though there would be scaling, which doesn't hurt us). So,
we would include 2 as a prime factor of n if we need n to be an even number for our procedure.
For example, the two square function guarantees that n = 2 * (5**16) * (13**2) * 17 would give exactly
(17*3*2)/2 = 102/2 = 51 postive integer pairs for the Diophantine equation c^2 + d^2 = n. The reason
to get exactly 51 pairs (and not 50 as needed by the problem) will become clear below. I included 2 as
a prime factor of n to ensure that n is even (for a reason that will become clear below).

b) Having picked a suitable n like 2*(5**16)*(13**2)*17 that will give exactly 51 (c,d) positive integer
pairs, solve the actual Diophantine equation c^2 + d^2 = n. Take only the positive integer (c, d) pairs
with c < d. Keep track of the pair having the highest value of d.

c) The pair with the highest value of d can be considered as a "special" pair (a-b, a+b) due to the
fact that (a-b)^2 + (a+b)^2 = 2(a^2 + b^2) = n. Having the (a-b, a+b) pair, we simply get the pair
(a, b) by doing (a+b) + (a-b) and (a+b) - (a-b) to get 2a and 2b, hence (a, b). This is an answer for
the main puzzle, so no programming is needed except to solve the Diophantine equation. Note that n had
a prime factor of 2 above. This was done to ensure that (a, b) is an integer pair. The remaining 50 (c, d)
pairs are the exact 50 pairs we wanted since all of them satisfy c^2 + d^2 = n. Notice that, for each of
those 50 sibling pairs, it is guaranteed that c > a - b, and d < a + b, since the (a-b, a+b) pair itself
was set aside to determine (a, b), and a+b was the highest d among the 51 pairs (equivalently, a-b was the
lowest c). Thus, the triangle inequality is satisfied by (a,b) with all the 50 (c,d) pairs. The (a-b, a+b)
pair would itself only create degenerate triangles (zero area) of (a,b,a-b) and (a,b,a+b), hence we have
found exactly 50 sibling pairs of triangles with integer side lengths (a,b,c) and (a,b,d).

For the main puzzle, with n = 2*(5**16)*(13**2)*17, we instantaneously get an answer:
a = 14921875 , b = 14687500. This gives exactly 50 sibling pairs (though all of them have irrational areas,
thus not satisfying the additional constraint for the bonus *). We can generate as many solutions for the
main puzzle as desired just by picking different 1mod4 primes to build the prime factorization of n,
keeping the product of their exponent+1 as 102. Note that, while we can keep generating answers endlessly,
my above algorithm doesn't generate some possible answers, for example, answers with small values of (a,b)
like (26537, 24616).

Though solutions with exactly 50 sibling pairs can be generated at will with my above algorithm, it is
clear that searching for an answer for the bonus problem is still like looking for a (much smaller) needle
in a (much bigger) haystack. Even by generating solutions with exactly 50 sibling pairs, it could take
forever to hit a set where at least two sibling pairs happen to have integer areas. A different line of
attack was needed. Here's the approach I came up with for the bonus puzzle. It completes the bonus search
instantaneously.

a) Look for an (x, y) integer pair (x > y) such that it gives two sibling pairs having integer areas
(i.e. Heronian integer triangles). This part of the program immediately reported (409, 123) as such an (x,y)
pair. Also, note that the prime factorization of 2*(409^2 + 123^2) is (2^2) * 5 * 17 * 29 * 37.

b) Let n = 2(a^2 + b^2). A sibling pair would satisfy c^d + d^2 = n. The number of positive integer
solutions for this can be controlled by using 1mod4 prime powers in the prime factorization of n. We can
use n = 2*(409^2 + 123^2) = (2^2) * 5 * 17 * 29 * 37 as a reference to quickly find a solution for the
bonus * problem.

c) If (a,b) = (409, 123), we get only two valid sibling pairs of triangles (areas for both are integers).
We can scale the pair of (409, 123) by any integer (but avoid odd powers of 3mod4 prime factors though we can
simply avoid 3mod4 prime factors altogether). Scaling (a,b) = (409, 123) up, we would naturally increase the
number of sibling pairs. The two sibling pairs with integer areas will clearly still have integer areas. Of
course, as we scale up (a,b) = (409, 123), we might get more than 50 valid sibling pairs. A bit of adjustment
in the scaling factor quickly achieves the objective of getting exactly 50 sibling pairs.
Setting a = 409 * (13^9), b = 123 * (13^9) achieves the desired result for the bonus problem.

Thus, with slightly different approaches for the main and bonus problems, both can be aolved instantaneously.
For the main puzzle, we really only need to find the special pair (a-b, a+b) that satisfies the Diophantine
equation (we don't care about what the other 50 (c,d) pairs are), so we could technically find it by
hand/calculator, but the numbers are large (use Gaussian integers method?). For the bonus, finding by hand a
pair like (409, 123) that gives two sibling pairs having integer areas would be tedious. Of course, solving
the bonus problem solves the main problem too, so we really wouldn't need the algorithm for the main problem
at all if we solved the bonus problem first.

Note: sympy's general diophantine solver function or the specific sum_of_squares function can be used for
this problem, but sum_of_squares is not fast enough for large numbers. Hence, the general diophantine solver
function is mostly used below.

'''

import math
from datetime import datetime
import sympy
from sympy.solvers.diophantine import diophantine
from sympy.abc import c,d,e,f
from sympy.solvers.diophantine.diophantine import sum_of_squares
'''
from sympy.solvers.diophantine.diophantine import power_representation
from sympy.solvers.diophantine.diophantine import diop_general_sum_of_squares
from sympy.solvers.diophantine.diophantine import diop_general_sum_of_even_powers
'''

CHECK_ANS = False #use for main puzzle if verifying solution
PAIR_TARGET = 50 #exactly 50 sibling pairs needed
INT_AREA_TARGET = 2 #bonus puzzle needs at least two sibling pairs to have integer areas

#use for main puzzle if verifying solution
def check_main_sol(a, b, n):
    sol_pairs = set()
    #for the given (a,b), check all possible values of c
    for c in range(a-b+1, a+b):
        c_sq = c*c
        d = math.isqrt(n - c_sq)
        if ((d*d) + c_sq) == n:
            if c < d:
                sol_pairs.add((c,d))
            elif c > d:
                sol_pairs.add((d,c))
    if len(sol_pairs) != PAIR_TARGET:
        print("ERROR: Found sibling pairs not matching target count", len(sol_pairs), a, b, n)
        return False
    for pair in sol_pairs:
        #for Heron's area formula, compute s(s-a)(s-b)(sic) for sibling pair sides
        heron_c = (a+b+pair[0])*(b+pair[0]-a)*(a+pair[0]-b)*(a+b-pair[0])
        heron_d = (a+b+pair[1])*(b+pair[1]-a)*(a+pair[1]-b)*(a+b-pair[1])
        if heron_c != heron_d:
            print("ERROR: Sibling pair not having equal area", a, b, n, pair)
            return False
    return True

#used to verify number of integer areas for bonus problem
def count_integer_areas(a, b, sol_list, cmin, cmax):
    integer_area_cnt = 0
    for pair in sol_list:
        #for Heron's area formula, compute s(s-a)(s-b)(sic) for sibling pair sides
        x = (a+b+pair[0])*(b+pair[0]-a)*(a+pair[0]-b)*(a+b-pair[0])
        temp = math.isqrt(x)
        if temp*temp == x and temp%4 == 0:
            integer_area_cnt += 1
    return integer_area_cnt

#main puzzle
print(datetime.now(), "Start main puzzle")
'''
Reverse engineer the sum of squares function to formulate n.
n is set such that its prime factorization has 1mod4 prime factors whose (exponent + 1)
multiply to 102; n is made even so that the (a,b) pair turns out to be integers.
We could use any 1mod4 prime factors; just using the smallest ones here.
'''
n = 2*(5**16)*(13**2)*17 #this will give exactly 51 pairs, one of which will lead to (a.b)
sol_set = diophantine(c**2 + d**2 - n) #solve the Diophantine equation
max_absum = 0 # a+b
min_abdiff = 0 # a-b
for pair in sol_set:
    #determine the (a-b, a+b) pair; Diophantine solver gives signed and flipped pairs, so skip them
    if pair[0] > 0 and pair[1] > 0 and pair[0] < pair[1] and pair[1] > max_absum:
        max_absum = pair[1]
        min_abdiff = pair[0]
a = (max_absum + min_abdiff)//2
b = (max_absum - min_abdiff)//2
print(datetime.now(), "An answer found for main puzzle: a =", a, ", b =", b)
if CHECK_ANS and check_main_sol(a, b, n): #if independent verification of the answer is desired
    print(datetime.now(), "Answer verified for main puzzle: a =", a, "b =", b)

#bonus puzzle
print(datetime.now(), "Start bonus puzzle")
ab_double_heronian = False
a = 1
'''
Find an (x,y) pair such that it causes at least two sibling pairs [(x,y,c1), (x,y,d1)] and
[(x,y,c2), (x,y,d2)], where both pairs have integer areas.
'''
while True:
    for b in range(1, a):
        c_min = a - b + 1 #third side of triangle needs to be longer than a-b
        c_max = a + b - 1 #third side of triangle needs to be shorter than a+b
        asq_bsq = a**2 + b**2
        temp = math.sqrt(asq_bsq)
        c_stop = int(temp) #we only need to look until angle between a and b is acute
        if temp.is_integer():
            c_stop -= 1
        for c in range(c_min, c_stop+1):
            n = asq_bsq*2
            d = math.sqrt(n - (c*c))
            if d.is_integer() and d > c and d <= c_max: #qualifies as sibling pair
                if math.gcd(math.gcd(a,b),c) == 1: #primitive Heronian integer triangle
                    #for Heron's area formula, compute s(s-a)(s-b)(sic) for sibling pair sides
                    temp = (a + b + c)*(a + b - c)*(a - b + c)*(b + c -a)
                    temp1 = math.isqrt(temp)
                    if temp1*temp1 == temp: #heronian integer triangle
                        #find all positive int solutions for c^2 + d^2 = n
                        sol_set = list(sum_of_squares(n, 2))
                        cnt = 0
                        for pair in sol_set:
                            #if valid for a triangle
                            if pair[0] >= c_min and pair[1] <= c_max and \
                               (pair[0]**2 + pair[1]**2) == n:
                                radical = (a + b + pair[0])*(a + b - pair[0])* \
                                          (a - b + pair[0])*(b + pair[0] -a)
                                radical1 = math.isqrt(radical)
                                if radical1*radical1 == radical: #heronian triangle
                                    cnt += 1
                                    if cnt == INT_AREA_TARGET:
                                        print(datetime.now(), \
                                              "a,b with >= 2 heronian sibling pairs found:", \
                                              a, b, "count", cnt)
                                        print("Prime factorization:", \
                                              sympy.ntheory.factorint((a**2 + b**2)*2))
                                        ab_double_heronian = True
                                        break
                        if ab_double_heronian:
                            break 
        if ab_double_heronian:
            break
    if ab_double_heronian:
            break
    a += 1

'''
Use the pair found above to set (a,b) which is an answer for the bonus puzzle. Scale (a,b)
such that we will get exactly 50 sibling pairs.
Scaling the (409, 123) result found above by 13**9 gives exactly 50 sibling pairs. Since
(a,b) = (409,123) gave two valid sibling pairs with integer areas, the scaled (a,b) will also
have at least 2 of the 50 sibling pairs having integer areas.
'''
a=409*(13**9)
b=123*(13**9)
n = (a**2 + b**2)*2
print(n, sympy.ntheory.factorint(n))
#for some reason, sympy's diophantine needs fresh variables; reusing c and d doesn't work here
sol_set = diophantine(e**2 + f**2 - n)
print(len(sol_set))
sibling_pair_cnt = 0
integer_area_cnt = 0
cmin = a - b + 1 #third side of triangle needs to be longer than a-b
cmax = a + b - 1 #third side of triangle needs to be shorter than a+b
sol_list = []
for pair in sol_set:
    #if valid triangle
    if pair[0] > 0 and pair[1] > 0 and pair[0] < pair[1] and pair[0] >= cmin and pair[1] <= cmax:
        sol_list.append(pair)
        sibling_pair_cnt += 1
        #for Heron's area formula, compute s(s-a)(s-b)(sic) for sibling pair sides
        temp = (a+b+pair[0])*(b+pair[0]-a)*(a+pair[0]-b)*(a+b-pair[0])
        temp1 = math.isqrt(temp)
        if temp1*temp1 == temp:
            if temp1%4 == 0: #if integer area
                integer_area_cnt += 1
                print('('+str(a)+', '+str(b)+', '+str(pair[0])+') and', \
                      '('+str(a)+', '+str(b)+', '+str(pair[1])+'),', \
                      'INTEGER area = '+str(temp1//4))
        '''
        #uncomment block if interested in printing sibling pairs having irrational areas
        else:
            print('('+str(a)+', '+str(b)+', '+str(pair[0])+') and', \
                  '('+str(a)+', '+str(b)+', '+str(pair[1])+'),', \
                  'IRRATIONAL area = (1/4) * sqrt('+str(temp)+')')
        '''
        #for Heron's area formula, compute s(s-a)(s-b)(sic) for sibling pair sides
        heron_d = (a+b+pair[1])*(b+pair[1]-a)*(a+pair[1]-b)*(a+b-pair[1])
        if temp != heron_d:
            print("ERROR: Sibling pair not having equal area", a, b, n, pair)
print(count_integer_areas(a, b, sol_list, cmin, cmax)) #recheck count of int areas
if sibling_pair_cnt == PAIR_TARGET and integer_area_cnt >= INT_AREA_TARGET:
    print(datetime.now(), "Answer verified for bonus puzzle: a =", a, ", b =", b, \
          "Number of sibling pairs:", sibling_pair_cnt, "Number of int areas:", integer_area_cnt)

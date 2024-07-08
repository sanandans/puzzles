'''
My IBM Ponder This June '24 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/June2024.html
Sanandan Swaminathan, submitted May 31, 2024

Euclid's triplet of (m^2 + n^2, m^2 - n^2, 2mn), where m > n, forms Pythagorean
triples. We need the ratio of the legs of the right triangle to be close to pi,
so we can set A/B = 2mn / (m^2 - n^2) = pi. Dividing numerator and denominator
by m^2, and setting x = n / m (so, 0 < x < 1), we get 2x / (1 - x^2) = pi.
Solving for x, we get x = (sqrt(pi^2 + 1) - 1) / pi. Since we need m and n to
form a Pythagorean triple, we need to approximate the irrational x (0 < x < 1)
by a rational fraction. I used the standard Farey technique to determine a pair
of m and n that works. The m and n values determine the Pythagorean triple.
Mainly, care had to be taken to ensure that the precision requirement was met,
and that the hypotenuse length wasn't exceeding 100 digits. I used the mpmath
package for the high precision requirement (even python decimal package doesn't
seem to provide arbitrary precision for floats).

The program completed instantantaneously for both the main and bonus * problems.
Of course, there are multiple solutions (infinite if the numbers didn't have the
100 digit restriction). The answers I submitted were:
One answer for Main puzzle ( Absolute difference < 10^(-20) ):
A = 13516735201388600982504
B = 4302510443530442460103
C = 14184982432881130228825

One answer for Bonus * puzzle ( Absolute difference < 10^(-95) ):
D = 7890091373031185054301288866929686910913538068187536764898417259494553500244722111241471584035148
E = 2511494086929265181023294797407931343582808418461204839452053493484857390154619575834833445830765
F = 8280165724395967329461233162970946908593310137164630940116369341148756474617092331911169833837877
'''
from mpmath import *
from datetime import datetime

PREC = 96 # precision > 20 for main (go with 21), > 95 for bonus * (go with 96)
MAXDIGITS = 100

#Standard Farey mediant technique to get rational number as close as desired to the given
#irrational, with the denominator of the rational capped as needed.
#We could also use continued fraction technique.
def getRationalFarey(floatnum, max_denom):
    mp.dps = PREC
    num1 = 0
    denom1 = 1
    num2 = 1
    denom2 = 1
    while True:
        if denom1 > max_denom or denom2 > max_denom:
            break
        numer_sum = num1 + num2
        denom_sum = denom1 + denom2
        med = mpf(numer_sum)/mpf(denom_sum) #mediant between the two fractions
        if floatnum == med: #if rational match to the irrational found
            if denom_sum <= max_denom:
                return (numer_sum, denom_sum)
            elif denom1 >= denom2:
                return (num1, denom1)
            else:
                return (num2, denom2)
        elif floatnum <= med: #narrow down by pulling fraction on right to mediant
            num2 = numer_sum
            denom2 = denom_sum
        else: #advance the fraction on left to mediant
            num1 = numer_sum
            denom1 = denom_sum
    #if exact match to given precision not found upto denominator limit,
    #return last good numerator and denominator
    if denom1 <= max_denom:
        return (num1, denom1)
    else:
        return (num2, denom2)

print("Starting", datetime.now(), "Precision =", PREC)
mp.dps = PREC
mypi = +pi

#solution of 2mn/(m^2 - n^2) = pi with x = n/m, m > n
x = mpf(mpf((mypi*mypi + 1)**0.5) - 1) / mpf(mypi)
#convert the irrational x to a rational fraction that is sufficiently close
n, m = getRationalFarey(x, 10**(MAXDIGITS//2)) #cap the denominator given the 100 digit restriction

#Pythagorean triple (A,B,C) from Euclid's ((m^2 + n^2), (m^2 - n^2), 2mn) triple 
A = 2*m*n
B = m**2 - n**2
C =  m**2 + n**2 #hypotenuse of the right triangle

#(A,B,C) is guaranteed to be a Pythagorean triple thanks to Euclid, but check anyway
if A**2 + B**2 == C**2:
    print("Checked: It is a Pythagorean Triple")

#only hypotenuse C needs to be checked to ensure it's 100 digits or less, but check all anyway
if len(str(C)) <= MAXDIGITS and len(str(A)) <= MAXDIGITS and len(str(B)) <= MAXDIGITS:
    print("Checked: All side lengths <=", MAXDIGITS, "digits")

#print key stuff so that precision can be verified with independent tools
ab_ratio = mpf(A)/mpf(B)
print("A/B ratio =", end = " ")
nprint(ab_ratio, PREC)
print("Pi value  =", end = " ")
nprint(mypi, PREC)
diff = abs(ab_ratio - mypi)
print("Absolute Diff between A/B and pi (upto precision) =", end = " ")
nprint(diff, PREC)
threshold = mpf(10**(1-PREC))
print("Diff between 10**(-(PREC-1)) and |A/B - pi| (upto precision) =", end = " ")
nprint(threshold - diff, PREC)
if diff < threshold:
    print("Checked: gap is fine")

#print the Pythagorean triple in the desired format
print("\nANSWER:")
print("A =",A)
print("B =",B)
print("C =",C)

print("\nDone", datetime.now())

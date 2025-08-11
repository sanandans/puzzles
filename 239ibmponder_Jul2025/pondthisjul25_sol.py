'''
My IBM Ponder This July '25 challenge solution
https://research.ibm.com/haifa/ponderthis/challenges/July2025.html
Sanandan Swaminathan, submitted July 20, 2025

The recursion to find the expected number of swallows when no more can fit is immediately clear:
Let E(x) be the expected number of swallows on a wire of length x, eventually. If the left edge of the first
swallow lands at y (from the left end of the wire), then we have sub problems with wires of length y on the
left and of length x-(y+1) on the right since those parts of the wire are empty. The left edge of the first
swallow can land between 0 and x-1 from the left end of the wire. So, we get...
E(x) = 1 + integral (y from 0 to x-1) of [ E(y)dy/(x-1) + E(x-y-1)dy/(x-1) ]
By symmetry of the distribution on the left and right, we can see that...
E(x) = 1 + integral (y from 0 to x-1) of 2E(y)dy/(x-1)
E(x) = 1 + (2/(x-1)) * integral (y from 0 to x-1) of E(y)dy

So, to find E(x) for some x, we need to find the area under the curve until x-1.

Clearly, E(x) = 0 for x between 0 and 1, and E(x) = 1 for x between 1 and 2.
For x between 2 and 3, we can integrate piecewise...
E(x) = 1 + (2/(x-1)) * integral (y from 0 to 1) of 0dy + (2/(x-1)) * integral (y from 1 to x-1) of 1dy
E(x) = 1 + [(2/(x-1)) * (x-2)] = (3x-5)/(x-1) for x in the interval (2,3)

We can evaluate the integral for x between 3 and 4 as well (using piecewise integration for 0 to 1 where E(y)=0,
1 to 2 where E(y)=1, and 2 to x-1 where E(y) = (3y-5)/(y-1) as shown above), but beyond the (3,4) interval it gets
messy. But we can use numerical integration and other numerical methods to get the answers for L1 and L2 to some
degree of approximation. We just need to take sufficiently thin slices to calculate area under the curve, and store
function values from the previous unit interval. We can store the history in a rolling fashion. I tried scipy's
quadrature integration, mpmath's quad, and also raw Riemann sums with thin rectangles and trapezoids. I also tried
by taking the derivative approach (a DDE aka delayed differential equation, not an ordinary differential equation
aka ODE)...
E(x) = 1 + (2/(x-1)) * integral (y from 0 to x-1) of E(y)dy
E(x) * (x-1) = (x-1) + 2 * integral (y from 0 to x-1) of E(y)dy
By differentiaing and applying the fundamental theorem of calculus and using the basic definition of derivative...
E(x) + (x-1)(E(x+h) - E(x))/h = 1 + 2E(x-1).
Rearranging, we get E(x+h) in terms of E(x), E(x-1), x and h.
Making h really small, like h = 10^(-9), we can progressively build E(x+h) values based on E(x) and E(x-1), for
example for x in the intervals (3,4), (4,5), etc. We only need to store 10^9 old values from the previous interval,
and the immediately preceding value, and keep a rolling storage as we move forward. I also did the calculations
using C++ with GMP mpf_class. But with different precision packages and techniques,I was getting slightly different
answers (usually differing at the 7th or 8th after the decimal point). I wondered if a power series approximation
that would build on power series for previous intervals recursively could be tried since the piecewise E(x) function
is easily convertible to a power series for x in the (2, 3) interval. However, I couldn't formulate a a general way
to set up successive power series for different intervals until I chanced upon a nice paper at:
https://www.researchgate.net/publication/265716047_Numerical_Solution_of_Some_Classical_Differential-Difference_Equations

This paper has a clever way to set up the power series for successive intervals; the derivation is easy to understand.
It seems this recursive integral function we are dealing with is the "Renyi function" (turns out it's related to a
"Renyi parking problem" which deals with random sequential adsorption). This paper also has clever tricks to accurately
solve other DDE's like Dickman's function and Buchstab function (which could pop up in a future puzzle). My program
below first sets up the rational coefficients of the power series centered at 2.5, which can quickly be determined,
as follows:
First, let f(x) = E(x) + 1
For x in (2,3), E(x) = (3x-5)/(x-1) as shown before...
So, f(x) = ((3x-5)/(x-1)) + 1
f(x) = 4 - (2/(x-1))
Let x = 2 + 1/2 + z/2. Here, z ranges between -1 and 1.
f(x) = 4 - 2/(3/2 + z/2) = 4 - (4/3)/(1 - (-z/3))
The latter is an infinite geometric series, with common ratio -z/3 whose abs value < 1. So the power series form
for f(x) where x is in the (2,3) interval is...
f(x) = 4 - [4/3 - 4z/9 + 4(z^2)/27 - ...]
Power series f(x) = 8/3 + 4z/9 - 4(z^2)/27 + ... for x in the (2,3) interval

With the power series set up for x in the (2,3) interval, the program just builds the rational coefficients for power
series centered at 3.5 (based on the power series at 2.5), then at 4.5 (based on the power series at 3.5), and so on.
I limited the power series to 30 terms (comfortably enough for the desired precision). The coefficients of the previous
and current power series are stored as rational numbers. When the power series value divided by the midpoint of the
interval (say, at 6.5 or 101.5) crosses the target (e.g. 36/51 or 38/51), the program does a binary search to find x
within the interval such that E(x)/x is within 10^(-15) of the desired target (again, comfortably enough tolerance
for the desired precision). The program completed immediately to report the answers for both L1 and L2 (to 8 decimal
places after the decimal point as required). This power series approach can give us the answers to any degree of
precision we desire, especially since we use rational numbers throughout. Plus, it's very fast. The answers were:

L1 = 6.05072200
L2 = 100.96563634

The bonus puzzle asks for the median of the center-to-center distance between two successive swallows as L -> infinity.
We can set up a recursive integral for the empty space between two successive swallows (starting with the first swallow
creating gaps on its left and right). We can look at the problem from the point of view of the number of gaps of size <=
unknown median. But these approaches didn't go very far, not least due to the wire length tending to infinity. We can
approximate the problem by discretizing it. By discretizing the problem, we can find an approximate median (required to
be accurate to only 4 decimal places after the decimal point). Monte Carlo is another option though it felt like a cop-out
for an IBM puzzle. I read more than a dozen published papers related to random sequential adsorption (RSA) for polymers
and DNA sequencing. Some papers look at the gap distribution problem, even as length tends to infinity, but these are
time evolution approaches (for us, time also tends to infinity). I also thought of somehow setting this up as a Poisson
process (especially since the mean is easily determined for the infinite length case). It's trivial to calculate the mean
of gaps using Renyi's parking constant C, as follows...
If x is the wire length, and x -> infinity, then the space covered by swallows -> Cx on average. So, the number of swallows
of width 1 -> Cx. Total emoty space -> x - Cx on average. And, the number of empty slots (gaps) is the same as the number
of swallows on the jammed, infinitely long wire, so Cx.
Mean of emoty space width = (x - Cx)/Cx = (1/C) - 1
Mean of center-to-center distance between successive swallows = 1 + (1/C) - 1 = 1/C = 1/0.7475979202... = 1.33761742
approximately. Alas, no satisfying way, Poisson or otherwise, seems to be there to determine the median (other than
approximating it by discretization, either by calculation or with a Monte Carlo simulation). I decided not to use such
approaches, and still hold hope that there is a more satisfying way to find the median of gap distribution when wire
is jammed and wire length -> infinity.
(edit 8/10/25: the official solution has been posted on the IBM site, and it suggests Monte Carlo to find the median.
That's a letdown. I should have given in to the urge to take the easy path and run an approximation with dicretization
or Monte Carlo to approximate the median).
'''

from fractions import Fraction
from copy import deepcopy
from datetime import datetime
from decimal import Decimal, getcontext
#import sys
#sys.set_int_max_str_digits(50000) #use if precise rational number answer desired

print(datetime.now(), "Start")
TGT1 = Fraction(36, 51) #target FD for main puzzle with wire of length L1
TGT2 = Fraction(38, 51) #target FD for main puzzle with wire of length L2
ROUNDING_NEEDED = 8 #rounding to 8 decimal places (after the decimal point) needed for main puzzle

getcontext().prec = 18 #precision for calculations involving Decimal number objects

#number of terms to be considered in infinite power series (30 terms will give plenty of precision in this case
NUM_COEFFS = 30
TOL = Fraction(1, 10**15) #tolerance of how close answer should be to target; 10^(-15) is more than close enough
frac_2 = Fraction(2,1)
frac_1 = Fraction(1,1)
frac_3_2 = Fraction(3,2)
frac_neg1 = Fraction(-1,1)
frac_pos1 = Fraction(1,1)

#function to do binary search for answer given a narrowed down range and previous and current power series
def binary_search_sol(curr_n, new_coeffs, prev_coeffs, target):
    n = deepcopy(curr_n)
    #check if FD is <= or > than target at curr_n + 1
    high_z = Fraction(0,1)
    low_z = Fraction(0,1)
    z = Fraction(-1, 1)
    val = Fraction(0,1)
    for idx in range(NUM_COEFFS):
        val += new_coeffs[idx]*(z**idx)
    fd = (val - frac_1)/(n + frac_3_2 + (z/frac_2))
    if fd <= target:
        coeffs = new_coeffs
        low_z = deepcopy(z)
    else:
        coeffs = prev_coeffs
        high_z = Fraction(1, 1)
        n -= frac_pos1
        
    while low_z < high_z:
        z = (low_z + high_z)/frac_2
        val = Fraction(0,1)
        for idx in range(NUM_COEFFS):
            val += coeffs[idx]*(z**idx)
        e_x = val - frac_1
        x = n + frac_3_2 + (z/frac_2)
        fd = e_x/x
        if abs(fd - target) < TOL:
            print("L Decimal, rounded to 8 decimal places (8 digits after decimal point):", \
                  round(Decimal(str(x.numerator)) / Decimal(str(x.denominator)), ROUNDING_NEEDED))
            return
        elif fd < target:
            low_z = deepcopy(z)
        elif fd > target:
            high_z = deepcopy(z)

a_coeffs = []
# set up coefficients of power series 8/3 + 4z/9 - 4(z^2)/27 + ... for x in the (2,3) interval
a_coeffs.append(Fraction(8,3))
a_coeffs.append(Fraction(4,9))
for i in range(NUM_COEFFS-2):
    a_coeffs.append(a_coeffs[-1]*Fraction(-1,3))
b_coeffs = []
n = Fraction(2,1)
prev_fd = Fraction(5,3)/Fraction(5,2) # E(x)/x at x = 2.5
found_main = False
while True:
    #set up power series coefficients for next interval
    b_coeffs = []
    b0 = Fraction(0,1)
    numer = Fraction(1,1)
    denom = Fraction(1,1)
    for a in a_coeffs:
        b0 += a*(n+(numer/denom))
        numer *= frac_neg1
        denom += frac_pos1
    temp = (frac_2*n) + frac_pos1
    b0 *= frac_2/temp
    b_coeffs.append(b0)
    i = Fraction(1,1)
    idx = 1
    while idx < NUM_COEFFS:
        b_coeffs.append( ( ((Fraction(2,1) * a_coeffs[idx-1])/i) - b_coeffs[idx-1] )/temp )
        i += frac_pos1
        idx += 1
    fd_x = (b0 - Fraction(1,1))/(n + frac_3_2) # FD at midpoint of current interval
    if not found_main and fd_x > TGT1: #when FD first crosses the target for L1
        print("L1 answer:")
        binary_search_sol(n, b_coeffs, a_coeffs, TGT1)
        found_main = True
    if fd_x > TGT2: #when FD crosses the target for L2
        print("L2 answer:")
        binary_search_sol(n, b_coeffs, a_coeffs, TGT2)
        break
    a_coeffs = deepcopy(b_coeffs)
    n += frac_pos1
print(datetime.now(), "Done")

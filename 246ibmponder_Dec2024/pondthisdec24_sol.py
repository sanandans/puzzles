'''
My IBM Ponder This December '24 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/December2024.html
Sanandan Swaminathan, submitted December 3, 2024

Main puzzle's answer (max value of n where wd(n)/n = 1/2 for each d from 1 to 9):
1062880, 2125762, 3188644, 4251526, 5314408, 6377290, 17006110, 18068992, 19131874

Bonus * puzzle (max value of n where w1(n)/n = 3/4 for d = 1):
10167463313312

I solved both puzzles with pen and paper, and verified the arithmetic with the program below.
For n between 1 through 999,999, there are 10^6 - 9^6 = 468,559 numbers that contain any of
the digits 1 to 9. This is short of the 50% mark by 31,441. For n between 1,000,000 through
9,999,999, there are 10^7 - 9^7 = 5,217,031 numbers containing the digits. This is an excess
of 217,031 above the 50% mark. For n between 10,000,000 through 99,999,999, there are
10^8 - 9^8 = 56,953,279 numbers containing the digits. This is an excess of 6,953,279 above
the 50% mark. Of course, excesses get more pronounced for larger powers. The shortfall and
excesses indicated that the desired maximum values might fall between 1,000,000 and 10,000,000,
or maybe unto 100,000,000. It turned out that the maximum values for digits 1 through 6 were
between 1,000,000 and 10,000,000, but for digits 7 through 9, they were between 10,000,000 and
20,000,000. We can take the excess of 217031 acculumated at the n = 9,999,999 mark, and divide
it by the shortfall of 31441 at the n = 999,999 mark. We see that the excess will not reduce to
0 for digits 1 through 6 after n = 9,999,999, but only increase. For digits 7, 8, 9, we can see
that the excess can reduce to 0 beyond n = 9,999,999, but not beynd the 20 million mark.

For digits 1 through 6 and n between 1 million and 10 million, we can see that the shortfall at
the n = 999,999 mark can be made up when the given digit is the leading digit. We can
calculate the n for which this happens. Subsequently, enough excess occurs with that given
digit to prevent the 50% mark being reached again.
For example, for digit 1, let n = 1,000,000 + x.
Since there were 468559 numbers that contained digit 1 until n = 999999, and digit 1 is always
the leading digit for n between 1000000 and 1999999, we get the equation...
(468559 + 1 + x) / (1000000 + x) = 1/2
x = 62880
So, n = 1000000 + x = 1062880

We can do a similar calculation for digits 2,3,4,5,6. For digits 7,8,9, the analysis of shortfalls
and excesses shows that we must use n = 10,000,000 + x in the above equation. The bonus puzzle can
also be solved by hand for digit 1 in a similar way, by analyzing shortfalls and excesses, but this
time with the ratio needing to be 3/4, of course.

The short program below just performs the above analysis and calculations. It completes instantaneously
for both the main and bonus * puzzles.
'''

from datetime import datetime

print(datetime.now(), "Start")
n = 1
while (10**n - 9**n)/((10**n)-1) < 0.5:
    n += 1
excess = (10**n)//2 - (9**n)
shortfall = (9**(n-1)) - (10**(n-1))//2
dig_max = excess//shortfall

results = []
for dig in range(1, dig_max + 1):
    results.append(2*dig*(9**(n-1)) - 2)
for dig in range(dig_max+1, 10):
    results.append(2*(9**n) + 2*dig*(9**(n-1)) - 2)
print("main results:", results)

print(datetime.now(), "Main done, start bonus")
n = 1
while (10**n - 9**n)/((10**n)-1) < 0.75:
    n += 1
excess = (10**n)//4 - (9**n)
shortfall = (9**(n-1)) - (10**(n-1))//4
dig_max = excess//shortfall

if dig_max > 1:
    print("bonus answer:", 4*(9**(n-1)) - 4)
print(datetime.now(), "Bonus done")

'''
Uncomment this block to see excesses/shortfalls for different powers of 10

for n in range(1,21):
    numer = 10**n - 9**n
    print(n, numer, numer/((10**n)-1))
'''

'''
IBM Ponder This challenge main and bonus ** of August '23
https://research.ibm.com/haifa/ponderthis/challenges/August2023.html
Sanandan Swaminathan, submitted July 31, 2023

Square-triangular numbers satisfy the recursion t = (34*tprev) - tprevprev + 2.
The first two ST numbers are 0 and 1. We are interested in positive ST nums, so
we start counting from the ST num 1.
A short loop gives the answer for the main puzzle:
66 positive square triangular numbers below googol.
Largest square triangular num below googol is...
3528831738665785331018532608627089984902507186374639595868856306732434076647600751541072978742212900

For the bonus **, we can use Euler's formula for the k'th square-triangular number (k >= 0).
If N(k) is the k'th square-triangular number (where k >= 0), then,
by Euler's formula:
N(k) = ( ( (3+2sqrt(2))^k - (3-2sqrt(2))^k ) / 4sqrt(2) )^2
We need the largest k where N(k) < 10^(10^100) (i.e. googolplex)
( ( (3+2sqrt(2))^k - (3-2sqrt(2))^k ) / 4sqrt(2) )^2 < 10^(10^100)
For large k, (3-2sqrt(2))^k <<  (3+2sqrt(2))^k, so we can ignore it, and the inequality simplifies to...
(3+2sqrt(2))^(2k) < 10^(10^100) * 32
Taking log to base 10, we get...
(2k) * log10( 3+2sqrt(2) ) < (10^100) + log10( 32 )
k < ( (10^100) + log10( 32 ) ) / ( 2 * log10( 3+2sqrt(2) )
I plugged the RHS expression into wolfram alpha to determine the largest k less than 10^(10^100).
Alternately, we could use bc kind of high precision library.
Exact number of positive square-triangular numbers below googolplex is:
6531240347184892454849237722169246600586075961192434058882920840740253494104859805019550623847957752
Note that this k is giving us the number of positive ST nums below googolplex.
Number of ST nums including 0 that are less than googolplex would be one more.
The above approximation technique, especially ignoring (3-2sqrt(2))^k for large k, works for the much smaller
googol too; it gives 66 positive ST nums below googol.
So the approximation technique would definitely hold for the much larger googolplex too.
Of course, unlike the main puzzle where we can compute and display the largest ST num below googol,
we can't even dream about computing, let alone ddisplaying, the largest ST num below googolplex.
The grand total number of atoms in the unverse is estimated to only be of the order of 10^80.
'''
limit = 10**100 #googol
tprevprev = 0 #first square-triangular number
tprev = 1 #first positive square-triangular number
cnt=1 #keep count of positive square-triangular numbers
while True:
    t = (34*tprev) - tprevprev + 2
    if t >= limit:
        break
    cnt += 1
    tprevprev, tprev = tprev, t
print(cnt, tprev)


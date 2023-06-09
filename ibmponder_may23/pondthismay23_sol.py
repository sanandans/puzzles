'''
IBM Ponder This challenge May '23
https://research.ibm.com/haifa/ponderthis/challenges/May2023.html
Sanandan Swaminathan, submitted May 4, 2023

This is an interesting linear algebra puzzle,
with fairly big data - a 1 by million (well, 2^20) row vector of equi-spaced fractions,
multiplied by a million by million matrix containing psuedo-randomly generated
fractions, and then multiplied by the transpose of the 1 by million row vector.
The size of the bonus * problem is even bigger - replace million above with
billion everywhere. This program is currently single-threaded.

The n elements of column vector x have the form:
x[j] = -1 + j*(2/(n-1)), where j = 0 to n-1.

We can extract the denominators out, and do all calculations with integers until the end.

The components of the 1 x n matrix resulting from multiplying x_transpose with matrix A are of the form:
result[j] = 2*{ sum of A[i][j] * i } - { (n-1)*{ sum of A[I][j] }, for i = 0 to n-1, divided by (n-1)*((2^k) - 1). 
Here, A[I][j] is the natural number [Qi == Qj] without the (2^k) - 1 denominator.

We can process each set bit of A[I][j] independently in the matrix multiplication to avoid creating and comparing
k-element Q vectors. This does mean more compute operations but the trade-off seems reasonable.

We first get the intermediate result of multiplying x_transpose with matrix A. I also have an array of lists
which can hold 2^k lists. Rather than create and compare the Q vectors, I have a t-loop that iterates k times,
once for each Q component. The idea is to process each set bit of A[I][j] separately. An inner loop that iterates
n times processes all the Q[t] values for a specific t.
 > i for any (i, j) pair, and Q is all 1's when j == i).
 The calculated Q[t] value falls into one of the 2^k lists. These lists (and their lengths and sums) can be used to
 directly calculate the intermediate result needed.

Once we have the 1 x n intermediate result matrix (integer numerator part) of the x_transpose times matrix A
multiplication, we multiply it with the x column vector to get the final numerator (integer).
The final denominator is the integer (n-1)*(n-1)*((2^k) - 1).
Program takes around 3 seconds for n = 2^20.
'''

from math import sin
from math import floor
from datetime import datetime

start_time = datetime.now()
print("starting", start_time)
ctr=0
k=5
n=2**20
pow_2k = 2**k
mult = n-1
result_firstterm=0
result_secondterm=0

for t in range(k):
    #print(ctr, datetime.now())
    q_digit_vals = [[] for _ in range(pow_2k)]
    qdig_list_sums = [0]*pow_2k
    pow_2t = 2**t
    tplus1 = t+1

    #for this t, for each of the n i's, bucket the computed result of the sin formula into the appropriate list
    for i in range(n):
        ctr += 1
        '''
        if ctr%10000000 == 0:
            print(ctr, datetime.now())
        '''
        temp = sin((i+1)*(tplus1))
        temp = floor(pow_2k*(temp - floor(temp)))
        q_digit_vals[temp].append(i)
        qdig_list_sums[temp] += i

    #now we can simply sweep through the elements in each list, and add their contributions
    #to the multiplication of x_transpose times matrix A
    for i in range(len(q_digit_vals)):
        for j in q_digit_vals[i]:
            #adding contributions for x_transpose multiplied by A matrix
            xt_res_temp = ((2 * qdig_list_sums[i]) - (mult * len(q_digit_vals[i]))) * pow_2t
            result_firstterm += j*xt_res_temp
            result_secondterm += xt_res_temp

#intermediate 1xn result multiplied by nx1 column vector x
result_numerator = (2*result_firstterm) - (mult*result_secondterm)
result_denominator = mult*mult*(pow_2k - 1)
print("result_numerator:", result_numerator, "result_denominator:", result_denominator)
print("answer:", round(result_numerator/result_denominator, 3))
end_time = datetime.now()
print("done:", end_time, "elapsed time:", end_time-start_time)
'''
result_numerator: 1785711786534373802
result_denominator: 34084795449375
answer: 52390.274
elapsed time: 0:00:03.345339
'''


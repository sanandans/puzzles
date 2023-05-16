'''
IBM Ponder This May 23
https://research.ibm.com/haifa/ponderthis/challenges/May2023.html
Sanandan Swaminathan, submitted May 4, 2023

-297135.726



In exact terms, this is -10127810427725542998 / 34084795449375



Please let me know if the answer is incorrect, and I can check my calculations (I only checked calculations with small n, like n=10, k=5).



Here is what my short python program does. The n elements of column vector x have the form:

x[j] = -1 + j*(2/(n-1)), where j = 0 to n-1.



We can extract the denominators out, and do all calculations with integers until the end. The components of the 1 x n matrix resulting from multiplying x_transpose with matrix A are of the form:



result[j] = 2*{ sum of A[i][j] * i } - { (n-1)*{ sum of A[I][j] }, for i = 0 to n-1}, divided by (n-1)*((2^k) - 1). 



Here, A[I][j] is the natural number [Qi == Qj] without the (2^k) - 1 denominator. We can process each set bit of A[I][j] independently in the matrix multiplication to avoid creating and comparing k-element Q vectors. This does mean more compute operations but the trade-off seems reasonable.



I have a couple of arrays of length n to capture the two running sums above for each component, and get the intermediate result of multiplying x_transpose with matrix A. I also have an array of lists which can hold 2^k lists. Rather than create and compare the Q vectors, I have a t-loop that iterates k times, once for each Q component. The idea is to process each set bit of A[I][j] separately. An inner loop that iterates n times processes all the Q[t] values for a specific t. Q indexes are processed from 0 to n-1 since we only need to consider j > i (j < i is identical to j > i for any (i, j) pair, and Q is zero when j = i). The calculated Q[t] value falls into one of the 2^k lists. The Q(t) value is truncated to integer as in the given example (though not mentioned in the given sine-based formula). It is also clear that Q[t] can be 0 (though some people don’t consider 0 to be a natural number which the components of Q are said to be). Before appending the current index to the appropriate list, it is processed against earlier indexes in that list since they all have the same Q[t] value at this t position. The sums arrays are updated at the relevant positions, just for the contribution from this set bit, both for A[I][j] and A[j][I] since they are the same. Once Q[t] processing is completed for all indexes for the given t, the procedure is repeated (for each of the k values of t).



Once we have the 1 x n intermediate result matrix (integer numerator part) of the x_transpose times matrix A multiplication, I multiply it with the x column vector to get the final numerator (integer). The final denominator is the integer (n-1)*(n-1)*((2^k) - 1).

'''

import math
from math import sin
from math import floor
#import numpy as np
from datetime import datetime

start_time = datetime.now()
print(start_time)
ctr=0

'''
Puzzle: https://research.ibm.com/haifa/ponderthis/challenges/May2023.html

This is an interesting data science/linear algebra puzzle,
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

We can process each set bit of A[I][j] independently in the matrix multiplication to avoid creating and comparing k-element Q vectors.
This does mean more compute operations but the trade-off seems reasonable.

I have a couple of arrays of length n to capture the two running sums above for each component,
nd get the intermediate result of multiplying x_transpose with matrix A. I also have an array of lists
which can hold 2^k lists. Rather than create and compare the Q vectors, I have a t-loop that iterates k times, once for each Q component.
The idea is to process each set bit of A[I][j] separately. An inner loop that iterates n times processes all the Q[t] values for a specific t.
Q indexes are processed from 0 to n-1 since we only need to consider j > i (j < i is identical to j > i for any (i, j) pair, and Q is zero when j = i).
The calculated Q[t] value falls into one of the 2^k lists. The Q(t) value is truncated to integer as in the given example
(though not mentioned in the given sine-based formula). It is also clear that Q[t] can be 0 (though some people don’t consider 0 to be a natural number
which the components of Q are said to be). Before appending the current index to the appropriate list,
it is processed against earlier indexes in that list since they all have the same Q[t] value at this t position.
The sums arrays are updated at the relevant positions, just for the contribution from this set bit, both for A[I][j] and A[j][I] since they are the same.
Once Q[t] processing is completed for all indexes for the given t, the procedure is repeated (for each of the k values of t).

Once we have the 1 x n intermediate result matrix (integer numerator part) of the x_transpose times matrix A multiplication, we multiply it with the x column vector
to get the final numerator (integer). The final denominator is the integer (n-1)*(n-1)*((2^k) - 1).
'''

k=5
n=10 #2**20 for main puzzle, 2**30 for bonus *
pow_2k = 2**k
coltot = [0]*n
xt_res = [0]*n

for t in range(k):
    print(ctr, datetime.now())
    q_digit_vals = [[] for _ in range(pow_2k)]
    pow_2t = 2**t
    tplus1 = t+1
    
    for i in range(n):
        ctr += 1
        if ctr%100000 == 0:
            print(ctr, datetime.now())
            
        temp = sin((i+1)*(tplus1))
        temp = floor(pow_2k*(temp - floor(temp)))
        for item in q_digit_vals[temp]:
            coltot[item] += pow_2t
            coltot[i] += pow_2t
            xt_res[item] += (i * pow_2t)
            xt_res[i] += (item * pow_2t)
        q_digit_vals[temp].append(i)

mult = n-1
for i in range(n):
    xt_res[i] = (2*xt_res[i]) - (mult*coltot[i])

result_firstterm=0
result_secondterm=0
for i in range(n):
    result_firstterm += (i*xt_res[i])
    result_secondterm += xt_res[i]
    
result_numerator = (2*result_firstterm) - (mult*result_secondterm)
result_denominator = mult*mult*(pow_2k - 1)
print("result_numerator:", result_numerator, "result_denominator:", result_denominator)
print("answer:", round(result_numerator/result_denominator, 3))
end_time = datetime.now()
print(datetime.now(), "elapsed time:", end_time-start_time)




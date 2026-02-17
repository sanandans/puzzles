'''
My IBM Ponder This January '26 challenge main and bonus * solutions
https://research.ibm.com/blog/ponder-this-january-2026
Old URL: https://research.ibm.com/haifa/ponderthis/challenges/January2026.html
Sanandan Swaminathan, submitted January 28, 2026

Due to the fact that any power of 10 is 1 mod 9, any split-and-add of n would have
the same value mod 9 as n mod 9. This is true for any rearrangement of the string
of n too, but that's irrelevant here. Elements x of n.A(n) would be n*n mod 9. The only
way n can be a member of A(x) is if n is 1 mod 9 or 0 mod 9. Thus, we only need to
consider numbers n of the form 9m or 9m + 1 (within the given range for n). This
reduces the search to two-ninths of the range of n's. Iterating through n's in the
order 1, 9, 10, 18, 19... upto the max limit, my program builds and caches A(n).
For each x = n.A(n), it checks if n belongs to A(x). If true, the x is added to the
overall sum, and x is also added to a "found" set to avoid adding x again if it
qualifies again with a later n. To determine if n belongs to A(x), the program
checks if A(x) is in the cache and if n is in A(x). Otherwise, it splits x
progressively from right to left. It does recursion to determine if exactly n can
be made with splits. This allows it to abort the search early if it reaches a stage
where getting a sum of exactly n is ruled out. This was also a way for me to avoid
caching A(x) for x larger than the max limit of n. I couldn't think of a math trick that
would be significantly faster in determining if n belongs to A(x). The program completes
in about 25 seconds for the main puzzle, and about 12 minutes for the bonus puzzle.
Answers:
160808197419276 for main puzzle (1 <= n <= 10^6)
26190672886645170 for bonus * puzzle (1 <= n <= 10^7)
'''

from datetime import datetime

max_n = 10**6 # 10**6 for main, 10**7 for bonus
A_sets = dict()
qualifying_x = set()
result_sum = 0

def create_A_set(num):
    if num in A_sets:
        return A_sets[num]
    A_sets[num] = {num}
    div = 10
    left_num = num // div
    while left_num > 0:
        right_num = num % div
        for n in create_A_set(left_num):
            A_sets[num].add(n + right_num)
        div *= 10
        left_num = num // div
    return A_sets[num]

def n_in_A_of_x(rem_n, rem_x):
    if rem_n > rem_x:
        return False
    elif rem_n == rem_x:
        return True
    elif rem_n <= 0:
        return False
    div = 10
    while rem_x//div > 0:
        if n_in_A_of_x(rem_n - (rem_x % div), rem_x//div):
            return True
        div *= 10
    return False

def process_n(num):
    global result_sum
    for i in create_A_set(num):
        x = num * i
        if x in qualifying_x:
            continue
        if n_in_A_of_x(num, x):
            result_sum += x
            qualifying_x.add(x)

print(datetime.now(), "start: max n is:", max_n)
max_9_multiplier = max_n//9
progress_cnt = max(1, max_9_multiplier//10)
for i in range(max_9_multiplier + 1):
    if i%progress_cnt == 0:
        print(datetime.now(), i)
    temp_n = i * 9
    process_n(temp_n)
    process_n(temp_n + 1)
print(datetime.now(), "ANSWER:", result_sum)

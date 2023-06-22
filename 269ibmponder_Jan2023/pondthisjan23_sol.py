'''
IBM Ponder This challenge main and bonus *, Jan 23
https://research.ibm.com/haifa/ponderthis/challenges/January2023.html
Sanandan Swaminathan, submitted January 14, 2023

Main puzzle (20-letter gene of only A's and C's and minimal number of steps to reach a gene of all ‘G’ characters between 880000 and 890000):

['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'A', 'C', 'C', 'A', 'C']
885125

Bonus "*" puzzle (minimal number of steps required for reaching the all-‘G’ state from an all-‘T’ state, for n=100 letters):

845100400152152934331135480100

My interpretation of constraint phrasing: Regarding the phrase "remaining letters to its left" in three of the given constraints, I 
interpreted this to mean that the "remaining letters to its left" can be 0. This interpretation is based on the given example 
where [‘C’, ‘T’, ‘G’, ‘G’, ‘G’] becomes [‘C’, ‘G’, ‘G’, ‘G’, ‘G’] using constraint #2 even though there are zero remaining 
letters ('A') to the left of CT.

Nomenclature in my solution writeup below: When I write a string as A(w)C(x)T(y)G(z) below, for example, read it as w number of A's, 
followed by x number of C's, etc.

First, I wrote a breadth-first search (for small strings like ten A and C characters) with visited strings tracked to avoid looping 
back. This was helpful to check the results against the given examples and also to understand the patterns. The following ideas 
developed from this initial analysis:
a) There is no purpose to ever using the constraint T(x)G -> T(x+1).
b) If we start with an n-letter string containing only A's and C's, and wish to proceed until the string transforms to C(n) 
or A(1)C(n-1), then the only applicable constraints throughout are A(x)C(2) -> A(x)C(1)A(1), and A(x)C(1)A(1) -> A(x)C(2), and 
changing the leftmost letter from A -> C or C -> A.
c) The G's should be filled from the rightmost end to the leftmost end. To get a G, we need to use A(x)C(1)T(1) -> A(x)C(1)G(1), and 
then we have a shorter string to process. To get to A(x)C(1)T(1), we must first get to C(x+2) or A(1)C(x+1), then move to T(x+2), then 
to C(x+1)T(1), and then to A(x)C(1)T(1). After putting the G in the end, we must go from A(x)C(1) to C(x+1) or to A(1)C(x). We can 
then process the shorter string by the same rules.

Then, the following formulas could be seen for minimal steps:
a) C(n) or A(1)C(n-1) -> T(n) = n steps
b) T(n) -> C(n-1)T(1) = n-1 steps
c) To do C(2x-1)C(1)T(1) -> A(2x-1)C(1)T(1), we need (4^x - 1)/3 steps. To do C(2x)C(1)T(1) -> A(2x)C(1)T(1), we need 2(4^x - 1)/3 
steps.
d) A(x)C(1)T(1) -> A(x)C(1)G(1) = 1 step.
d) To do A(n)C(1) -> C(n)C(1) (or to A(1)C(n-1)C(1)), we can start with steps=0 and loop n times as follows: double the steps, and if 
the loop counter is odd, add 1. If n is odd, after the loop, subtract 1 from steps (this is done because, in this scenario, it is 
sufficient to reach A(1)C(n-1)C(1) and start substituting T's from the left).
f) CG(n-1) -> G(n) = 1 step.

I wrote a short function that uses the above formulas to calculate the minimal number of steps from C(n) (or A(1)C(n-1)) to G(n). This 
completes instantaneously. For the main puzzle, my program first computes this number, say X. X turned out to be 699440. Then, the 
program loops through 20-letter strings (containing only A's and C's) in lexicographic order. For each string, it does breadth-first 
search (with visited strings tracked) to find the minimal number of steps, say Y, to go from the starting string to C(n) or A(1)C(n-1),
 whichever is reached first. Y has to be between 880000-X and 890000-X, so between 180560 and 190560. In a couple of minutes, the 
program found the lexicographically smallest string ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'C', 'A', 
'C', 'C', 'A', 'C'] that fulfills the goal for the main puzzle, with minimal steps being 885125.

For the bonus "*" puzzle, the function instantaneously calculated the minimal number of steps to go from C(100) to G(100). Subtracting 
the 100 steps it takes to go from C(100) to T(100) gave the bonus "*" answer: minimal steps  845100400152152934331135480100.

'''

from queue import Queue
from datetime import datetime

def print_preds(dist_from_start):
    temp_pred = FINAL_STR
    while temp_pred != "XYZ":
        print(temp_pred, dist_from_start)
        temp_pred = visited_preds_dict[temp_pred]
        dist_from_start -= 1

def add_new_string(new_string, predecessor_string, distance):
    if new_string not in visited_preds_dict:
        visited_preds_dict[new_string] = predecessor_string
        bfs_queue.put([new_string, distance])

def BFS_ac_allc():
    while bfs_queue.empty() == False:
        popped = bfs_queue.get()
        item = popped[0]
        dist_from_start = popped[1]
        if item == ALL_C_STR or item == ALT_C_STR:
            #print(dist_from_start)
            #print_preds(dist_from_start)
            return dist_from_start
       
        for replace_first_letter in ('C','A'):
            if item[0] != replace_first_letter:
                temp_str = replace_first_letter + item[1:]
                add_new_string(temp_str, item, dist_from_start+1)
        if item[0] == 'C':
            if item[1] == 'C':
                temp_str = "CA" + item[2:]
            elif item[1] == 'A':
                temp_str = "CC" + item[2:]
            add_new_string(temp_str, item, dist_from_start+1)

        elif item[0] == 'A':
            for i in range(1,len(item)-1):
                if item[i] == 'C':
                    if item[i+1] == 'C':
                        sub='A'
                    elif item[i+1] == 'A':
                        sub='C'
                    if i == len(item) - 2:
                        temp_str = item[:i+1] + sub
                    else:
                        temp_str = item[:i+1] + sub + item[i+2:]
                    add_new_string(temp_str, item, dist_from_start+1)
                    break
    return -1

# input_cstring can be C(n) or AC(n-1)
def min_len_allc_allg(allc_str_len):
    n = allc_str_len
    tot_steps = 0
    while n>1:
        # C(n) or AC(n-1) -> T(n) = n steps, T(n) -> C(n-1)T = n-1 steps
        tot_steps += (2*n) - 1
        #C(n-2)CT -> A(n-2)CT = (4^((n-2 + ((n-2)%2))//2) - 1)/3 if n-2 is odd, and twice of that if n-2 is even
        steps = (pow( 4, (n-2 + ((n-2)%2))//2 ) - 1)//3
        if (n-2)%2 == 0:
            steps *= 2
        tot_steps += steps
        #A(n-2)CT -> A(n-2)CG = 1 step
        tot_steps += 1
        #If n-2 is odd, A(n-2)C -> AC(n-1) takes 1,2,5,10,21,42,85,170... steps. If n-2 is even, A(n-2)C -> C(n-1) takes 
        #those steps, and then minus 1
        steps=0
        for i in range(1, n-1):
            steps = (steps*2) + (i%2)
        if (n-2)%2 == 1:
            steps -= 1
        tot_steps += steps
        #Now we have C(n-1) or AC(n-2), so we loop
        n -= 1

    #We now have CG(n-1), so 1 more step to make it G(n)
    tot_steps += 1
    return tot_steps

MAX_STR_LEN=20
FINAL_STR=("0".zfill(MAX_STR_LEN)).replace('0','G')
ALL_C_STR=("0".zfill(MAX_STR_LEN)).replace('0','C')
ALT_C_STR='A' + ("0".zfill(MAX_STR_LEN -1)).replace('0','C')
'''
start_str="CACACACACACACACACACA"
print(len(start_str),len(FINAL_STR))
visited_preds_dict[start_str] = "XYZ"
bfs_queue.put([start_str, 0])
needed_steps = BFS_ac_allc()
if needed_steps == -1:
    print("issue converting ac string to all c string")
else:
    needed_steps += min_len_allc_allg(len(start_str))
print(needed_steps)
'''
print("start main:", datetime.now())
allc_allg_steps = min_len_allc_allg(MAX_STR_LEN)
print("C(n) or AC(n-1) to G(n) number of steps:", allc_allg_steps, datetime.now())
low_threshold = 880000 - allc_allg_steps
high_threshold = 890000 - allc_allg_steps
for i in range(pow(2,MAX_STR_LEN)):
    start_str = (((bin(i)[2:]).zfill(MAX_STR_LEN)).replace('0','A')).replace('1','C')
    visited_preds_dict = {}
    bfs_queue = Queue(maxsize = 0)
    visited_preds_dict[start_str] = "XYZ"
    bfs_queue.put([start_str, 0])
    needed_steps = BFS_ac_allc()
    #print(start_str, needed_steps+allc_allg_steps)
   
    if needed_steps >= low_threshold and needed_steps <= high_threshold:
        print("found start str:",start_str, " , tot steps from start str to G(n):", needed_steps+allc_allg_steps, " , num steps from start str to C(n) or AC(n-1):", needed_steps)
        #print main answer in desired format
        res="['"+start_str[0]+"'"
        for j in range(1,MAX_STR_LEN):
            res += ", '"+start_str[j]+"'"
        res += "]"  
        print(res)
        print(needed_steps+allc_allg_steps)
        break
print("end main:", datetime.now())

#extra credit
print("extra credit number of steps:", min_len_allc_allg(100) - 100)
print("end extra credit:", datetime.now())


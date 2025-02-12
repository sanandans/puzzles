'''
My IBM Ponder This January '25 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/January2025.html
Sanandan Swaminathan, submitted December 31, 2024

Note: Separate files for main and bonus * puzzles.

For the bonus puzzle, I tweaked my program for the main puzzle. It
increments q (starting from 1). For a given q, the candidate values of p
vary from 1 to q*sqrt(3). However, only those values need to be considered
where p and q are relatively prime, i.e. GCD(p, q) = 1 since we are processing
from lower to higher q values.
For each (p, q), jug C's volume p/q is calculated. Then, the BFS search is
done to see if there is a solution in exactly 11 steps. If any jug has
1 +- 10^(-8) liters before 11 steps, the search with that p/q is aborted,
and the next p/q is tried. If the desired state is reached by BFS in exactly
11 steps, the p/q and path and path length are printed. This actually takes
several hours to find the answer. Parallel processing or multi-threading with
different batches of q values would speed this up.

Bonus * answer (p/q, and the 11 steps):
p/q =  4224 / 3187
Number of steps and list of steps: 11 TA AB AC TA AC CS AC CS AC TA AC
After 11 steps, jug A ends up with about 1 liter (within the 10^(-8) tolerance).
Jugs A,B,C with capacity sqrt(5), sqrt(3) and 4224/3187 respectively don't lead to
a solution in fewer than 11 steps.
'''

import math
from datetime import datetime

print("Start bonus * puzzle", datetime.now())
a_cap = math.sqrt(5)
b_cap = math.sqrt(3)
MIN_LIM = 1 - 0.00000001
MAX_LIM = 1 + 0.00000001
MAX_DEPTH = 11
sol_found = False
cnt=0
c_q = 3185 #start from 1
while True:
    cnt += 1
    if cnt%100==0:
        print(datetime.now(),c_q)
    c_p_min = 1
    c_p_max = int(c_q * b_cap)
    for c_p in range(c_p_min, c_p_max+1):
        #if c_p ad c_q are not relatively prime, try next c_p
        if math.gcd(c_p, c_q) != 1:
            continue
        c_cap = c_p/c_q
        q = [] #queue of states for iterative BFS search
        q.append((0,0,0)) #initial state of empty jugs
        '''
        visited dictionary maps a state (tuple of 3 jugs) to its predecessor
        state, the action that caused the current state and the state's depth.
        This helps avoid repeat processing for previously visited states, can be
        used to print the answer when the terminating state is encountered, and
        move to next jug C capacity if current capacity causes a solution
        prematurely (in less than 11 steps).
        '''
        visited = dict()
        visited[(0,0,0)] = (None, None, 0)
        #iterative BFS search with jug C having capacity p/q
        while len(q) > 0:
            curr_state_tup = q.pop(0)
            #if terminating state is reached
            if (curr_state_tup[0] >= MIN_LIM and curr_state_tup[0] <= MAX_LIM) or \
               (curr_state_tup[1] >= MIN_LIM and curr_state_tup[1] <= MAX_LIM) or \
               (curr_state_tup[2] >= MIN_LIM and curr_state_tup[2] <= MAX_LIM):
                #if terminating state is reached in exactly 11 steps, print answer and quit
                if visited[curr_state_tup][2] == MAX_DEPTH:
                    print("Final state reached:", curr_state_tup)
                    print("p/q = ", c_p,"/",c_q)
                    templist = []
                    templist.append(visited[curr_state_tup][1])
                    pred = visited[curr_state_tup][0]
                    while visited[pred][0] is not None:
                        templist.append(visited[pred][1])
                        pred = visited[pred][0]
                    print(len(templist), end=" ")
                    for i in range(len(templist)-1, -1, -1):
                        print(templist[i], end=" ")
                    sol_found = True
                #whether terminating state is reached in exactly 11 steps or less,
                #break out of BFS search for given jug C capacity
                break

            #if current state's depth is less than 11 steps, add next states.
            #if we are at a depth of exactly 11 steps, simply continue looking
            #for a state that might be a terminating state.
            if visited[curr_state_tup][2] < MAX_DEPTH:
                #empty jug (A, B or C) into sink
                if curr_state_tup[0] > 0 and \
                   (0,curr_state_tup[1],curr_state_tup[2]) not in visited:
                    visited[(0,curr_state_tup[1],curr_state_tup[2])] = (curr_state_tup,"AS",visited[curr_state_tup][2]+1)
                    q.append((0,curr_state_tup[1],curr_state_tup[2]))
                if curr_state_tup[1] > 0 and \
                   (curr_state_tup[0],0,curr_state_tup[2]) not in visited:
                    visited[(curr_state_tup[0],0,curr_state_tup[2])] = (curr_state_tup,"BS",visited[curr_state_tup][2]+1)
                    q.append((curr_state_tup[0],0,curr_state_tup[2]))
                if curr_state_tup[2] > 0 and \
                   (curr_state_tup[0],curr_state_tup[1],0) not in visited:
                    visited[(curr_state_tup[0],curr_state_tup[1],0)] = (curr_state_tup,"CS",visited[curr_state_tup][2]+1)
                    q.append((curr_state_tup[0],curr_state_tup[1],0))

                #transfer from tap/jug to jug
                rem = a_cap - curr_state_tup[0]
                if rem > 0:
                    if (a_cap,curr_state_tup[1],curr_state_tup[2]) not in visited:
                        visited[(a_cap,curr_state_tup[1],curr_state_tup[2])] = (curr_state_tup,"TA",visited[curr_state_tup][2]+1)
                        q.append((a_cap,curr_state_tup[1],curr_state_tup[2]))
                    min_tr = min(rem, curr_state_tup[1])
                    if min_tr > 0 and \
                       (curr_state_tup[0]+min_tr,curr_state_tup[1]-min_tr,curr_state_tup[2]) not in visited:
                        visited[(curr_state_tup[0]+min_tr,curr_state_tup[1]-min_tr,curr_state_tup[2])] = (curr_state_tup,"BA",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0]+min_tr,curr_state_tup[1]-min_tr,curr_state_tup[2]))
                    min_tr = min(rem, curr_state_tup[2])
                    if min_tr > 0 and \
                       (curr_state_tup[0]+min_tr,curr_state_tup[1],curr_state_tup[2]-min_tr) not in visited:
                        visited[(curr_state_tup[0]+min_tr,curr_state_tup[1],curr_state_tup[2]-min_tr)] = (curr_state_tup,"CA",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0]+min_tr,curr_state_tup[1],curr_state_tup[2]-min_tr))

                rem = b_cap - curr_state_tup[1]
                if rem > 0:
                    if (curr_state_tup[0],b_cap,curr_state_tup[2]) not in visited:
                        visited[(curr_state_tup[0],b_cap,curr_state_tup[2])] = (curr_state_tup,"TB",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0],b_cap,curr_state_tup[2]))
                    min_tr = min(rem, curr_state_tup[0])
                    if min_tr > 0 and \
                       (curr_state_tup[0]-min_tr,curr_state_tup[1]+min_tr,curr_state_tup[2]) not in visited:
                        visited[(curr_state_tup[0]-min_tr,curr_state_tup[1]+min_tr,curr_state_tup[2])] = (curr_state_tup,"AB",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0]-min_tr,curr_state_tup[1]+min_tr,curr_state_tup[2]))
                    min_tr = min(rem, curr_state_tup[2])
                    if min_tr > 0 and \
                       (curr_state_tup[0],curr_state_tup[1]+min_tr,curr_state_tup[2]-min_tr) not in visited:
                        visited[(curr_state_tup[0],curr_state_tup[1]+min_tr,curr_state_tup[2]-min_tr)] = (curr_state_tup,"CB",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0],curr_state_tup[1]+min_tr,curr_state_tup[2]-min_tr))

                rem = c_cap - curr_state_tup[2]
                if rem > 0:
                    if (curr_state_tup[0],curr_state_tup[1],c_cap) not in visited:
                        visited[(curr_state_tup[0],curr_state_tup[1],c_cap)] = (curr_state_tup,"TC",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0],curr_state_tup[1],c_cap))
                    min_tr = min(rem, curr_state_tup[0])
                    if min_tr > 0 and \
                       (curr_state_tup[0]-min_tr,curr_state_tup[1],curr_state_tup[2]+min_tr) not in visited:
                        visited[(curr_state_tup[0]-min_tr,curr_state_tup[1],curr_state_tup[2]+min_tr)] = (curr_state_tup,"AC",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0]-min_tr,curr_state_tup[1],curr_state_tup[2]+min_tr))
                    min_tr = min(rem, curr_state_tup[1])
                    if min_tr > 0 and \
                       (curr_state_tup[0],curr_state_tup[1]-min_tr,curr_state_tup[2]+min_tr) not in visited:
                        visited[(curr_state_tup[0],curr_state_tup[1]-min_tr,curr_state_tup[2]+min_tr)] = (curr_state_tup,"BC",visited[curr_state_tup][2]+1)
                        q.append((curr_state_tup[0],curr_state_tup[1]-min_tr,curr_state_tup[2]+min_tr))
        if sol_found:
            break
    if sol_found:
        break
    c_q += 1 #try next c_q value

print("\nEnd bonus * puzzle", datetime.now())

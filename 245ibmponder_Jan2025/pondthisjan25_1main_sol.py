'''
My IBM Ponder This January '25 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/January2025.html
Sanandan Swaminathan, submitted December 31, 2024

Note: Separate files for main and bonus * puzzles.

For the main puzzle, the program uses iterative BFS with a "visited" dictionary
that maps a state to its predecessor state and the action that resulted in the
current state. When the terminating condition is reached in the BFS search, the
path length and the path found get printed. BFS guarantees that a shortest sequence
of steps has been found. I used the mpmath package to deal with the precision requirement.
The program completes in about 7 seconds.

One answer for the main puzzle:
39 TC CA TC CA AS CA TC CA AB TC CA TC CA AS CA TC CA AS CA TC CA TC CA AS CA TC CA
TC CA AS CA TC CA AS CA TC CA TC CA
'''

import math
from mpmath import *
from datetime import datetime

print("Start main puzzle", datetime.now())
mp.dps=96

a_cap = mpf(math.sqrt(5))
b_cap = mpf(math.sqrt(3))
c_cap = mpf(math.sqrt(2))

MIN_LIM = mpf(0.9997)
MAX_LIM = mpf(1.0003)
q = [] #queue of states for iterative BFS search
q.append((mpf(0),mpf(0),mpf(0))) #initial state of empty jugs
'''
visited dictionary maps a state (tuple of 3 jugs) to its predecessor
state and the action that caused the current state.
This helps avoid repeat processing for previously visited states and
can be used to print the answer when the terminating state is encountered.
'''
visited = dict()
visited[(mpf(0),mpf(0),mpf(0))] = (None, None)

#do iterative BFS search
while len(q) > 0:
    curr_state_tup = q.pop(0)
    #if terminating state is reached, print answer and break
    if (curr_state_tup[0] >= MIN_LIM and curr_state_tup[0] <= MAX_LIM) or \
       (curr_state_tup[1] >= MIN_LIM and curr_state_tup[1] <= MAX_LIM) or \
       (curr_state_tup[2] >= MIN_LIM and curr_state_tup[2] <= MAX_LIM):
        templist = []
        templist.append(visited[curr_state_tup][1])
        pred = visited[curr_state_tup][0]
        while visited[pred][0] is not None:
            templist.append(visited[pred][1])
            pred = visited[pred][0]
        print(len(templist), end=" ")
        for i in range(len(templist)-1, -1, -1):
            print(templist[i], end=" ")
        break

    #empty jug (A, B or C) into sink
    if curr_state_tup[0] > 0 and \
       (mpf(0),curr_state_tup[1],curr_state_tup[2]) not in visited:
        visited[(mpf(0),curr_state_tup[1],curr_state_tup[2])] = (curr_state_tup,"AS")
        q.append((mpf(0),curr_state_tup[1],curr_state_tup[2]))
    if curr_state_tup[1] > 0 and \
       (curr_state_tup[0],mpf(0),curr_state_tup[2]) not in visited:
        visited[(curr_state_tup[0],mpf(0),curr_state_tup[2])] = (curr_state_tup,"BS")
        q.append((curr_state_tup[0],mpf(0),curr_state_tup[2]))
    if curr_state_tup[2] > 0 and \
       (curr_state_tup[0],curr_state_tup[1],mpf(0)) not in visited:
        visited[(curr_state_tup[0],curr_state_tup[1],mpf(0))] = (curr_state_tup,"CS")
        q.append((curr_state_tup[0],curr_state_tup[1],mpf(0)))

    #transfer from tap/jug to jug
    rem = mpf(a_cap - curr_state_tup[0])
    if rem > 0:
        if (a_cap,curr_state_tup[1],curr_state_tup[2]) not in visited:
            visited[(a_cap,curr_state_tup[1],curr_state_tup[2])] = (curr_state_tup,"TA")
            q.append((a_cap,curr_state_tup[1],curr_state_tup[2]))
        min_tr = mpf(min(rem, curr_state_tup[1]))
        if min_tr > 0 and \
           (curr_state_tup[0]+min_tr,curr_state_tup[1]-min_tr,curr_state_tup[2]) not in visited:
            visited[(curr_state_tup[0]+min_tr,curr_state_tup[1]-min_tr,curr_state_tup[2])] = (curr_state_tup,"BA")
            q.append((curr_state_tup[0]+min_tr,curr_state_tup[1]-min_tr,curr_state_tup[2]))
        min_tr = mpf(min(rem, curr_state_tup[2]))
        if min_tr > 0 and \
           (curr_state_tup[0]+min_tr,curr_state_tup[1],curr_state_tup[2]-min_tr) not in visited:
            visited[(curr_state_tup[0]+min_tr,curr_state_tup[1],curr_state_tup[2]-min_tr)] = (curr_state_tup,"CA")
            q.append((curr_state_tup[0]+min_tr,curr_state_tup[1],curr_state_tup[2]-min_tr))

    rem = mpf(b_cap - curr_state_tup[1])
    if rem > 0:
        if (curr_state_tup[0],b_cap,curr_state_tup[2]) not in visited:
            visited[(curr_state_tup[0],b_cap,curr_state_tup[2])] = (curr_state_tup,"TB")
            q.append((curr_state_tup[0],b_cap,curr_state_tup[2]))
        min_tr = mpf(min(rem, curr_state_tup[0]))
        if min_tr > 0 and \
           (curr_state_tup[0]-min_tr,curr_state_tup[1]+min_tr,curr_state_tup[2]) not in visited:
            visited[(curr_state_tup[0]-min_tr,curr_state_tup[1]+min_tr,curr_state_tup[2])] = (curr_state_tup,"AB")
            q.append((curr_state_tup[0]-min_tr,curr_state_tup[1]+min_tr,curr_state_tup[2]))
        min_tr = mpf(min(rem, curr_state_tup[2]))
        if min_tr > 0 and \
           (curr_state_tup[0],curr_state_tup[1]+min_tr,curr_state_tup[2]-min_tr) not in visited:
            visited[(curr_state_tup[0],curr_state_tup[1]+min_tr,curr_state_tup[2]-min_tr)] = (curr_state_tup,"CB")
            q.append((curr_state_tup[0],curr_state_tup[1]+min_tr,curr_state_tup[2]-min_tr))

    rem = mpf(c_cap - curr_state_tup[2])
    if rem > 0:
        if (curr_state_tup[0],curr_state_tup[1],c_cap) not in visited:
            visited[(curr_state_tup[0],curr_state_tup[1],c_cap)] = (curr_state_tup,"TC")
            q.append((curr_state_tup[0],curr_state_tup[1],c_cap))
        min_tr = mpf(min(rem, curr_state_tup[0]))
        if min_tr > 0 and \
           (curr_state_tup[0]-min_tr,curr_state_tup[1],curr_state_tup[2]+min_tr) not in visited:
            visited[(curr_state_tup[0]-min_tr,curr_state_tup[1],curr_state_tup[2]+min_tr)] = (curr_state_tup,"AC")
            q.append((curr_state_tup[0]-min_tr,curr_state_tup[1],curr_state_tup[2]+min_tr))
        min_tr = mpf(min(rem, curr_state_tup[1]))
        if min_tr > 0 and \
           (curr_state_tup[0],curr_state_tup[1]-min_tr,curr_state_tup[2]+min_tr) not in visited:
            visited[(curr_state_tup[0],curr_state_tup[1]-min_tr,curr_state_tup[2]+min_tr)] = (curr_state_tup,"BC")
            q.append((curr_state_tup[0],curr_state_tup[1]-min_tr,curr_state_tup[2]+min_tr))

print("\nEnd main puzzle", datetime.now())

'''
My IBM Ponder This December '23 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/December2023.html
Sanandan Swaminathan, submitted November 30, 2023

Main puzzle (find one value of m for which f(m) is exactly 1000000):
m = 4313134 is a palindrome where f(4313134) = 1000000

Bonus * (list of all values of m where f(m) is exactly 1000000):
4310930, 4311298, 4312919, 4313134, 4313718

This short program counts the desired circles within the washer ring
region in the first quadrant, where the region is bounded by the concentric
circles of radii m and m+1. The program completed in 7 seconds for the main puzzle;
I constrained the search to palindromes in the range 4.31 million to 4.315 million
(based on results I saw with sporadic runs for some m values).
To avoid floats, I use a scaled grid where side length of equilateral triangle is 2
units, and I use radius squared rather than radius. Only the first quadrant of the
grid is used. The program looks to count the desired circles by traversing the grid
ines in a particular order. Consider the grid line through (m+1, 0), i.e. (2m+2,0) in
this setup with triangle side lengths of 2 units. This line makes an angle of 120 degrees
with the positive direction of the X-axis. First, the program traverses the triangular lattice
points on this grid line to find circles in the washer ring region. Then it moves to the parallel
grid line on the left which passes through (m, 0), i.e. (2m, 0) in this setup of side lengths 2.
It traverses this grid line starting from beyond the circle of radius
m. It repeats this process for every parallel grid line, right to left, to count
circles in the washer ring region, always trying to stay in the washer ring region.
Distinct circles are ensured by using a set to store the squared radii found.
I first tested the program for the given examples (m = 0, 1, 2, 3, 11, 42), and then
ran it for a few sporadic m values to narrow the range that I would need to search.
Thanks to the palindrome hint, the program took only 7 seconds to find a palindromic
answer.

I ran the same program for a range for the bonus * question. The function f(m) doesn’t
exhibit a smoothly non-decreasing behavior, sometimes fluctuating to materially smaller
function values for larger m. So I took an educated a guess at what range might cover
all m values that give f(m) = 1000000. The program ran for a couple of hours to find
the five m values for the bonus * search. If multiple cores can be spared for this search,
we can use multi threading and split the range. Mutex/semaphore/thread barriers not needed
as f(m) is independent for each m.
'''

from datetime import datetime

def count_circles(m):
    low = (2*m)**2
    high = (2*(m+1))**2
    x = (2*m) + 1
    myset = set()
    #in grid with triangle side length 2 (scaled), height-squared of lattice points make the sequence
    #3, 12, 27, 48, 75...
    ysquared = 3
    incr = 9
    #traverse chord that goes through m+1 and makes 120 degree angle with positive dir of X-axis
    while ysquared <= high:
        if x < 0:
            break
        curr = (x**2) + ysquared #radius squared of circle passing through this lattice point
        if curr > low and curr < high: #within the desired washer ring region
            myset.add(curr)
        x -= 1
        ysquared += incr
        incr += 6

    #travsere parallel chords left to right
    startx = (2*m) - 1
    startysq = 3
    startincr = 9
    while startx >= 0: #traverse each chord
        x = startx
        ysquared = startysq
        incr = startincr
        while True: #look for first point to start with on this chord
            curr = (x**2) + ysquared
            if curr > low:
                startx = x-2
                startysq = ysquared
                startincr = incr
                break
            ysquared += incr
            incr += 6
            x -= 1

        while True: #traverse this chord looking for intersections
            curr = (x**2) + ysquared
            if x < 0 or curr >= high:
                break
            myset.add(curr)
            x -= 1
            ysquared += incr
            incr += 6

    return len(myset)

#main puzzle: ran in around 7 secs
print(datetime.now())  
TARGET = 1000000
sol_found = False
#based on trial runs of count_circles(m) for some m values, we can quickly make
#an educated guess that the desired m value is in the 4.31 million ballpark
for p in range(4,10):
    for q in range(0,10):
        for r in range(0,10):
            for s in range(0,10):
                #for main, constrain the search to palindromes
                m = (p*(10**6)) + (q*(10**5)) + (r*(10**4)) + \
                    (s*(10**3)) + (r*(10**2)) + (q*10) + p
                #Change line below to try different m values to narrow
                #the search range further. Then, look in likely range.
                if m<4310000 or m > 4315000:
                    continue
                x = count_circles(m)
                if x == TARGET:
                    print("found an answer for main:",m)
                    sol_found = True
                    break
            if sol_found == True:
                break
        if sol_found == True:
            break
    if sol_found == True:
        break            
print(datetime.now())

#bonus puzzle: Note - will take a couple of hours to run to check 5k m values
m_list = []
#look in likely range based on runs for some m values
for m in range(4310000,4315000):
    x = count_circles(m)
    if x == TARGET:
        print(m)
        m_list.append(m)
    if m%100 == 0: #monitor progress
        print(m,x,len(m_list),datetime.now())
print("bonus answer:", m_list)
print("len", len(m_list))
print(datetime.now())

'''
#If multiple cores available for this, we can multi thread.
#No need for mutex/semaphore/thread barriers for this as
#the tasks are fully independent of each other.

import threading

def count_circles_range(mstart, mend, tgt):
    for m in range(mstart, mend):
        if count_circles(m) == tgt:
            print(datetime.now(), m)

print(datetime.now())
t1 = threading.Thread(target=count_circles_range, args=(4310920, 4310930, TARGET,))
t2 = threading.Thread(target=count_circles_range, args=(4310930, 4310940, TARGET,))
t3 = threading.Thread(target=count_circles_range, args=(4310940, 4310950, TARGET,))
t4 = threading.Thread(target=count_circles_range, args=(4310950, 4310960, TARGET,))
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()
print(datetime.now())
'''

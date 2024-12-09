/*
My IBM Ponder This November '24 challenge main and bonus * solutions
https://research.ibm.com/haifa/ponderthis/challenges/November2024.html
Sanandan Swaminathan, submitted November 12, 2024

To compile: gcc pondthisnov24_sol.c -o pondthisnov24_sol
To run: ./pondthisnov24_sol
Note: To run for bonus puzzle, change "tgt" variable in main() to 655, compile, and run.

An answer found for the main puzzle (144 * (V^2) = 128):
[ 280, 245, 137, 69, 217, 177 ]

An answer found for the bonus * puzzle (144 * (V^2) = 655):
[ 345, 252, 94, 245, 102, 9 ]

Due to the computation heavy nature of this puzzle, I decided to use C. The Cayley-Menger determinant 
(https://en.wikipedia.org/wiki/Cayley%E2%80%93Menger_determinant) is a convenient way to calculate the
volume of a tetrahedron from edge lengths (works for any n-dimensional simplex, actually).
144*(V^2) is half the value of the Cayley-Menger determinant for a tetrahedron, so the determinant value
needs to be 128*2 = 256 for the main puzzle, and 655*2 = 1310 for the bonus puzzle. We can iterate through
groups of 5 edge lengths of the tetrahedron. By setting the Cayley-Menger determinant to 256 for the main
puzzle (or 1310 for the bonus puzzle) and expanding the determinant, we can get a quartic equation for the 
6th edge length f. Conveniently, this reduces to a quadratic equation in x where x = f^2. The quadratic
equation can be solved with the quadratic formula, and f = sqrt(x). If either of the two positive values of
f (one for each x) is an integer, we have a solution for the puzzle. Note that there will be two positive
values for the 6th edge length f for any given group of 5 valid edge lengths and tetrahedron volume; for a 
base triangle containing edge lengths a, b, c, the face containing edge lengths a, d, e can be oriented in
two ways to get the same tetrahedron volume.

To iterate through sets of 5 edge lengths in a "reasonably" efficient manner, we can consider the face
having the top two longest edges of the 5 edges we are working with as the base of the tetrahedron. There 
will always be such a face since we are considering only 5 of the 6 edges. Even if the top two longest edges 
of the 6 edges of the tetrahedron happen to be opposite each other (not on the same face), any set of 5 edges 
will still have two longest among those 5 on the same face. Suppose a, b, c, d, e are 5 edge lengths of the 
tetrahedron, with a >= b >= c, d, e (b >= c, b >= d, b >= e). The edge length f that we are trying to determine 
could be any value (subject to triangle inequalities). We consider the triangle formed by a, b, c as the base. 
Let d be the third edge at the common vertex of a and b. Let e be the third edge at the common vertex of a and c.
Now, b has to  be at least floor(a/2) + 1 to ensure that b >= c. Also, d needs to be at least a - b + 1. If d 
was smaller, say d = a - b, then e would be at least a - d + 1 = a - (a - b) + 1 = b + 1. But b >= e according 
to our setup. Hence d needs to be at least a - b + 1. There's no relative order between c, d and e, and  f is 
the unknown edge we are trying to find. We also have the max value constraints governed by a >= b >= c, d, e, 
and the triangle inequalities for the faces. All these restrictions make the overall search more efficient by 
reducing the search space considerably (compared to the search space for a less restricted brute force approach). 
For any group of a, b, c, d, e that we are iterating, we can solve the Cayley-Menger determinant quartic equation 
(adjusted to quadractic). We will end up with two positive values for the sixth edge length f. If either of the 
values is an integer, a solution for the puzzle is found. Search for the main puzzle completed in about 2.5 
minutes, and the search for the bonus puzzle completed in about 7 minutes. Of course, if desired, one can 
multi-thread this program or run it with multiple processes/compute nodes by splitting the search in batches 
based on edge length a. For each value of a, the search is independent of the search with any other value of a.
*/

#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <math.h>
#include <stdbool.h>

int main()
{
int tgt = 128; // set to 128 for main puzzle, 655 for bonus * puzzle
time_t t = time(NULL);
struct tm *tm = localtime(&t);
printf("START %s Target: %d\n", asctime(tm), tgt);
bool sol_found = false;
int a = 3; //other than the example given, no solution for main or bonus can exist with longest edge length 2 or less
while (1 == 1){
    if (a%100 == 0){
        t = time(NULL);
        tm = localtime(&t);
        printf("%s progress: a = %d\n", asctime(tm), a);
    }
    long long asq = a*a;
    for (int b = (a/2)+1; b < a+1; b++){
        long long bsq = b*b;
        for (int c = a-b+1; c<b+1; c++){
            long long csq = c*c;
            for (int d = a-b+1; d < b+1; d++){
                long long dsq = d*d;
                for (int e = a-d+1; e <b+1; e++){
                    long long esq = e*e;
                    /*
                    Compute pieces needed to solve the Cayley-Menger quartic equation for edge length f.
                    Since the equation contains only f^4 and f^2 terms for f, we can treat it as a quadratic
                    equation, solve for f^2, take the positive values, and take their positive square roots to
                    find f values. If either of the two positive f values is an integer, we have a solution.
                    */
                    long long abc = asq+bsq-csq;
                    long long ade = asq+dsq-esq;
                    long long bdsq = bsq+dsq;
                    long long bq = (abc*ade) - (2*asq*(bdsq));
                    long long cq = (asq*(bdsq*bdsq)) + (bsq*(ade*ade)) + (dsq*(abc*abc)) - (4*asq*bsq*dsq) - (abc*ade*bdsq) + tgt;
                    long long discrim = (bq*bq) - (4*asq*cq);
                    if (discrim >= 0){
                        long long discrimroot = (long long)(sqrt(discrim));
                        if (discrimroot * discrimroot == discrim){
                            long long numer;
			                for (int discsign = -1; discsign < 2; discsign += 2){
				                numer = (discsign*discrimroot) - bq;
                            	if (numer > 0){
                               	    long long denom = 2*asq;
                                    if (numer%denom == 0){
                                        double num = numer/denom;
                                        long long f = (long long)(sqrt(num));
                                        if (f*f == num){
        			                        t = time(NULL);
        				                    tm = localtime(&t);
                                            printf("%s FOUND a solution for target %d: [ %d, %d, %d, %d, %d, %llu ]\n", asctime(tm),tgt,a,b,c,d,e,f);
				                            sol_found = true;	
					                        break;
                                       }
                                    }
                            	}
                            }
                        }
                    }
		            if (sol_found == true){
			            break;
		            }
                } // end e loop
                if (sol_found == true){
			        break;
                }
            } // end d loop
            if (sol_found == true){
			    break;
            }
        } // end c loop
	    if (sol_found == true){
            break;
        }
    } // end b loop
if (sol_found == true){
    break;
}
a++;
} // end infinite a loop

t = time(NULL);
tm = localtime(&t);
printf("DONE %s", asctime(tm));

return 0;
}

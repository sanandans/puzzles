/*
IBM Ponder This challenge and bonus *, Jan 21
https://research.ibm.com/haifa/ponderthis/challenges/January2021.html
Sanandan Swaminathan, submitted Jan 1, 2021

Here are the solutions I found for the January 2021 IBM Ponder This challenge (for each grid, the origin is at the top-left corner and the robot starts in that cell facing upwards, as in your examples )...
For the main question, i.e. N=50, one solution I found for placing the two "B" cells in the 50x50 grid is [(34,0), (1,48)].
For the bonus '*' question, i.e. N=100, one solution I found for placing two "B" cells in the 100x100 grid is [(82,0), (26,35)].
I verified the above solutions for N=50 and N=100 with a short program that simply follows the given rules with the two "B" cells in the fixed spots, and completes the vaccination. I'm still trying to determine the answer for the double bonus '**' question, i.e. minimum N such that two "B" cells do not suffice for it. All I can say so far is that the '**' answer is above N=121  since I've found solutions for N=2 through N=121 with two "B" cells.

My solution approach: I wrote a C program that loops through different combinations of two "B" cells on an NxN grid. It breaks out to a different combination as soon as it's detected that the robot is in a cycle of cells that it can't escape from (with the vaccination task not having been completed). A cycle could be a simple loop of a whole row or a whole column filled with "2" values when the robot is walking that loop. Intersection of two loops full of "2" values with a "B" cell at the intersection also forms a cycle. A cycle consisting of three loops with one "B" cell at one intersection and another "B" cell at another intersection is also possible. A cycle is also possible with two parallel loops (horizontal or vertical), with a bridge of cells with "2" values between the two parallel loops, with the bridge bookended by "B" cells. Since the grid wraps around in horizontal and vertical directions, that had to be taken into account and also the direction of travel in some scenarios. If all but the two "B" cells reach a "2" state, the program reports the solution. The program found a solution [(34,0), (1,48)] for a 50x50 grid in 8 seconds.

I then ran the program in a loop for N=2 through N=100 to determine if N=100 could be solved with two "B" cells, and also to determine if there was any N in that range for which two "B" cells don't suffice. The program ran fast for most N values, but it did take upto a few minutes for some N (not unexpected). It found a solution for all N upto 100 (and later, solutions for upto N=121). It completed within seconds for N=100 itself, and found a solution [(82,0), (26,35)] for a 100x100 grid.

For the bonus '**" question, I let the program run for N > 100 to determine the minimum N for which two "B" cells don't suffice. Of course, the program is running much slower for large N. I'm not sure if it's possible for two "B" cells to not work for some N but work for a higher N. Since I'm not sure whether there is a clean upper bound upto which two "B" cells suffice and beyond which they definitely don't, I didn't use a binary search type of approach to narrow down to the minimum N. As of the time of writing this email, the program has reported solutions with two "B" cells for upto N=121. I separately ran it for N=150 and it found a solution, so I'm not sure yet what is the smallest N for which it won't find a solution. I'll keep the program running, but I might need to think of some optimization or symmetry for the bonus '**' question.

*/

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <time.h>

#include <math.h>

#include <stdbool.h>

 

/* To compile: gcc -o robovacfinal robovacfinal.c -lm

   Usage: ./robovacfinal > robovacfinal.log &

   Author: Sanandan

*/

 

int main() {

unsigned short n=200;

unsigned short firstbx,firstby,secondbx,secondby,dir,tempb,tempcnt;

unsigned long firstb,secondb,twocnt;

short posx,posy,trial;

unsigned short grid[n][n];

unsigned short rowcnt[n];

unsigned short colcnt[n];

bool solfound = false;

bool bridgefound;

time_t rightnow = time(NULL);

unsigned long cnt = 0;

 

printf("Started at %s", ctime(&rightnow)); printf("n is %hu\n", n); fflush(stdout);

 

for (firstb=0; firstb <= (n*n) -2; firstb++) {

  firstbx = firstb%n;

  firstby = firstb/n;

 

  for (secondb=firstb+1; secondb <= (n*n) -1; secondb++)

   {

    memset(grid, 0, n*n*sizeof(grid[0][0]));

    secondbx = secondb%n;

    secondby = secondb/n;

    grid[firstby][firstbx] = 3;

    grid[secondby][secondbx] = 3;

    twocnt = 0;

    memset(rowcnt, 0, n*sizeof(rowcnt[0]));

    memset(colcnt, 0, n*sizeof(colcnt[0]));

    posx=0;

    posy=0;

    dir=0; //0 for up, 1 for down, 2 for left, 3 for right

 

    cnt++;

    if (cnt%1000000 == 0){

      cnt=0;

     rightnow = time(NULL);

     printf("Continung at %s", ctime(&rightnow));

     printf("n is %hu, firstb (%hu,%hu), secondb (%hu,%hu)\n", n,firstbx,firstby,secondbx,secondby);

    fflush(stdout);

    }

   

    while (true)

     {

      if ( ((dir==0||dir==1) && colcnt[posx]==n) || ((dir==2||dir==3) && rowcnt[posy]==n) )

              break;

 

      if (grid[posy][posx] == 0) {

        grid[posy][posx] = 1;

              if (dir == 0)

                dir = 3;

              else if (dir == 1)

                dir = 2;

              else if (dir == 2)

                dir = 0;

              else

                dir = 1;

      }

      else if (grid[posy][posx] == 1) {

              grid[posy][posx] = 2;

              twocnt++;

              if (twocnt == (n*n) -2) {

                rightnow = time(NULL);

                printf("Solution found at %s", ctime(&rightnow));

                printf("n is %hu, firstb (%hu,%hu), secondb (%hu,%hu)\n",n,firstbx,firstby,secondbx,secondby);

          fflush(stdout);

                solfound = true;

                break;

        }

              colcnt[posx] = colcnt[posx] + 1;

              rowcnt[posy] = rowcnt[posy] + 1;

 

              if (rowcnt[posy] >= n-2){

                tempcnt=0;

                tempb=0;

                if (firstby==posy){ tempcnt++; tempb=1;}

                if (secondby==posy){ tempcnt++; tempb=2;}

                if (tempcnt==2 && colcnt[firstbx]==n-1 && colcnt[secondbx]==n-1){

                  rowcnt[posy]=n;

                  colcnt[firstbx]=n;

                  colcnt[secondbx]=n;

                }

                if (tempcnt==1 && rowcnt[posy]==n-1)

                  if( tempb==1 )

              if( colcnt[firstbx]==n-1 ){

                             rowcnt[posy]=n;

                             colcnt[firstbx]=n;

                    }      

                    else if ( colcnt[firstbx]==n-2 && secondbx==firstbx && rowcnt[secondby]==n-1 ){

                             rowcnt[posy]=n;

                             colcnt[firstbx]=n;

                             rowcnt[secondby]=n;

                    }      

                  else if( tempb==2 )

                    if ( colcnt[secondbx]==n-1 ){

                             rowcnt[posy]=n;

                colcnt[secondbx]=n;

                    }

                    else if ( colcnt[secondbx]==n-2 && firstbx==secondbx && rowcnt[firstby]==n-1 ){

                             rowcnt[posy]=n;

                      colcnt[secondbx]=n;

                             rowcnt[firstby]=n;

                    }

              }

 

              if (colcnt[posx] >= n-2 && tempcnt!=2){

                tempcnt=0;

                tempb=0;

                if (firstbx==posx){ tempcnt++; tempb=1;}

                if (secondbx==posx){ tempcnt++; tempb=2;}

                if (tempcnt==2 && rowcnt[firstby]==n-1 && rowcnt[secondby]==n-1){

                  colcnt[posx]=n;

                  rowcnt[firstby]=n;

                  rowcnt[secondby]=n;

                }

                if (tempcnt==1 && colcnt[posx]==n-1)

                  if( tempb==1 )

              if( rowcnt[firstby]==n-1 ){

                             colcnt[posx]=n;

                      rowcnt[firstby]=n;

                    }      

                    else if ( rowcnt[firstby]==n-2 && secondby==firstby && colcnt[secondbx]==n-1 ){

                             colcnt[posx]=n;

                             rowcnt[firstby]=n;

                             colcnt[secondbx]=n;

                    }      

                  else if( tempb==2 )

                    if ( rowcnt[secondby]==n-1 ){

                             colcnt[posx]=n;

                             rowcnt[secondby]=n;

                    }

                    else if ( rowcnt[secondby]==n-2 && firstby==secondby && colcnt[firstbx]==n-1 ){

                             colcnt[posx]=n;

                             rowcnt[secondby]=n;

                             colcnt[firstbx]=n;

                    }

                }

 

              if (dir == 0)

                dir = 2;

              else if (dir == 1)

                dir = 3;

              else if (dir == 2)

                dir = 1;

              else

                dir = 0;

      }

      else if (grid[posy][posx] == 3) {

        if ( colcnt[posx]>=n-1 && rowcnt[posy]>=n-1 )

          break;

 

              if (dir == 0)

                dir = 2;

              else if (dir == 1)

                dir = 3;

              else if (dir == 2)

                dir = 1;

              else

                dir = 0;

             

              bridgefound=false;

              if (posy==firstby && firstby==secondby && colcnt[firstbx]>=n-1 && colcnt[secondbx]>=n-1){

                if (dir==2){

                  trial=posx-1;

                  if (trial<0)

                    trial=n-1;

                  while (grid[posy][trial]!= 0 && grid[posy][trial]!= 1){

                    if (grid[posy][trial]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial-1;

                    if (trial<0)

                trial=n-1;

                  }

                }

                else if (dir==3){

                  trial=posx+1;

                 if (trial>n-1)

                    trial=0;

                  while (grid[posy][trial]!= 0 && grid[posy][trial]!= 1){

                    if (grid[posy][trial]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial+1;

                    if (trial>n-1)

                trial=0;

                  }

                }

              }

              else if (posx==firstbx && firstbx==secondbx && rowcnt[firstby]>=n-1 && rowcnt[secondby]>=n-1){

                if (dir==0){

                  trial=posy-1;

                  if (trial<0)

                    trial=n-1;

                  while (grid[trial][posx]!= 0 && grid[trial][posx]!= 1){

                    if (grid[trial][posx]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial-1;

                    if (trial<0)

                trial=n-1;

                  }

                }

                else if (dir==1){

                  trial=posy+1;

                 if (trial>n-1)

                    trial=0;

                  while (grid[trial][posx]!= 0 && grid[trial][posx]!= 1){

                    if (grid[trial][posx]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial+1;

                    if (trial>n-1)

                trial=0;

                  }

                }

              }

 

              if (bridgefound==true)

                break;

      }

 

      if (dir == 0) {

              posy--;

              if (posy < 0)

                posy = n-1;

      }

      else if (dir == 1) {

              posy++;

              if (posy > n-1)

                posy = 0;

      }

      else if (dir == 2) {

              posx--;

              if (posx < 0)

                posx = n-1;

      }

      else {

              posx++;

              if (posx > n-1)

                posx = 0;

      }

   

    } //end while

 

    if (solfound == true)

              break;

 

  } //end for secondB

 

  if (solfound == true)

    break;

 

} //end for firstB

 

if (solfound==false){

  rightnow = time(NULL);

  printf("No solution found at %s\n", ctime(&rightnow));

  fflush(stdout);

}

 

return 0;

} //end main

 

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <time.h>

#include <math.h>

#include <stdbool.h>

 

/* To compile: gcc -o robocheck robocheck.c -lm

   Usage: ./robocheck > robocheck.log &

   Author: Sanandan

*/

 

int main() {

unsigned short n=50;

unsigned short grid[n][n];

time_t rightnow = time(NULL);

unsigned long cnt = 0;

unsigned long twocnt = 0;

unsigned short dir,i,j;

short posx,posy;

memset(grid, 0, n*n*sizeof(grid[0][0])); grid[0][34]=3; grid[48][1]=3; posx=0; posy=0; dir=0; //0 for up, 1 for down, 2 for left, 3 for right

 

printf("Started at %s", ctime(&rightnow)); fflush(stdout);

 

    while (true)

     {

 

      if (grid[posy][posx] == 0) {

        grid[posy][posx] = 1;

              if (dir == 0)

                dir = 3;

              else if (dir == 1)

                dir = 2;

              else if (dir == 2)

                dir = 0;

              else

                dir = 1;

      }

      else if (grid[posy][posx] == 1) {

              grid[posy][posx] = 2;

              twocnt++;

              if (twocnt == (n*n) -2) {

               rightnow = time(NULL);

                printf("Done at %s", ctime(&rightnow));

                printf("num steps %lu\n", cnt);

          fflush(stdout);

                break;

        }

 

              if (dir == 0)

                dir = 2;

              else if (dir == 1)

                dir = 3;

              else if (dir == 2)

                dir = 1;

              else

                dir = 0;

      }

      else if (grid[posy][posx] == 3) {

              if (dir == 0)

                dir = 2;

              else if (dir == 1)

                dir = 3;

              else if (dir == 2)

                dir = 1;

              else

                dir = 0;

 

      }

 

      if (dir == 0) {

              posy--;

              if (posy < 0)

                posy = n-1;

      }

      else if (dir == 1) {

              posy++;

              if (posy > n-1)

                posy = 0;

      }

      else if (dir == 2) {

              posx--;

              if (posx < 0)

                posx = n-1;

      }

      else {

              posx++;

              if (posx > n-1)

                posx = 0;

      }

      cnt++;

    } //end while

 

for(i=0;i<n;i++){

for(j=0;j<n;j++){

printf("%hu,",grid[i][j]);

}

printf("\n");

}

printf("n %hu, twocnt %lu, posx %hi, posy %hi, dir %hu\n",n,twocnt,posx,posy,dir);

 

return 0;

} //end main

 

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#include <time.h>

#include <math.h>

#include <stdbool.h>

 

/* To compile: gcc -o robovacall robovacall.c -lm

   Usage: ./robovacall > robovacall.log &

   Author: Sanandan

*/

 

int main() {

unsigned short n;

unsigned short firstbx,firstby,secondbx,secondby,dir,tempb,tempcnt;

unsigned long firstb,secondb,twocnt;

short posx,posy,trial;

bool solfound = false;

bool bridgefound;

time_t rightnow = time(NULL);

unsigned long cnt = 0;

 

printf("Started at %s", ctime(&rightnow)); fflush(stdout);

 

//for (n=2;n<101;n++) {

n=101;

while (n>100){ //solutions found for N=2 through N=100 before solfound=false; cnt=0; unisgned short grid[n][n]; unisgned short rowcnt[n]; unisgned short colcnt[n];

 

for (firstb=0; firstb <= (n*n) -2; firstb++) {

  firstbx = firstb%n;

  firstby = firstb/n;

 

  for (secondb=firstb+1; secondb <= (n*n) -1; secondb++)

   {

    memset(grid, 0, n*n*sizeof(grid[0][0]));

    secondbx = secondb%n;

    secondby = secondb/n;

    grid[firstby][firstbx] = 3;

    grid[secondby][secondbx] = 3;

    twocnt = 0;

    memset(rowcnt, 0, n*sizeof(rowcnt[0]));

    memset(colcnt, 0, n*sizeof(colcnt[0]));

    posx=0;

    posy=0;

    dir=0; //0 for up, 1 for down, 2 for left, 3 for right

 

    cnt++;

    if (cnt%1000000 == 0){

     cnt=0;

     rightnow = time(NULL);

     printf("Continung at %s", ctime(&rightnow));

     printf("Attempt is at (%lu,%lu), n is %hu\n",firstb,secondb,n);

     fflush(stdout);

    }

   

    while (true)

     {

      if ( ((dir==0||dir==1) && colcnt[posx]==n) || ((dir==2||dir==3) && rowcnt[posy]==n) )

              break;

 

      if (grid[posy][posx] == 0) {

        grid[posy][posx] = 1;

              if (dir == 0)

                dir = 3;

              else if (dir == 1)

                dir = 2;

              else if (dir == 2)

                dir = 0;

              else

                dir = 1;

      }

      else if (grid[posy][posx] == 1) {

              grid[posy][posx] = 2;

              twocnt++;

              if (twocnt == (n*n) -2) {

                rightnow = time(NULL);

                printf("At %s", ctime(&rightnow));

                printf("solution found for n %hu, firstb (%hu,%hu), secondb (%hu,%hu)\n",n,firstbx,firstby,secondbx,secondby);

          fflush(stdout);

                solfound = true;

                break;

        }

              colcnt[posx] = colcnt[posx] + 1;

              rowcnt[posy] = rowcnt[posy] + 1;

 

              if (rowcnt[posy] >= n-2){

                tempcnt=0;

                tempb=0;

                if (firstby==posy){ tempcnt++; tempb=1;}

                if (secondby==posy){ tempcnt++; tempb=2;}

                if (tempcnt==2 && colcnt[firstbx]==n-1 && colcnt[secondbx]==n-1){

                  rowcnt[posy]=n;

                  colcnt[firstbx]=n;

                  colcnt[secondbx]=n;

                }

                if (tempcnt==1 && rowcnt[posy]==n-1)

                  if( tempb==1 )

              if( colcnt[firstbx]==n-1 ){

                             rowcnt[posy]=n;

                             colcnt[firstbx]=n;

                    }      

                    else if ( colcnt[firstbx]==n-2 && secondbx==firstbx && rowcnt[secondby]==n-1 ){

                             rowcnt[posy]=n;

                             colcnt[firstbx]=n;

                            rowcnt[secondby]=n;

                    }      

                  else if( tempb==2 )

                    if ( colcnt[secondbx]==n-1 ){

                             rowcnt[posy]=n;

                colcnt[secondbx]=n;

                    }

                    else if ( colcnt[secondbx]==n-2 && firstbx==secondbx && rowcnt[firstby]==n-1 ){

                             rowcnt[posy]=n;

                      colcnt[secondbx]=n;

                             rowcnt[firstby]=n;

                    }

              }

 

              if (colcnt[posx] >= n-2 && tempcnt!=2){

                tempcnt=0;

                tempb=0;

                if (firstbx==posx){ tempcnt++; tempb=1;}

                if (secondbx==posx){ tempcnt++; tempb=2;}

                if (tempcnt==2 && rowcnt[firstby]==n-1 && rowcnt[secondby]==n-1){

                  colcnt[posx]=n;

                  rowcnt[firstby]=n;

                  rowcnt[secondby]=n;

                }

                if (tempcnt==1 && colcnt[posx]==n-1)

                  if( tempb==1 )

              if( rowcnt[firstby]==n-1 ){

                             colcnt[posx]=n;

                      rowcnt[firstby]=n;

                    }      

                    else if ( rowcnt[firstby]==n-2 && secondby==firstby && colcnt[secondbx]==n-1 ){

                             colcnt[posx]=n;

                             rowcnt[firstby]=n;

                             colcnt[secondbx]=n;

                    }      

                  else if( tempb==2 )

                    if ( rowcnt[secondby]==n-1 ){

                             colcnt[posx]=n;

                             rowcnt[secondby]=n;

                    }

                    else if ( rowcnt[secondby]==n-2 && firstby==secondby && colcnt[firstbx]==n-1 ){

                             colcnt[posx]=n;

                             rowcnt[secondby]=n;

                             colcnt[firstbx]=n;

                    }

                }

 

              if (dir == 0)

                dir = 2;

              else if (dir == 1)

                dir = 3;

              else if (dir == 2)

                dir = 1;

              else

                dir = 0;

      }

      else if (grid[posy][posx] == 3) {

        if ( colcnt[posx]>=n-1 && rowcnt[posy]>=n-1 )

          break;

 

              if (dir == 0)

                dir = 2;

              else if (dir == 1)

                dir = 3;

              else if (dir == 2)

                dir = 1;

              else

                dir = 0;

             

              bridgefound=false;

              if (posy==firstby && firstby==secondby && colcnt[firstbx]>=n-1 && colcnt[secondbx]>=n-1){

                if (dir==2){

                  trial=posx-1;

                  if (trial<0)

                    trial=n-1;

                  while (grid[posy][trial]!= 0 && grid[posy][trial]!= 1){

                    if (grid[posy][trial]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial-1;

                    if (trial<0)

                trial=n-1;

                  }

                }

                else if (dir==3){

                  trial=posx+1;

                  if (trial>n-1)

                    trial=0;

                  while (grid[posy][trial]!= 0 && grid[posy][trial]!= 1){

                    if (grid[posy][trial]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial+1;

                    if (trial>n-1)

                trial=0;

                  }

                }

              }

              else if (posx==firstbx && firstbx==secondbx && rowcnt[firstby]>=n-1 && rowcnt[secondby]>=n-1){

                if (dir==0){

                  trial=posy-1;

                  if (trial<0)

                    trial=n-1;

                  while (grid[trial][posx]!= 0 && grid[trial][posx]!= 1){

                    if (grid[trial][posx]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial-1;

                    if (trial<0)

                trial=n-1;

                  }

                }

                else if (dir==1){

                  trial=posy+1;

                  if (trial>n-1)

                    trial=0;

                  while (grid[trial][posx]!= 0 && grid[trial][posx]!= 1){

                    if (grid[trial][posx]==3){

                             bridgefound=true;

                             break;

                    }

                    trial=trial+1;

                    if (trial>n-1)

                trial=0;

                  }

                }

              }

 

              if (bridgefound==true)

                break;

      }

 

      if (dir == 0) {

              posy--;

              if (posy < 0)

                posy = n-1;

      }

      else if (dir == 1) {

              posy++;

              if (posy > n-1)

                posy = 0;

      }

      else if (dir == 2) {

              posx--;

              if (posx < 0)

                posx = n-1;

      }

      else {

              posx++;

              if (posx > n-1)

                posx = 0;

      }

   

    } //end while

 

    if (solfound == true)

              break;

 

  } //end for secondB

 

  if (solfound == true)

    break;

 

} //end for firstB

 

if (solfound==false){

  rightnow = time(NULL);

  printf("At %s", ctime(&rightnow));

  printf("No solution found for n %hu.\n",n);

  fflush(stdout);

  break;

}

 

n++;

 

} //end while of n

 

rightnow = time(NULL);

printf("At %s", ctime(&rightnow));

printf("Done.\n");

fflush(stdout);

 

return 0;

} //end main


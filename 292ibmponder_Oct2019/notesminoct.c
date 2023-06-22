/*
IBM Ponder This challenge Oct 19
https://research.ibm.com/haifa/ponderthis/challenges/October2019.html
Sanandan Swaminathan, submitted Oct 2, 2019

One solution I found for the October 2019 challenge that maximizes the desired probability is {1, 2, 12, 16, 48}. The desired conditional 
probability for this set of denominations is about 29.07 %.

I tweaked my C program (which uses dynamic programming approach) that I wrote for the September 2019 challenge. The program run completed 
very quickly.

The desired conditional probability works out to 100 divided by sum of squares of counts of amounts made by each distinct set of notes 
for a given set of 5 denominations. That sum of squares has to be minimum to maximize the desired conditional probability. I took the US 
denominations as baseline; the sum of squares is 476. If a lower sum of squares is found for some set of denominations, that sum and set 
of denominations become the new baseline for further iterations. As with my September program, the revised program loops through 
different sets containing denomination 1 and four other denominations, and considers all amounts from 2 through 99. The second 
denomination is constrained to a maximum of 22 since any higher second denomination would cause the sum of squares to exceed 476. During 
the dynamic programming based search, it checks if more than one distinct minimal set of notes could be used to make an amount. If true, 
the corresponding set of five denominations is rejected. The program also moves to a fresh set of denominations as soon as the sum of
squares for the current set being processed is greater than or equal to the current baseline. I didn't try any other performance 
improvements apart from the above.

After exhausting the sets of 5 denominations, the program exited with the best solution found {1, 2, 12, 16, 48} with desired conditional 
probability being 29.07 %.

*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>

/* gcc -o notesminoct notesminoct.c -lm
   ./notesminoct > logfilename &
*/

int main() {

time_t rightnow = time(NULL);
short minnotes[100]; //minimum number of notes needed for each amount
minnotes[0] = 0; //zero amount made with no notes
minnotes[1] = 1; //amount 1 made with denomination 1
short highest_denomindex[100]; //index of highest denomination used in set of notes for each amount
highest_denomindex[0] = -1;
highest_denomindex[1] = 4;
bool dupefound;
long progresscount = 0;
short e,f,g,h,amount,mincount,i,j,temp,highestnoteindex,a,altsum,sum;
//sets of distinct notes can range from 00000 to 11111 where each bit represents a denomination
//below array stores running count of amounts made minimally with each distinct set of notes
short denomsetscnt[32];

short denoms[5]; //only 5 denominations, one of them being 1 so that amount 1 can be made
short bestdenoms[5] = {1,5,10,20,50}; //using US denoms as baseline
int best_sum_counts_squares = 476; //find solutions smaller than this to maximize desired probability
short sum_counts_squares;
bool max_exceeded;
denoms[4] = 1;
short alt_notes[5]; //array used to decide if another combo of notes that makes the same amount minimally is the same as another set or not
short notes[5]; //array to store current minimal set of notes for an amount

printf("%s Started\n", ctime(&rightnow));
fflush(stdout);

for(e = 2; e <= 22; e++) //if second denomination is 23 or more, set {1} itself would cause less probability than US baseline
{
denoms[3] = e;
for(f = e+1; f <= 97; f++)
{
denoms[2] = f;
for(g = f+1; g <= 98; g++)
{
denoms[1] = g;
for(h = g+1; h <= 99; h++)
{
denoms[0] = h;

progresscount = progresscount +1;
if (progresscount%100000 == 0) {
 rightnow = time(NULL);
 printf("%s Progress\n", ctime(&rightnow));
 printf("%li ", progresscount);
 for(i = 0; i <= 4; i++) {
   printf("%hi ", denoms[i]);
 }
 printf("%d\n", best_sum_counts_squares);
 fflush(stdout);
}

memset(denomsetscnt, 0, 32*sizeof(denomsetscnt[0]));
denomsetscnt[16] = 1; //amount 1 is made with notes set 00001 which we consider equivalent to index 16 and increment the count of amounts using that set
denomsetscnt[0] = 1; //amount 0 is made with notes set 00000 which is equivalent to index 0 and increment the count of amounts using that set
sum_counts_squares = 2; //sum of squares for sets {{0},{0}} and {{1},{1}}
max_exceeded = false;

for(amount = 2; amount <= 99; amount++) {

    mincount = 100;
    for(i = 0; i <= 4; i++) {
      if(denoms[i] <= amount) {
        temp = 1 + minnotes[amount - denoms[i]];
        if(temp < mincount) { //this is the latest minimal set for this amount
                mincount = temp;
                highestnoteindex = i;
                dupefound = false; //this is a new minimal
                memset(notes, 0, 5*sizeof(notes[0]));
                notes[i] = 1;
                a = amount - denoms[i];
                while(a > 0) {
                  notes[highest_denomindex[a]] = 1;
                  a = a - denoms[highest_denomindex[a]];
                }
        }
        else if(temp == mincount) { //this could be just another ordering of current minimal set or a new set of notes
                memset(alt_notes, 0, 5*sizeof(alt_notes[0]));
                alt_notes[i] = 1;
                a = amount - denoms[i];
                while(a > 0) {
                  alt_notes[highest_denomindex[a]] = 1;
                  a = a - denoms[highest_denomindex[a]];
                }

                altsum=0;
                sum=0;
                for (j=0; j<=4; j++) {
                        altsum = altsum + (alt_notes[j] * (short)pow(2,j));
                        sum = sum + (notes[j] * (short)pow(2,j));
                }

                if (altsum != 0 && altsum != sum) { //this could potentially be another minimal set of notes
                        dupefound = true; //don't break as a minimum lower than this could be found
                }
        }
      } // if denoms[i] <= amount
    }  // i loop

    if (dupefound == true) { //we need to restart with a fresh set of 5 denominations
        break; // from amount loop
    }
    else {
        minnotes[amount] = mincount;
        highest_denomindex[amount] = highestnoteindex;
        sum=0;
        for (j=0; j<=4; j++) {
                sum = sum + (notes[j] * (short)pow(2,j));
        }

        denomsetscnt[sum] = denomsetscnt[sum] + 1;
        sum_counts_squares = sum_counts_squares + (2*denomsetscnt[sum]) -1;
        if (sum_counts_squares >= best_sum_counts_squares) {
                max_exceeded = true;
                break; //from amount loop
        }
    }

} // amount loop

if (dupefound == false && max_exceeded == false) {
        bestdenoms[1] = e;
        bestdenoms[2] = f;
        bestdenoms[3] = g;
        bestdenoms[4] = h;
        best_sum_counts_squares = sum_counts_squares;
}

} // h loop
} // g loop
} // f loop
} // e loop

rightnow = time(NULL);
printf("%s Best Solution found\n", ctime(&rightnow));
printf("Progress count %li\n", progresscount);
for(i = 0; i <= 4; i++) {
  printf("%hi ", bestdenoms[i]);
}
printf("\n Best sum of counts squares is %d\n", best_sum_counts_squares);
printf("Max probability percentage is %f\n", (double)10000/best_sum_counts_squares);
fflush(stdout);

return 0;
}


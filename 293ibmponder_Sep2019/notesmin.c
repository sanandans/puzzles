/* IBM Ponder This Sep 19
 https://research.ibm.com/haifa/ponderthis/challenges/September2019.html
 Sanandan Swaminathan, submitted Sep 18, 2019

One solution I found for the condition that there can be only five denominations is {1, 2, 4, 8, 62}. This set gives the desired 
probability of exactly 4%.

First I tried to do this with pen and paper using various sequences including geometric progressions, but then wrote a small C program 
that uses the dynamic programming approach. The program found the above solution almost instantaneously.

The program loops through different sets containing denomination 1 and four other denominations, and considers all amounts from 2 through 
99. During the dynamic programming based search, it checks if more than one distinct minimal set of notes could be used to make an 
amount. The corresponding set of five denominations is rejected. When a unique minimal set of notes is found for an amount, the program 
increments an array of counters that keeps track of how many amounts are made minimally by each set of notes. If all amounts get 
processed for a given set of five denominations, the program computes the total desired permutations using the array of counters, and 
checks if we got 396 permutations. If not, it tries again with a new set of five denominations. The program exited on finding the first 
solution {1, 2, 4, 8, 62}.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>

/* gcc -o notesmin notesmin.c -lm
   ./notesmin > logfilename &1
*/

int main() {

time_t rightnow = time(NULL);
short minnotes[100]; //minimum number of notes needed for each amount
minnotes[0] = 0; //zero amount made with no notes
minnotes[1] = 1; //amount 1 made with denomination 1
short highest_denomindex[100]; //index of highest denomination used in set of notes for each amount
highest_denomindex[0] = -1;
highest_denomindex[1] = 4;
bool solutionfound = false;
bool dupefound;
long progresscount = 0;
short e,f,g,h,amount,mincount,i,j,temp,highestnoteindex,a,altsum,sum,permsum;
//sets of distinct notes can range from 00000 to 11111 where each bit represents a denomination
//below array stores running count of amounts made minimally with each distinct set of notes
short denomsetscnt[32];

short denoms[5]; //only 5 denominations, one of them being 1 so that amount 1 can be made
denoms[4] = 1;
short alt_notes[5]; //array used to decide if another combo of notes that makes the same amount minimally is the same as another set or not
short notes[5]; //array to store current minimal set of notes for an amount

printf("%s Started\n", ctime(&rightnow));
fflush(stdout);

for(e = 2; e <= 96; e++)
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
if (progresscount%1000000 == 0) {
 printf("%s Progress\n", ctime(&rightnow));
 printf("%li ", progresscount);
 for(i = 0; i <= 4; i++) {
   printf("%hi ", denoms[i]);
 }
 printf("\n");
 fflush(stdout);
}

memset(denomsetscnt, 0, 32*sizeof(denomsetscnt[0]));
denomsetscnt[16] = 1; //amount 1 is made with notes set 00001 which we consider equivalent to index 16 and increment the count of amounts using that set

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
                        dupefound = true;
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
    }

} // amount loop

if (dupefound == false) {
        permsum = 0;
        for(i = 1; i <= 31; i++) {
                permsum = permsum + ( denomsetscnt[i] * (denomsetscnt[i] -1) );
                if (permsum > 396)
                        break; // from this permsum loop
        }

        if (permsum == 396) {
                printf("%s Solution found\n", ctime(&rightnow));
                printf("%li ", progresscount);
                for(i = 0; i <= 4; i++) {
                  printf("%hi ", denoms[i]);
                }
                printf("\n");
                fflush(stdout);
                solutionfound = true;
        }
}
if (solutionfound == true)
        break;
} // h loop
if (solutionfound == true)
        break;
} // g loop
if (solutionfound == true)
        break;
} // f loop
if (solutionfound == true)
        break;
} // e loop

return 0;
}


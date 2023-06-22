/*
IBM Ponder This challenge main and bonus *, Dec 21
https://research.ibm.com/haifa/ponderthis/challenges/December2021.html
Sanandan Swaminathan, submitted Dec 28, 2021

"L<><<><<<><<<<RL<<<R><L<<R>><<L<R>>>" for the main puzzle.

"L<><<><<<><<<<RR<<<<>L><<L<><L><<L<><RL>>LL<L" for the bonus "*" puzzle.

Main puzzle: n = 9 cells (left to right), m = 150 balls, Permutation [5, 6, 4, 7, 3, 8, 2, 9, 1]:
String for initial orientation of 36 pins (top to bottom, left to right): L<><<><<<><<<<RL<<<R><L<<R>><<L<R>>>

Main puzzle ball distribution (Cells 1 to 9, left to right): [38, 19, 9, 9, 4, 5, 9, 19, 38]
Main puzzle Score = 88.681766

Bonus "*" puzzle: n = 10 cells (left to right), m = 150 balls, Permutation [4, 8, 2, 7, 10, 6, 3, 9, 1, 5]:
String for initial orientation of 45 pins (top to bottom, left to right): L<><<><<<><<<<RR<<<<>L><<L<><L><<L<><RL>>LL<L

Bonus "*" ball distribution (Cells 1 to 10, left to right): [19, 4, 10, 4, 38, 24, 9, 4, 19, 19]
Bonus "*" Score = 90.363569

I worked out the initial pin orientations with pen and paper. For the main puzzle, due to the pattern of the permutation given, we could 
give 1/4 of the balls to each of cells 1 and 9, 1/8 each to cells 2 and 8, 1/16 each to cells 3 and 7, 1/16 to cell 4, and 1/32 each to 
cells 6 and 5. For cells 1 through 4, we can achieve the desired distribution by looking at the triangle of six pins at the bottom left 
of the pin structure. For cells 5 through 9, we can achieve the desired distribution by looking at the triangle of ten pins at the bottom 
right of the pin structure. I set up these sixteen pins to get the desired distribution. Of course, the topmost pin (pin #1) has to be a 
dynamic pin. The pins at the left edge of the overall pin structure, between pin #1 and the top of the six-pin triangle at the bottom 
left, need to be static left pins. Similarly, the pins at the right edge of the overall pin structure, between pin #1 and the top of the 
ten-pin triangle at the bottom right, need to be static right pins. All remaining pins don't play a role, hence I just made them static 
left pins. I wrote a short C program to calculate the ball distribution and score based on the initial pin orientations that I had 
determined.

The initial pin orientations for the bonus puzzle took longer to work out with pen and paper. I eventually went with 16/64 of the balls 
to cell 5, 8/64 each to cells 1 and 9, 4/64 to cell 3, 10/64 to cell 6, 8/64 to cell 10, 4/64 to cell 7, 2/64 each to cells 2, 8 and 4. 
This distribution was achievable by considering the triangle of ten pins at the bottom left, and the triangle of fifteen pins at the 
bottom right of the overall pin structure. I set up these 25 pins to get the desired distribution. As in the main puzzle, the topmost pin 
of the overall pin structure has to be dynamic, and the pins along the leftmost and rightmost edges, from the topmost pin to the triangle 
sub structures, need to be appropriately static. The remaining pins don't play a role, hence I just made them static left pins. With this 
initial pin orientation, I ran the C program to calculate the ball distribution and score for the bonus "*" puzzle.

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>

/* To compile: gcc -o ponderdec21 ponderdec21.c -lm
   Usage: ./ponderdec21 > ponderdec21.log &
   Author: Sanandan
*/

#define CELLS 10
#define BALLS 150
#define PINS 45

int main() {
short n = CELLS;
short m = BALLS;
double c = (double)n/m;
short perms[CELLS] = {4, 8, 2, 7, 10, 6, 3, 9, 1, 5};
char *peg_str = "L<><<><<<><<<<RR<<<<>L><<L<><L><<L<><RL>>LL<L";
short pin_state[PINS];
short targets[PINS] = {1,3,4,6,7,8,10,11,12,13,15,16,17,18,19,21,22,23,24,25,26,28,29,30,31,32,33,34,36,37,38,39,40,41,42,43,45,46,47,48,49,50,51,52,53};
short dist[CELLS] = {0,0,0,0,0,0,0,0,0,0};
short ball, next_pin, prev_pin, k;
double prod = 1.0;

for (k=0; k<strlen(peg_str); k++)
  if (peg_str[k] == 'R' || peg_str[k] == '>')
    pin_state[k] = 1;
  else
    pin_state[k] = 0;

for (ball=0; ball < BALLS; ball++) {
  next_pin = 0;
  while(true) {
    if (next_pin>(PINS-1)) {
        dist[next_pin - PINS]++;
        break;
    }

    prev_pin = next_pin;
    if (pin_state[next_pin] == 0)
        next_pin = targets[next_pin];
    else
        next_pin = targets[next_pin]+1;

    if (peg_str[prev_pin] == 'L' || peg_str[prev_pin] == 'R')
        pin_state[prev_pin] = (pin_state[prev_pin] + 1)%2;

  }
}

printf("n = %hi cells (left to right), m = %hi balls, Peg string (top to bottom, left to right) = %s\n", n, m, peg_str);
printf("Permutations: [");
for (k=0; k<n; k++)
  printf("%hi, ",perms[k]);
printf("]\n");
printf("Ball distribution (Cells 1 to %hi): [",n);
for (k=0; k<n; k++)
  printf("%hi, ",dist[k]);
printf("]\n");

for (k=1; k<=n; k++)
    prod = prod*(pow(c*dist[perms[k-1] -1], k));

printf("Score = %lf\n", prod);

}


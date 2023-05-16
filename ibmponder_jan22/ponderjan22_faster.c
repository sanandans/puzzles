/*
IBM Ponder This challenge and bonus *, Jan 22
https://research.ibm.com/haifa/ponderthis/challenges/January2022.html
Sanandan Swaminathan, submitted Jan 6, 2022

Main puzzle (n=7, d=5):

[1, 2, 5, 4, 9, 3, 7] gives maximum total circle score of 3051.

[1, 0, 6, 2, 8, 5, 4] gives minimum total circle score of 446.

Bonus puzzle (n=8, d=6):

[1, 8, 2, 3, 4, 6, 7, 9] gives maximum total circle score of 23209.

[1, 0, 6, 9, 5, 2, 8, 4] gives minimum total circle score of 8265.

Of course, clockwise and counter-clockwise rotations of the above answers will also give the same results. Also, there may be other sets that give the same max or min.

I wrote a C program. It completed quickly for both the main and bonus puzzles. First it stores a list of d-digit primes with all distinct digits. Then it loops through n-digit numbers with all distinct digits, skipping any number that is equivalent through clockwise or counter-clockwise rotation. For a qualifying n-digit number, it iterates through the stored list of primes and checks if the prime can be formed, and calculates the total circle score also. It outputs the earliest n-digit number that gave the max total circle score, and also the earliest n-digit number that gave the min.

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>

/* To compile: gcc -o ponderjan22_faster ponderjan22_faster.c -lm
   Usage: ./ponderjan22_faster > ponderjan22_faster.log &
   Author: Sanandan
*/

#define NUM_N 8
#define NUM_D 6

short primes_arr[(long)(pow(10, NUM_D-1))][NUM_D]; // approx number of primes less than 10^d is (10^d) / ln(10^d) < 10^(d-1) for d>4
bool ndig_nums[(long)(9*pow(10, NUM_N-1))];

bool is_prime(long num)
{
    long i;

    if (num == 2)
        return true;

    if (num%2 == 0)
        return false;

    for (i=3; i<=(sqrt(num)+1); i += 2) {
        if (num%i == 0)
                return false;
    }

    return true;
}


bool has_repeating_digit(long num, short numdigits)
{
bool num_digit_pos[10];
short j, dig;
memset(num_digit_pos, 0, sizeof(num_digit_pos));
for (j=0; j<numdigits; j++) {
  dig = num%10;
  if (num_digit_pos[dig])
    return true;
  else
    num_digit_pos[dig] = true;

  num = num/10;
}

return false;

}

void populate_primes()
{
long i = 0;
long init_j, end_j, j, rem_prime;
short k;
init_j = (long)(pow(10, NUM_D-1));
end_j = (long)(pow(10, NUM_D));
for (j=init_j; j<end_j; j++) {
  if (!(has_repeating_digit(j, NUM_D))) {
    if (is_prime(j)) {
      rem_prime = j;
      for (k=0; k<NUM_D-1; k++) {
        primes_arr[i][k] = rem_prime%10;
        rem_prime = rem_prime/10;
      }
      primes_arr[i][k] = rem_prime;
//long prime_match_count=0;
short num_digit_pos[10];
short j, dig, half_diff, prev_digit, prev_digit_pos, next_digit, next_digit_pos, pos_diff;
memset(num_digit_pos, 0, sizeof(num_digit_pos));
for (j=1; j<NUM_N; j++) {
  num_digit_pos[num%10] = j;
  num = num/10;
}

num_digit_pos[num] = j;

half_diff = NUM_N/2;
long tot_score = 0;
long i=0;
long temp_score;
short prime_unit_digit = primes_arr[0][0];
while (prime_unit_digit > 0) {
  temp_score = 0;
  prev_digit = primes_arr[i][0];
  prev_digit_pos = num_digit_pos[prev_digit];
  if (prev_digit_pos > 0) {
    for (j=1; j<NUM_D; j++) {
      next_digit = primes_arr[i][j];
      next_digit_pos = num_digit_pos[next_digit];
      if (next_digit_pos > 0) {
        pos_diff = abs(next_digit_pos - prev_digit_pos);
        if (pos_diff > half_diff)
           temp_score += (NUM_N - pos_diff);
        else
           temp_score += pos_diff;

        prev_digit_pos = next_digit_pos;
      }
      else {
        temp_score = 0;
        break;
      }
    }

    //if (temp_score > 0)
       //prime_match_count++;

    tot_score += temp_score;
  }
  i++;
  prime_unit_digit = primes_arr[i][0];
}
//printf("prime_match_count %li\n", prime_match_count);
return tot_score;

}

int main()
{

long max_score = 0;
long num_max_score = 0;
long min_score = 10000000000;
long num_min_score = 0;
long tot_score;
time_t rightnow = time(NULL);
printf("Started at %s\n", ctime(&rightnow));

memset(primes_arr,0,sizeof(primes_arr));
populate_primes();

memset(ndig_nums,0,sizeof(ndig_nums));

long init_j = (long)(pow(10, NUM_N-1));
long end_j = (long)(pow(10, NUM_N));
long basenum = (long)(pow(10, NUM_N-1));
long j;
//for (j=4736201; j<4736202; j++) {
for (j=init_j; j<end_j; j++) {
  if (!(ndig_nums[j - basenum])) {
    if (!(has_repeating_digit(j, NUM_N))) {
      mark_rotations(j);
      tot_score = score(j);
      if (tot_score < min_score) {
        min_score = tot_score;
        num_min_score = j;
      }
      if (tot_score > max_score) {
        max_score = tot_score;
        num_max_score = j;
      }
    }
  }
}

printf("min_score %li, num_min_score %li, max_score %li, num_max_score %li\n", min_score, num_min_score, max_score, num_max_score);
rightnow = time(NULL);
printf("Ended at %s\n", ctime(&rightnow));
return 0;
}


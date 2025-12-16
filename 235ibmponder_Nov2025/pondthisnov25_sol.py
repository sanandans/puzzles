'''
My IBM Ponder This November '25 challenge main and bonus * solutions (both complete instantaneously)
https://research.ibm.com/haifa/ponderthis/challenges/November2025.html
Sanandan Swaminathan, submitted December 4, 2025

By expanding the letters in the starting string a few times by hand, we immediately see that the
span of each letter expands in a Fibonacci manner, so roughly increasing by a factor of the golden
ratio (1.618 approximately) in each round. If a letter's expansion goes beyond 10^100 length in x
rounds, then 1.618^x > 10^100. Taking log10, we determine that it takes only about 479 rounds for
the first letter C (of CAT) to exceed a spam of 10^100 length. Also, the starting letter in each
generation of the string alternates as C, T, C, T... After 10^100 rounds, the starting letter would
be C. The starting letter of the string would also be C after 500 rounds, and every 500 rounds after
that, all the way to after thr final round 10^100. The desired substring of length 1000 would be in
the expansion of single starting letter C after generations 500, 1000, 1500... 10^100. So, the final
answer after 10^100 generations will be the same as the substring we can obtain after 500 generations.
Finding the substring between indices 10^100 and (10^100) + 999, both inclusive, is straight forward.
Of course, we can't afford to store actual strings even for 500 generations. Consider the first few
generations originating with the starting letter C of CAT.
Gen 0: C
Gen 1: TG
Gen 2: CAT
Gen 3: TGCCA

The expansion of C after 500 rounds is the same as the expansion of TG after 499 rounds, which is the
same as the expansion of CAT after 498 rounds, which is the same as the expansion of TGCCA after 497
rounds, and so on. We can build a table of expansion lengths of each letter after each round. All
letters start with an expansion length of 1 after 0 rounds. After x rounds, a letter expands to the sum
of the expansion lengths of its child letters after x-1 rounds. For example, after 3 rounds, the span
of the initial C expands to 3 + 2 = 5, where 3 is the expansion length of C's child T and 2 is the
expansion length of C's child G after 2 rounds. Once we have the table of expansion lengths built
upto 500 rounds, we can trace back to a desired letter in the desired substring. For example, the
expansion length of the initial C would be well over (10^100) + 999 after 500 rounds. If we are looking
for the letter at index 10^100, for example, we know that it's the same as the letter at that index
in the expansion of T after 499 rounds. As we trace backwards, there will be a point when the desired
letter is not in the leftmost block, In this case, we can subtract the length of the insufficient
leftmost block from the search index number, and proceed to trace in the second block. Eventually, it
will trace to a single letter (entry in the table pertaining to 0 rounds). We can repeat this search
for all 1000 indices of the desired substring to extract each desired letter in order.

The bonus puzzle can be tackled in a very similar manner. The initial letters of strings are R, B, I,
T, C, B, I, T, C... After 10^100 rounds, the starting letter would be C, and it would also be C after
rounds 500, 1000, 1500... Also, the starting C after round 4 would have expanded to well over
(10^100) + 999 in length in 496 rounds (from round 5 through round 500). A desired letter in the
expansion of C after 500 rounds can be traced to the exxpansion of C's children after 499 rounds, and
so on.

My short program below completed instantaneously for both the main and bonus puzzles, and reported the
following answers.
Main puzzle answer:
TGTGCTGCCATGCCACATTGCCACATCATTGCATTGTGCTGCCATGCCACATTGCCACATCATTGTGCCACATCATTGCATTGTGCTGCCACATCATTGCAT
TGTGCCATTGTGCTGCCACATTGTGCTGCCATGCCACATCATTGTGCTGCCATGCCACATTGCCACATCATTGCATTGTGCTGCCATGCCACATTGCCACAT
CATTGTGCCACATCATTGCATTGTGCCATTGTGCTGCCATGCCACATTGCCACATCATTGTGCCACATCATTGCATTGTGCTGCCACATCATTGCATTGTGC
CATTGTGCTGCCACATTGTGCTGCCATGCCACATTGCCACATCATTGTGCCACATCATTGCATTGTGCTGCCACATCATTGCATTGTGCCATTGTGCTGCCA
TGCCACATCATTGCATTGTGCCATTGTGCTGCCACATTGTGCTGCCATGCCACATTGCCACATCATTGCATTGTGCCATTGTGCTGCCACATTGTGCTGCCA
TGCCACATCATTGTGCTGCCATGCCACATTGCCACATCATTGTGCCACATCATTGCATTGTGCCATTGTGCTGCCACATTGTGCTGCCATGCCACATCATTG
TGCTGCCATGCCACATTGCCACATCATTGCATTGTGCTGCCATGCCACATTGCCACATCATTGTGCCACATCATTGCATTGTGCTGCCACATCATTGCATTG
TGCCATTGTGCTGCCACATTGTGCTGCCATGCCACATCATTGTGCTGCCATGCCACATTGCCACATCATTGCATTGTGCTGCCATGCCACATTGCCACATCA
TTGTGCCACATCATTGCATTGTGCCATTGTGCTGCCATGCCACATTGCCACATCATTGTGCCACATCATTGCATTGTGCTGCCACATCATTGCATTGTGCCA
TTGTGCTGCCATGCCACATCATTGCATTGTGCCATTGTGCTGCCACATTGTGCTGCCATGCCACATCATTGTGCTGCCATGC

Bonus * puzzle answer:
BRTGCBRICATGCISCATBRICAISBCATBRISBTGBRITGCISBRICAISBTGCISCATISBTGBRICAISBCATBRISBTGBRITGCISCATISBTGCAT
BRTGCISBTGBRITGCISCATBRTGCBRICATGCISCATISBTGBRITGCISBRICAISBTGCISCATISBTGCATBRTGCBRICATGCISCATBRICAISB
CATBRTGCISCATISBTGCATBRTGCISBTGBRITGCISBRICAISBTGCISCATISBTGBRICAISBCATBRISBTGBRITGCISCATISBTGCATBRTGC
ISBTGBRITGCISCATBRTGCBRICATGCISCATBRICAISBCATBRTGCISCATISBTGCATBRTGCBRICAISBCATBRISBTGBRICATBRTGCBRICA
TGCISCATISBTGCATBRTGCISBTGBRITGCISCATBRTGCBRICATGCISCATBRICAISBCATBRISBTGBRICATBRTGCBRICAISBTGBRITGCIS
BRICAISBCATBRTGCBRICATGCISCATBRICAISBCATBRTGCISCATISBTGCATBRTGCISBTGBRITGCISCATBRTGCBRICATGCISCATISBTG
BRITGCISBRICAISBTGCISCATISBTGCATBRTGCBRICATGCISCATBRICAISBCATBRTGCISCATISBTGCATBRTGCBRICAISBCATBRISBTG
BRICATBRTGCBRICAISBTGBRITGCISBRICAISBCATBRTGCBRICATGCISCATBRICAISBCATBRISBTGBRITGCISBRICAISBTGCISCATIS
BTGBRICAISBCATBRISBTGBRICATBRTGCBRICATGCISCATBRICAISBCATBRTGCISCATISBTGCATBRTGCBRICAISBCATBRISBTGBRICA
TBRTGCBRICATGCISCATISBTGCATBRTGCISBTGBRITGCISCATBRTGCBRICATGCISCATISBTGBRITGCISBRI
'''

from datetime import datetime

def populate_expansion_lengths(symbols, transform_rules, num_iterations):
    expansion_lengths = dict()
    for sym in symbols:
        expansion_lengths[sym] = [1]*(num_iterations+1)
    for iteration in range(1, num_iterations + 1):
        for sym in symbols:
            expansion_len = 0
            for child in transform_rules[sym]:
                expansion_len += expansion_lengths[child][iteration - 1]
            expansion_lengths[sym][iteration] = expansion_len
    return expansion_lengths

def get_char(start_char, char_idx, num_iterations, transform_rules, expansion_lengths):
    curr_leader, iteration = start_char, num_iterations
    while iteration > 0:
        for char in transform_rules[curr_leader]:
            char_span = expansion_lengths[char][iteration - 1]
            if char_span <= char_idx:
                char_idx -= char_span
            else:
                curr_leader = char
                iteration -= 1
                break
    return curr_leader

def find_answer(start_str, transform_rules, answer_len, num_iterations, start_char, first_ans_idx):
    symbols = set()
    for sym in start_str:
        symbols.add(sym)
    for key, val in transform_rules.items():
        symbols.add(key)
        for sym in val:
            symbols.add(sym)
    expansion_lengths = populate_expansion_lengths(symbols, transform_rules, num_iterations)
    result = ""
    for i in range(answer_len):
        result += get_char(start_char, first_ans_idx + i, num_iterations, transform_rules, expansion_lengths)
    return result

print(datetime.now(), "main puzzle answer:\n", find_answer("CAT", {"G": "T", "T": "CA", "C": "TG", "A": "C"}, 1000, 500, "C", 10**100))
print(datetime.now(), "bonus * puzzle answer:\n", find_answer("RABBITS", {"G": "T", "T": "CA", "C": "BR", "A": "I", "R": "B", "B": "IS", "I": "TG", "S": "C"}, 1000, 500, "C", 10**100))
print(datetime.now(), "done")

'''
IBM Ponder This challenge main and bonus *, Dec 22
https://research.ibm.com/haifa/ponderthis/challenges/December2022.html
Sanandan Swaminathan, submitted Dec 5, 2022

Main puzzle (square box of 12 letters having exactly one two-word solution based on the given word list):

'irj aks ohl upn'    ['journals', 'sparkish']

Bonus "*" puzzle (sequence with at least 15 letters having exactly one two-word solution based on the given word list):

'atk uvh ows idl egc'    ['gavelocks', 'sawdustish']

For the main puzzle, I interpreted the instruction "Find a box that has only a single two-word solution" to mean that, while the box 
should have exactly one two-word solution, it is ok for that box to have other solutions containing more than two words (or another 
solution of just one word). I imagine that it would generally be possible to take a two-word solution and make it a three-word 
solution by adding a short word that meets the rules of the game. For the bonus "*" puzzle, I interpreted the instruction "find a 
sequence of at least 15 letters that also has a unique solution" to mean that you want a sequence of 15 letters that still has exactly 
one TWO-WORD solution (the instruction just says "unique solution"), and again, that it is ok for the sequence to have other solutions 
containing more than two words (or another solution of just one word). If you meant the instruction to be stricter, i.e. the box or 
sequence must have exactly one solution in total and that single solution must contain exactly two words, please let me know (though 
I'm not sure if such a situation can exist).

I wrote a python program, and it completed instantaneously for both the main and bonus "*" puzzles. It reads the given (hyperlinked) 
word file (words_alpha.txt), ignoring words that contain two consecutive, identical letters (since those words are not permissible in 
the game). I don't filter out words that are shorter than 3 characters since the puzzle doesn't state such a rule (the NYT game does 
have this restriction). I build a Trie structure that captures the pruned word list. The program then randomly picks 4 different 
vowels and assigns one to each edge. It picks 8 different consonants randomly and assigns two to each edge. Using each of the 12 
letters as the starting point, it does a recursive search through the word bank (the Trie) to find all words that can be made with the 
box. It then looks at pairs of words to see if their letters together cover all 12 letters of the box. If exactly one such word pair 
is found, the 12 letters of the box and the pair of words are printed. If no such word pair or two such pairs are found, it loops back 
to generate another random box. Given that I was doing a random search, it found a valid box and its single two-word solution 
surprisingly fast. I did the same thing for the bonus "*" puzzle, except that I used a pentagonal box (3 letters on each of 5 edges). 
The program randomly assigned 5 vowels, one to each edge, and 10 random consonants, two to each edge. Again, the program completed 
instantaneously and reported a valid pentagonal box and its single two-word solution.

'''

#import networkx as nx
import random
import datetime

f = open("words_alpha.txt", "r")
words = f.read().strip().split("\n")
prunedset = set()
for word in words:
    wordtemp = word.lower()
    reject = False
    for i in range(0,len(wordtemp)-1):
        if wordtemp[i] == wordtemp[i+1]:
            reject = True
            break
    if reject == False:
        prunedset.add(wordtemp)
words = [tempword.lower() for tempword in prunedset]
f.close()
print(len(words))

N=5

class Trie(object):
   
    def __init__(self, words=None):
        self.trie = dict()
        if words is not None:
            for word in words:
                self.add(word)
       
    def add(self, word):
        current_position = self.trie
        for c in word:
            if c not in current_position:
                current_position[c] = dict()
            current_position = current_position[c]
        current_position["done"] = True
       
    def query(self, word):
        current_position = self.trie
        for c in word:
            if c in current_position:
                current_position = current_position[c]
            else:
                return -1
        if "done" in current_position:
            return 1
        else:
            return 0

def do_search(current_face, current_word):

    for face in range(N):
        if face != current_face:
            for c in faces[face]:
                val = trie.query(current_word+c)
                if val == 1:
                    possible_words.append(current_word+c)
                    do_search(face, current_word+c)
                elif val == 0:
                    do_search(face, current_word+c)

trie = Trie(words)

'''
faces = [
    ["t","j","o"],
    ["f","e","b"],
    ["c","u","y"],
    ["h","i","l"]
]
'''
faces = [['0','0','0'], ['0','0','0'], ['0','0','0'], ['0','0','0'], ['0','0','0']]
vowels = ['a', 'e', 'i', 'o', 'u']
consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
progresscnt=0
while(True):
    progresscnt += 1
    if progresscnt%100 == 0:
        print(datetime.datetime.now(),progresscnt)
       
    row=0
    for letter in random.sample(vowels, N):
        faces[row][0] = letter
        row += 1

    arr = random.sample(consonants, 2*N)
    faces[0][1] = arr[0]
    faces[0][2] = arr[1]
    faces[1][1] = arr[2]
    faces[1][2] = arr[3]
    faces[2][1] = arr[4]
    faces[2][2] = arr[5]
    faces[3][1] = arr[6]
    faces[3][2] = arr[7]
    faces[4][1] = arr[8]
    faces[4][2] = arr[9]
    '''
    faces = [
        ["t","j","o"],
        ["f","e","b"],
        ["c","u","y"],
        ["h","i","l"]
    ]
    '''
    #faces = [['a', 'n', 'w'], ['e', 'c', 'z'], ['i', 's', 'm'], ['o', 'l', 'd']]
   
    all_letters = set([letter for face in faces for letter in face])

    possible_words = []
    for i in range(N):
        for c in faces[i]:
            #print("Searching for", c)
            do_search(i, c)

    #G = nx.DiGraph()
    cnt=0
    reject=False
    res = []
    for u in possible_words:
        for v in possible_words:
            if u != v:
                if u[-1] == v[0] and len(all_letters - set(u.join(v))) == 0:
                    cnt += 1
                    if cnt == 1:
                        res.append(u)
                        res.append(v)
                    else:
                        reject = True
                        break
                    #G.add_edge(u,v)
        if reject == True:
            break
    if cnt == 1:
        print(faces, res)
        break
    #break
    '''
    for u in possible_words:
        for v in possible_words:
            if u != v:
                for path in nx.all_simple_paths(G, u, v, 2):
                    if len(all_letters - set(''.join(path))) == 0:
                        if len(path) < 3:
                            print(path)        
    '''


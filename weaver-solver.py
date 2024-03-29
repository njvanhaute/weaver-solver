import argparse
import collections
import re

WORDS_FILE_PATH = '/usr/share/dict/words'

class WeaverSolution:
    def __init__(self):
        self.steps = []

    def __repr__(self):
        rep = ''
        for i in range(len(self.steps) - 1, 0, -1):
            rep += f'{self.steps[i]} -> '
        rep += self.steps[0]
        return rep

    def add_step(self, word):
        self.steps.append(word)

def english_words():
    words = None
    with open(WORDS_FILE_PATH) as words_file:
        words = set(words_file.read().split())
    return words

def adjacent_words(word, valid_words):
    words = set()
    for i in range(0, len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            new_word = word[:i] + c + word[i+1:]
            if new_word != word and new_word in valid_words:
                words.add(new_word)
    return words

def solve(start_word, end_word):
    valid_words = english_words()
    q = collections.deque([start_word])
    visited = set(start_word)
    parents = {}
    while q and end_word not in visited:
        word = q.pop()
        for adj_word in adjacent_words(word, valid_words):
            if adj_word not in visited:
                visited.add(adj_word)
                parents[adj_word] = word
                q.appendleft(adj_word)
    
    solution = WeaverSolution()
    solution.add_step(end_word)
    curr_word = end_word
    while curr_word != start_word:
        curr_word = parents[curr_word]
        solution.add_step(curr_word)

    return solution

def main():
    parser = argparse.ArgumentParser(description='Solve a Weaver puzzle.')
    parser.add_argument('start_word', type=str)
    parser.add_argument('end_word', type=str)
    args = parser.parse_args()
    print(solve(**vars(args)))

if __name__ == '__main__':
    main()
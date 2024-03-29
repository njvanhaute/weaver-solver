import argparse
import collections
import re

DEFAULT_WORDS_FILE_PATH = '/usr/share/dict/words'

class WeaverSolution:
    def __init__(self):
        self.steps = []

    def __repr__(self):
        if len(self.steps) == 0: return "No solution found"
        rep = ''
        for i in range(len(self.steps) - 1, 0, -1):
            rep += f'{self.steps[i]} -> '
        rep += self.steps[0]
        return rep

    def add_step(self, word):
        self.steps.append(word)

def english_words(words_file_path):
    words = None
    with open(words_file_path) as words_file:
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

def solve(start_word, end_word, words_file_path):
    solution = WeaverSolution()
    valid_words = english_words(words_file_path)

    if start_word not in valid_words or end_word not in valid_words:
        return solution
    
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

    if end_word in visited:
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
    parser.add_argument('--w', help='Alternate words file', default=DEFAULT_WORDS_FILE_PATH, type=str, required=False)
    args = vars(parser.parse_args())
    start_word = args['start_word']
    end_word = args['end_word']
    words_file_path = args['w']
    
    if len(start_word) != len(end_word):
        parser.error('start_word and end_word must be of equal length')
    else:
        print(solve(start_word, end_word, words_file_path))

if __name__ == '__main__':
    main()
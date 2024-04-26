import argparse
import collections

class WeaverSolution:
    def __init__(self):
        self.steps = []

    def __repr__(self):
        if len(self.steps) == 0: return 'No solution found'
        rep = ''
        for step in reversed(self.steps):
            rep += step
            if step != self.steps[0]:
                rep += ' -> '
        return rep

    def add_step(self, word):
        self.steps.append(word)

class InvalidInput(WeaverSolution):
    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return f'{self.word} is not in the word list'

def english_words(words_file_path):
    with open(words_file_path) as words_file:
        return set(words_file.read().split())

def adjacent_words(word, valid_words):
    words = set()
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            new_word = word[:i] + c + word[i+1:]
            if new_word != word and new_word in valid_words:
                words.add(new_word)
    return words

def solve(start_word, end_word, words_file_path):
    valid_words = english_words(words_file_path)

    if start_word not in valid_words:
        return InvalidInput(start_word)
    
    if end_word not in valid_words:
        return InvalidInput(end_word)
    
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
    if end_word in visited:
        curr_word = end_word
        while curr_word != start_word:
            solution.add_step(curr_word)
            curr_word = parents[curr_word]
        solution.add_step(start_word)
            
    return solution

def build_parser():
    parser = argparse.ArgumentParser(description='Solve a Weaver puzzle.')
    parser.add_argument('start_word', type=str)
    parser.add_argument('end_word', type=str)
    parser.add_argument('--w', help='Alternate words file', default='weaver_words', type=str, required=False)
    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    
    if len(args.start_word) != len(args.end_word):
        parser.error('start_word and end_word must be of equal length')
    elif args.start_word == args.end_word:
        parser.error('start_word and end_word must be different')
    else:
        print(solve(args.start_word, args.end_word, args.w))

if __name__ == '__main__':
    main()
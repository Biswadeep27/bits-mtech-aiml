import pandas as pd
import re
from collections import Counter

class SpellingCorrector:
    def __init__(self, corpus_path):
        self.words = self.load_words(corpus_path)
        self.word_counts = Counter(self.words)
        self.total_words = sum(self.word_counts.values())

    def load_words(self, corpus_path):
        df = pd.read_csv(corpus_path)
        text = ' '.join(df['Message'].tolist()).lower()
        words = re.findall(r'\w+', text)
        return words

    def probability(self, word):
        return self.word_counts[word] / self.total_words

    def correction(self, word):
        return max(self.candidates(word), key=self.probability)

    def candidates(self, word):
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

    def known(self, words):
        return set(w for w in words if w in self.word_counts)

    def edits1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word):
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def correct_text(self, text):
        return ' '.join(self.correction(word) for word in text.split())


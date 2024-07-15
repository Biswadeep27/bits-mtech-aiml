import os
import re
from collections import Counter
from typing import List, Dict, Union, Tuple, Optional

import pandas as pd
from language_tool_python import LanguageTool

from spellcorrection.configuration import conf
from spellcorrection.exception import SpellCorrectionException
from spellcorrection.utils import is_directory, mkdir

class SpellingCorrector(object):
    """The Main Spelling Corrector class"""
    def __init__(self,model_type) -> None:
        self.model_type = model_type
        self.tokens = None
        self.words_count = None
        self.total_words = None
        self.tokenized = False

    def tokenize_corpus(self):
        if not self.tokenized:
            corpus_path = conf.get('backend', 'corpus_path')
            df = pd.read_csv(corpus_path)
            text = ' '.join(df['Message'].tolist()).lower()
            self.tokens = re.findall(r'\w+', text)
            self.words_count = Counter(self.tokens)
            self.total_words = sum(self.words_count.values())
            self.tokenized = True

    def _edits1(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _edits2(self, word):
        return (e2 for e1 in self._edits1(word) for e2 in self._edits1(e1))
    
    def _probability(self, word):
        return self.words_count[word] / self.total_words
    
    def _known(self, words):
        return set(w for w in words if w in self.words_count)

    def _candidates(self, word):
        return (self._known([word]) or self._known(self._edits1(word)) or self._known(self._edits2(word)) or [word])
    
    def _correction(self, word):
        return max(self._candidates(word), key=self._probability)
        

    def read_file(self, file_path) -> Optional[str]:
        try:
            return open(file_path).read()
        except Exception as e:
            raise SpellCorrectionException("Input File read failed.") from e 
        
    def write_file(self, file_path : str, text : str) -> Optional[bool]:
        try:
            parent_dir = os.path.split(file_path)[0]
            if not is_directory(parent_dir):
                mkdir(parent_dir)
            file = open(file_path, 'w')
            file.write(text)
            file.close()
            return True
        except Exception as e:
            print(f'ERROR: writing to file {file_path} failed with the error: {e}')
            return False
        
    def correct_text_classic(self, input_type : str, input_text : str = None, file_path : str = None, language : str = 'en') -> Optional[str]:
        if input_type == 'file':
            print('This model does not support file input. try pyspellchecker or language_tool.')
            return ''
        self.tokenize_corpus()
        return ' '.join(self._correction(word) for word in input_text.split())
    
    def correct_text_spellchecker(self, input_type : str, input_text : str = None, file_path : str = None, language : str = 'en'):
        if input_type == 'file':
            input_text = self.read_file(file_path)

        from spellchecker import SpellChecker
        spell = SpellChecker(language = language)

        # Split the text into words
        words = input_text.split()

        # Find misspelled words,Returns those words that are not in the frequency list
        misspelled = spell.unknown(words)

        # Correct misspelled words
        corrected_text = []
        for word in words:
            corrected_text.append(spell.correction(word) if word in misspelled else word)

        corrected_text_str =  ' '.join(corrected_text)
        
        if input_type == 'file':
            output_dir = conf.get('backend', 'corrected_file_path')
            file_name = f'corrected_{os.path.split(file_path)[-1]}'
            output_path = os.path.join(output_dir, file_name)
            self.write_file(output_path, corrected_text_str)
            return True
        else:
            return corrected_text_str
        
    def correct_text_language_tool(self, input_type : str, input_text : str = None, file_path : str = None, language : str = 'en-US'):
        if input_type == 'file':
            input_text = self.read_file(file_path)

        from language_tool_python import LanguageTool

        tool = LanguageTool(language= language)

        # Check text for errors
        matches = tool.check(input_text)

        # Correct errors
        corrected_text = tool.correct(input_text)

        if input_type == 'file':
            output_dir = conf.get('backend', 'corrected_file_path')
            file_name = f'corrected_{os.path.split(file_path)[-1]}'
            output_path = os.path.join(output_dir, file_name)
            self.write_file(output_path, corrected_text)
            return True
        else:
            return corrected_text
        
    def correct_text(self, *args, **kwargs):
        corrector = {
            'classic' : self.correct_text_classic,
            'pyspellchecker' : self.correct_text_spellchecker,
            'language_tool' : self.correct_text_language_tool
        }

        return corrector.get(self.model_type)(*args, **kwargs)

        



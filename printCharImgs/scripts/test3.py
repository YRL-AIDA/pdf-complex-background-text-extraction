import nltk
from nltk.corpus import words



def word_exists(word):
    word = word.lower()  # Convert word to lowercase for case-insensitive matching
    english_vocab = set(words.words())
    return word in english_vocab

# Example usage:
word_to_check = ""
if word_exists(word_to_check):
    print(f"'{word_to_check}' exists in the English language.")
else:
    print(f"'{word_to_check}' does not exist in the English language.")

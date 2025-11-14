from EnigmaConstants import ALPHABET

def apply_permutation(index, permutation, offset):
    shifted = (index + offset) % len(ALPHABET)
    letter = permutation[shifted]
    output_index = (ord(letter) - ord('A') - offset) % len(ALPHABET)
    return output_index

class EnigmaRotor:
    key = "A"
    alphabet = ""
    shifted_alphabet = ""

    def __init__(self, alphabet, shifted_alphabet):
        self.alphabet = alphabet
        self.shifted_alphabet = shifted_alphabet
        self.key = alphabet[0]

    def advance(self):
        next_idx = self.alphabet.index(self.key) + 1
        if next_idx == len(self.alphabet):
            self.key = self.alphabet[0]
        else:
            self.key = self.alphabet[next_idx]

    def get_offset(self):
        return self.alphabet.index(self.key)

    def get_permutation(self):
        return self.key



from EnigmaConstants import ALPHABET

class EnigmaRotor:
    def __init__(self, permutation):
        self._permutation = permutation
        self._inverse_permutation = self._invert_key(permutation)
        self._offset = 0

    def get_offset(self):
        return self._offset

    def get_permutation(self):
        return self._permutation

    def get_inverse_permutation(self):
        return self._inverse_permutation

    #Returns whether it looped back from Z to A
    #Used by the next rotor, to tell if it should also advance
    def advance(self):
        self._offset = (self._offset + 1) % 26
        return self._offset == 0

    def _invert_key(self, key):
        inverted = [""] * 26
        for i in range(26):
            encrypted_letter = key[i]
            encrypted_index = ALPHABET.index(encrypted_letter)
            inverted[encrypted_index] = ALPHABET[i]
        return "".join(inverted)

def apply_permutation(index, permutation, offset):
    shifted_index = (index + offset) % 26
    encrypted_char = permutation[shifted_index]
    encrypted_index = ALPHABET.index(encrypted_char)
    return (encrypted_index - offset) % 26

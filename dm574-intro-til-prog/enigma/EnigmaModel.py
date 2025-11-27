# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView
from EnigmaConstants import ALPHABET, ROTOR_PERMUTATIONS, REFLECTOR_PERMUTATION
from EnigmaRotor import EnigmaRotor, apply_permutation

class EnigmaModel:

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self._views = [ ]
        self._pressed_keys = {letter: False for letter in ALPHABET}
        self._lit_lamps = {letter: False for letter in ALPHABET}

        self._rotors = [
            EnigmaRotor(ROTOR_PERMUTATIONS[0]), #Slow
            EnigmaRotor(ROTOR_PERMUTATIONS[1]), #Medium
            EnigmaRotor(ROTOR_PERMUTATIONS[2])  #Fast
        ]

    def add_view(self, view):
        """Adds a view to this model."""
        self._views.append(view)

    def update(self):
        """Sends an update request to all the views."""
        for view in self._views:
            view.update()

    def is_key_down(self, letter):
        return self._pressed_keys.get(letter, False)

    def is_lamp_on(self, lamp_letter):
        return self._lit_lamps.get(lamp_letter, False)

    def key_pressed(self, letter):
        self._pressed_keys[letter] = True

        self._advance_rotors()

        encrypted_letter = self._encrypt_letter(letter)
        self._lit_lamps[encrypted_letter] = True

        self.update()

    def key_released(self, letter):
        self._pressed_keys[letter] = False

        #We can't really know what light to turn off, so we just turn the all off.
        for lamp_letter in ALPHABET:
            self._lit_lamps[lamp_letter] = False

        self.update()

    def get_rotor_letter(self, index):
        offset = self._rotors[index].get_offset()
        return ALPHABET[offset]

    def rotor_clicked(self, index):
        self._rotors[index].advance()
        self.update()

    def _advance_rotors(self):
        carry = self._rotors[2].advance()
        if carry:
            carry = self._rotors[1].advance()
            if carry:
                self._rotors[0].advance()

    def _encrypt_letter(self, letter):
        index = ALPHABET.index(letter)

        index = apply_permutation(index,
                                 self._rotors[2].get_permutation(),
                                 self._rotors[2].get_offset())
        index = apply_permutation(index,
                                 self._rotors[1].get_permutation(),
                                 self._rotors[1].get_offset())
        index = apply_permutation(index,
                                 self._rotors[0].get_permutation(),
                                 self._rotors[0].get_offset())

        index = apply_permutation(index, REFLECTOR_PERMUTATION, 0)

        index = apply_permutation(index,
                                 self._rotors[0].get_inverse_permutation(),
                                 self._rotors[0].get_offset())
        index = apply_permutation(index,
                                 self._rotors[1].get_inverse_permutation(),
                                 self._rotors[1].get_offset())
        index = apply_permutation(index,
                                 self._rotors[2].get_inverse_permutation(),
                                 self._rotors[2].get_offset())

        return ALPHABET[index]

def enigma():
    """Runs the Enigma simulator."""
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)

# Startup code

if __name__ == "__main__":
    enigma()

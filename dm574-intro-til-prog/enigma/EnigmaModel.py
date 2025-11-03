# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView
from EnigmaConstants import ALPHABET, ROTOR_PERMUTATIONS

class EnigmaRotor:
    key = "A"
    alphabet = ""

    def __init__(self, alphabet):
        self.alphabet = alphabet
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




class EnigmaModel:
    pressed_keys = set()
    rotors = [EnigmaRotor(ALPHABET),
              EnigmaRotor(ALPHABET),
              EnigmaRotor(ALPHABET)]

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self._views = [ ]

    def add_view(self, view):
        """Adds a view to this model."""
        self._views.append(view)

    def update(self):
        """Sends an update request to all the views."""
        for view in self._views:
            view.update()

    def is_key_down(self, letter):
        return letter in self.pressed_keys
        return False        # In the stub version, keys are never down

    def is_lamp_on(self, letter):
        return letter in self.pressed_keys
        return False        # In the stub version, lamps are always off

    def key_pressed(self, letter):
        # You need to fill in this code
        self.pressed_keys.add(letter)
        self.update()

    def key_released(self, letter):
        # You need to fill in this code
        self.pressed_keys.remove(letter)
        self.update()

    def get_rotor_letter(self, index):
        return self.rotors[index].get_permutation()
        return "A"          # In the stub version, all rotors are set to "A"

    def rotor_clicked(self, index):
        self.rotors[index].advance()
        # You need to fill in this code
        self.update()

def enigma():
    """Runs the Enigma simulator."""
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)

# Startup code

if __name__ == "__main__":
    enigma()

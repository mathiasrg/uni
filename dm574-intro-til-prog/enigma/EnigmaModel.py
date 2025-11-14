# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView
from EnigmaConstants import ALPHABET, ROTOR_PERMUTATIONS
from EnigmaRotor import EnigmaRotor, apply_permutation

class EnigmaModel:
    pressed_keys = set()
    rotors = [EnigmaRotor(ALPHABET, ROTOR_PERMUTATIONS[2]),
              EnigmaRotor(ALPHABET, ROTOR_PERMUTATIONS[1]),
              EnigmaRotor(ALPHABET, ROTOR_PERMUTATIONS[0])]

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

    def is_lamp_on(self, lamp_letter):
        if not self.pressed_keys:
            return False

        # The Enigma only allows one pressed key at a time for this assignment
        pressed = next(iter(self.pressed_keys))

        index = ALPHABET.index(pressed)
        new_index = apply_permutation(index,
                                  self.rotors[0].shifted_alphabet,
                                  self.rotors[0].get_offset())
        output_letter = ALPHABET[new_index]

        return lamp_letter == output_letter

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

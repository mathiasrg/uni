inches_input = int(input("Input inches: "))
feet_input = int(input("Input feet: "))
ell_input = int(input("Input ell: "))
fathom_input = int(input("Input fathom: "))

inches = inches_input
inches += feet_input * 12
inches += ell_input * 2 * 12
inches += fathom_input * 3 * 2 * 12

print("Total inches: ", inches)

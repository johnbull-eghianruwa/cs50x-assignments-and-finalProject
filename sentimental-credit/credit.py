# Import cs50 get_string library
from cs50 import get_int

while True:
    card = get_int("Enter Card: ")
    if card > 0:
        break

    # Find digits to be multipled by 2
    card1 = int(card % 10**2 / 10) * 2
    card2 = int(card % 10**4 / 10) * 4
    card3 = int(card % 10**6 / 10) * 6
    card4 = int(card % 10**8 / 10) * 8
    card5 = int(card % 10**10 / 10)



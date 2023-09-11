# Import cs50 get_string library
from cs50 import get_int

while True:
    card = get_int("Enter Card: ")
    if card > 0:
        break

    # Find digits to be multipled by 2
    card1 = int(card % 10**2 / 10) * 2
    card2 = int(card % 10**4 / 10**3) * 2
    card3 = int(card % 10**6 / 10**5) * 2
    card4 = int(card % 10**8 / 10**7) * 2
    card5 = int(card % 10**10 / 10**9) * 2
    card6 = int(card % 10**10 / 10**11) * 2
    card7 = int(card % 10**10 / 10**13) * 2
    card8 = int(card % 10**10 / 10**15) * 2




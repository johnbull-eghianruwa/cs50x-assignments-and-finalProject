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

    card1 = int(card1 % 10 / 10) + (card1 % 10)
    card2 = int(card2 % 10 / 10) + (card2 % 10)
    card3 = int(card3 % 10 / 10) + (card3 % 10)
    card4 = int(card4 % 10 / 10) + (card4 % 10)
    card5 = int(card5 % 10 / 10) + (card5 % 10)
    card6 = int(card6 % 10 / 10) + (card6 % 10)
    card7 = int(card7 % 10 / 10) + (card7 % 10)
    card8 = int(card8 % 10 / 10) + (card8 % 10)

    sum1 = card1 + card2 + card3 + card4 + card5 + card6 + card7 + card8

    # Find digits not multiplied by 2
    card9 = int(card % 10)
    card10 = int(card % 10**3 / 10**2)
    card11 = int(card % 10**5 / 10**4)
    card12 = int(card % 10**7 / 10**6)
    card13 = int(card % 10**9 / 10**8)
    card14 = int(card % 10**11 / 10**10)
    card15 = int(card % 10**13 / 10**12)
    card16 = int(card % 10**15 / 10**14)

    sum2 = card10 + card11 + card12 + card13 + card14 + card15 + card16
    sum3 = sum1 + sum2




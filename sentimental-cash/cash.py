# TODO
from cs50 import get_float

while True:
    cents = get_float("Change: ")
    if cents > 0:
        break

cents = round(cents * 100)

count = 0

# Number of quarters
while cents >= 25:
    cents = cents - 25
    count += 1

# Number of Dimes
while cents >= 5:
    cents = cents - 10
    count += 1

# Number of Nickels
while cents >= 5:
    cents = cents - 5
    count += 1

# Number of Pennies
while cents >= 1:
    cents = cents - 1
    count += 1
print("Coins\n: ", count)

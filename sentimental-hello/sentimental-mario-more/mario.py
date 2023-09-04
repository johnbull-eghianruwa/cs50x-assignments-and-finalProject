# TODO
from cs50 import get_int

# so while true n equal to get into height we will prompt the iser for height
while True:
    n = get_int("Enter height here: ")

# Notes as long as height is greater than o we use break
    if n > 0 and n < 9:
       break

# Function that is range to get any number of values and that range actually takes in other functions as well
for i in range(0, n, 1):
    for j in range(0, n + i + 3, 1):
        if (j == n or j == n+1 or i + j < n - 1):

            # To specfiy that nothing should be printed at the end of our string
            print("", end=" ")
        else:
            print("#", end="")
    print()


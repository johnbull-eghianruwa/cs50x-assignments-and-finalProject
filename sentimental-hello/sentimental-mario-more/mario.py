# TODO
from cs50 import get_int

# so while true n equal to get into height we will prompt the iser for height
while True:
    n = get_int("Enter height here: ")

# notes as long as height is greater than o we use break
    if n > 0 and n < 9:
       break
for i in range(0, n, 1):
    for j in range(0, n + i + 3, 1):
        if (j == n or j == n+1 or i + j < n - 1):
            print("", end=" ")
        else:
            print("#", end="")
    print()


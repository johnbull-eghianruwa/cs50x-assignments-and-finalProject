# Import cs50 get_string library
from cs50 import get_int

def main():
    while True:
        credit_card = get_int("Number: ")
        if credit_card >= 0:
            break # we look for the valid case here and break out

        if check_validity(credit_card):
            print
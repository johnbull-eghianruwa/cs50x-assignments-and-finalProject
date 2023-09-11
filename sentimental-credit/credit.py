# Import cs50 get_string library
from cs50 import get_int

def main():
    while True:
        card = get_int("Card: ")
        if card > 0:
            break
def luhn_checksum(card):
    def digits_of(n):
        return[int(d) for d in str(n)]
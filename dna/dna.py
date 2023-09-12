import csv
import sys

def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("python dna.py data.csv sequence.text")

    # TODO: Read database file into a variable
    database = []
    with open(sys.argv[1], "r") as file:
        reader = csv.dictReader(file)
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        dna_sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    subsequences = list(database[0].keys())[1:]
    result = {}
    for subsequence in subsequences:
        result[subsequence] = longest_match(dna_sequence, subsequence)


    # TODO: Check database for matching profiles
    for person in database:
        match = 0
        for subsequence in subsequences:
            if int(person[subsequence]) == result[subsequence]:
                match += 1

        # If all sequences match
        if match == len(subsequences):
            print(person["name"])
            return

    print("No match")

   
import csv
import sys


def main():

    # TODO: Check for command-line usage

    if len(sys.argv) != 3:
        print("Error in command-line usage!")
        sys.exit()

    # TODO: Read database file into a variable

    database_variable = []
    with open(sys.argv[1]) as f:
        content = csv.DictReader(f)
        for row in content:
            database_variable.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as f:
        sequence = f.readline().strip()

    # TODO: Find longest match of each STR in DNA sequence
    # print(database[0].keys())
    strs = list(database_variable[0].keys())
    strs = strs[1:]

    longest_str_counts = []
    for s in strs:
        longest_str_counts.append(longest_match(sequence, s))


    # TODO: Check database for matching profiles
    for person in database_variable:
        to_compare = []
        for s in strs:
            to_compare.append(int(person[s]))
        if to_compare == longest_str_counts:
            name = person["name"]
            print(name)
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

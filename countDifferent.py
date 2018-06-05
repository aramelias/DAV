# This script is made to count the different number of items that appear
#   in a given row. Program can either get target column through arguments,
#   or by quering the user itself.
import pandas as pd
import sys

def count_dict(dictionary):
    count = 0
    for item in dictionary:
        count += 1
    return count

# Entry
if __init__ == '__main__':
    print("<<< DifferentCounter >>>")
    print("<<<       v1.0       >>>\n")

    # Start by getting arguments
    column = ""
    if len(sys.argv) > 1:
        # We have been given an argument!
        column = sys.argv[1]

    # If not, query the user instead
    if len(column) == 0:
        print("What is the column that we should check?")
        column = input()

    print("Reading database...")
    database = pd.read_csv("/home/tim/Downloads/WFPVAM_FoodPrices_05-12-2017.csv")
    print("Done")

    # Verify the column is in the dataset
    if column not in database:
        print("FATAL ERROR: Given column does not appear in database")
        sys.exit(1)

    print("Collecting data from given column...")
    unique_items = {}
    for column in database:
        # Row length
        row_length = database[column].count
        for i in range(row_length):
            cell_value = database[column][i]
            if cell_value not in unique_items:
                unique_items[cell_value] = 1
            else:
                unique_items[cell_value] += 1
    print("Done.")
    # Time to represent the data
    print("<<< Result >>>")
    print("Total number of items: {}".format(count_dict(unique_items)))
    print("Occurence of each item:")
    for item in database:
        print("#{}: {}".format(item, database[item]))
    print("\nDone.")

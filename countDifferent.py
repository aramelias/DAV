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

progressbar_width = 30

y_words = {"y", "yes", "yep", "jup", "j", "ja", "sure", "whatever", "awesome",
            "great idea", "aye aye captain", "aye aye", "aye", "yes please"}

# Entry
if __name__ == '__main__':
    print("<<< DifferentCounter >>>")
    print("<<<       v1.0       >>>\n")

    # Start by getting arguments
    search_column = ""
    if len(sys.argv) > 1:
        # We have been given an argument!
        search_column = sys.argv[1]

    # If not, query the user instead
    if len(search_column ) == 0:
        print("What is the column that we should check?")
        print("(Note: you can also pass the column as an argument)")
        search_column = input()

    print("Reading database...")
    database = pd.read_csv("/home/tim/Downloads/WFPVAM_FoodPrices_05-12-2017.csv")
    print("Done")

    # Verify the column is in the dataset
    if search_column not in database:
        print("FATAL ERROR: Given column does not appear in database")
        sys.exit(1)

    print("Collecting data from given column...")
    # First of all, collect total cell count
    row_length = database[search_column].count()

    # Now do the real scan
    unique_items = {}
    for i in range(row_length):
        cell_value = database[search_column][i]
        if cell_value not in unique_items:
            unique_items[cell_value] = 1
        else:
            unique_items[cell_value] += 1
        # Update progress bar
        percentage = i / row_length
        print(" {:5.1f}% [".format(percentage * 100) + "=" * (int(progressbar_width * percentage)) + " " * ((progressbar_width - 1) - int(progressbar_width * percentage)) + "]", end="\r")
    print("Done.")
    # Time to represent the data
    print("<<< Result >>>")
    print("Total number of items: {}".format(count_dict(unique_items)))
    print("")
    print("Would you like to see the occurence of each item?")
    yn = input().lower()
    if yn in y_words:
        print("Occurence of each item:")
        for item in unique_items:
            print("#{}: {}".format(item, unique_items[item]))
    print("\nDone.")

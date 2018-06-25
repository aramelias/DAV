# This script is made to count the different number of items that appear
#   in a given row. Program can either get target column through arguments,
#   or by quering the user itself.
import pandas as pd
import sys
<<<<<<< HEAD
import os
=======
>>>>>>> 27d75ea2d5f004c2b5705ba0b48696758e842934
from TimsStuff.progressBar import ProgressBar

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
<<<<<<< HEAD
    database = pd.read_csv("/home/tim/git/DAV/WFPVAM_FoodPrices with unified units.csv")
=======
    database = pd.read_csv("/home/tim/Downloads/WFPVAM_FoodPrices_05-12-2017.csv")
>>>>>>> 27d75ea2d5f004c2b5705ba0b48696758e842934
    print("Done")

    # Verify the column is in the dataset
    if search_column not in database:
        print("FATAL ERROR: Given column does not appear in database")
        sys.exit(1)

    print("Collecting data from given column...")
    # First of all, collect total cell count
    row_length = len(database)

    # Now do the real scan
<<<<<<< HEAD
    _, screen_width = os.popen('stty size', 'r').read().split()
    unique_items = {}
    progress_bar = ProgressBar(int(screen_width), max_amount=row_length)
=======
    unique_items = {}
    progress_bar = ProgressBar(progressbar_width, max_amount=row_length)
>>>>>>> 27d75ea2d5f004c2b5705ba0b48696758e842934
    for i in range(row_length):
        cell_value = database[search_column][i]
        if cell_value not in unique_items:
            unique_items[cell_value] = 1
        else:
            unique_items[cell_value] += 1
        # Update progress bar
        progress_bar.set(i)
    print("Done.")
    # Time to represent the data
    print("<<< Result >>>")
    print("Total number of items: {}".format(count_dict(unique_items)))
    print("Total number of elements: {}".format(row_length))
    print("Would you like to see the occurence of each item?")
    yn = input().lower()
    if yn in y_words:
        print("Occurence of each item:")
        for item in unique_items:
            print("#{}: {}".format(item, unique_items[item]))
    print("\nDone.")

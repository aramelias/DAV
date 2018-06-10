# Checks a database for the spelling
import argparse
import pandas as pd
import sys
import os
import threading

from TimsStuff.progressBar import ProgressBar

class Analyser(threading.Thread):
    def __init__(self, database_path, columns):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.database_path = database_path
        self.columns = columns
        self.running = False
        print("{}: Successfully created".format(self.name))

    # Return the total work to be done by this thread
    def getTotalWork (self):
        total = 0
        for column in self.columns:
            total += len(column)
        return total

    # Return the current progress
    def getStatus (self):
        return self.counter

    # Return the final list if done
    def getResult (self):
        if not self.done:
            return self.diff_words

    # Check if done
    def isDone (self):
        return not self.running

    # Start the thread
    def start (self):
        print("{}: Starting...".format(self.name))
        if not self.running:
            self.running = True
            self.diff_words = {}
            self.counter = 0
            threading.Thread.start(self)
            print("{}: Started successfully (analysing {} columns)".format(self.name, len(self.columns)))
        else:
            print("{}: Already started".format(self.name))

    # The work itself
    def run (self):
        for column in self.columns:
            for cell in column:
                if cell not in self.diff_words:
                    self.diff_words[cell] = 1
                else:
                    self.diff_words[cell] += 1
                if not self.running:
                    break
                self.counter += 1
            if not self.running:
                break
        self.running = False

    # Stop the thread
    def stop (self):
        print("{}: Stopping...")
        if self.running:
            self.running = False
            while self.isAlive():
                pass
            print("{}: Stopped successfully".format(self.name))
        else:
            print("{}: Not running".format(self.name))

# Check if int
def is_int (to_test):
    try:
        int(to_test)
        return True
    except ValueError:
        return False

# Check if float
def is_float (to_test):
    try:
        float(to_test)
        return True
    except ValueError:
        return False

# Get the amount of characters different between the two
def difference (word1, word2):
    # Loop through each letter of word1 to see if it occurs in word2
    i = 0
    j = 0
    similar = ""
    while i < len(word1):
        if word1[i] == word2[j]:
            # Match
            similar += word1[i]
            word1 = word1[:i] + word1[i + 1:]
            word2 = word2[:j] + word2[j + 1:]
            j = -1
        j += 1
        if j >= len(word2):
            j = 0
            i += 1
    return len(word1 + word2)

# Return a multid
def spread (list):
    # Calculate the partitions
    part_sizes = []
    for i in range(4):
        part_sizes.append(len(list) // 4)
    for i in range(len(list) % 4):
        part_sizes[i] += 1
    # Now return a multidimensional list
    to_return = []
    for part in part_sizes:
        to_return.append(list[:part])
        list = list[part:]
    return to_return

# Entry point
if __name__ == "__main__":
    # First, read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--database", help="The path to the to be checked database")
    args = parser.parse_args()

    database_path = "/home/tim/git/DAV/WFPVAM_FoodPrices_05-12-2017 with column names.csv"
    if args.database:
        database_path = args.database

    print("########################")
    print("##### SPELLCHECKER #####")
    print("#####     v1.0     #####")
    print("########################\n")

    # Check database validity
    try:
        f = open(database_path, "r")
        f.close()
    except FileNotFoundError:
        print("Given database doesn't exist")
        sys.exit(1)

    # Read the database
    print("Reading database...")
    database = pd.read_csv(database_path)
    print("Done")

    # Get database size
    database_size = 0
    for column in database:
        database_size += len(database)

    # Get terminal size
    _, width = os.popen('stty size', 'r').read().split()

    # Setup the threads
    print("Preparing to analyse the database...")
    columns = []
    for column in database:
        columns.append(column)
    # Now divide over threads
    thread_columns = spread(columns)
    for i in range(len(thread_columns)):
        for j in range(len(thread_columns[i])):
            thread_columns[i][j] = database[thread_columns[i][j]]
    threads = []
    for columns in thread_columns:
        threads.append(Analyser(database_path, columns))
    print("Done")

    # Start analysing
    print("Analysing database...")
    # Prepare progress bars
    for i in range(len(threads)):
        thread = threads[i]
        threads[i] = (thread, ProgressBar(int(width) - len(thread.name) - 8, max_amount=thread.getTotalWork()))
    # Start the threads
    for (thread, progress_bar) in threads:
        thread.start()

    # Now keep up with the progress bars
    running_threads = len(threads)
    result = {}
    while running_threads > 0:
        running_threads = 0
        for (thread, progress_bar) in threads:
            # Update the running status
            if not thread.isDone():
                running_threads += 1
                # Print
                print("Thread {} ".format(thread.name),end="")
                progress_bar.set(thread.getStatus())
                print("")
            else:
                print("Thread done" + " " * (-3 + len(thread.name)))
        # Reset the cursor to the beginning
        for i in range(len(threads)):
            print("\033[F\033[F")
    print("\n\n\n\n\n\nDone")

    print("Post-analysing...")
    # Cross-reference the result to eliminate all doubles
    result = {}
    for (thread, progress_bar) in threads:
        thread_result = thread.getResult()
        for res in thread_result:
            if res not in result:
                result[res] = thread_result[res]
            else:
                result[res] += thread_result[res]
    print("Done")

    # Now loop through each word in diff_words, comparing it to other words
    print("Checking the spelling...")
    progress_bar = ProgressBar(int(width), min_amount=0, max_amount=len(result)**2)
    spelling_errors = []
    for word in result:
        for to_check in result:
            # Is two words differ less than 3 characters but more than 0, we say it's a spelling error
            diff = difference(word, to_check)
            if diff > 0 and diff < 4:
                to_add = (to_check, word)
                if result[word] > result[to_check]:
                    to_add = (word, to_check)
                if to_add not in spelling_errors:
                    spelling_errors.append(to_add)
            progress_bar.update()
    if len(spelling_errors) > 0:
        print("Found {} spelling errors:".format(len(spelling_errors)))
        for (chief_word, error_word) in spelling_errors:
            print(" > {} (probably meant to be {})".format(error_word, chief_word))
    print("Done")

# Checks a database for the spelling
import argparse
import pandas as pd
import sys
import os
import threading

from TimsStuff.progressBar import ProgressBar

class Analyser(threading.Thread):
    def __init__(self, columns):
        threading.Thread.__init__(self)
        self.setDaemon(True)
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
        if not self.running:
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
                # Only if not float or int
                if not is_int(cell) and not is_float(cell):
                    if cell not in self.diff_words:
                        self.diff_words[str(cell)] = 1
                    else:
                        self.diff_words[str(cell)] += 1
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

class SpellChecker (threading.Thread):
    def __init__(self, words, diff_words, name=-1):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.words = words
        self.diff_words = diff_words
        self.running = False
        print("{}: Successfully created".format(self.name))

    # Return the total work to be done by this thread
    def getTotalWork (self):
        return len(self.words) * len(self.diff_words)

    # Return the current progress
    def getStatus (self):
        return self.counter

    # Return the final list if done
    def getResult (self):
        if not self.running:
            return self.spelling_errors

    # Check if done
    def isDone (self):
        return not self.running

    def start (self):
        print("{}: Starting...".format(self.name))
        if not self.running:
            self.running = True
            self.spelling_errors = []
            self.counter = 0
            threading.Thread.start(self)
            print("{}: Started successfully (checking {} words)".format(self.name, len(self.words)))
        else:
            print("{}: Already started".format(self.name))

    # The work itself
    def run (self):
        for (word1, counter1) in self.words:
            for (word2, counter2) in self.diff_words:
                # Compare
                diff = difference(word1, word2)
                # If not equal but differ less than four characters:
                if diff > 0 and diff < 4:
                    # See which is biggest
                    big = word1
                    small = word2
                    if counter1 < counter2:
                        big = word2
                        small = word1
                    self.spelling_errors.append((big, small))
                self.counter += 1
                if not self.running:
                    break
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
    return difference_ordered(word1, word2)
    # Loop through each letter of word1 to see if it occurs in word2
    i = 0
    j = 0
    while i < len(word1) and len(word1) > 0 and len(word2) > 0:
        if word1[i] == word2[j]:
            # Match
            word1 = word1[:i] + word1[i + 1:]
            word2 = word2[:j] + word2[j + 1:]
            j = -1
        j += 1
        if j >= len(word2):
            j = 0
            i += 1
    return len(word1 + word2)

def difference_ordered (word1, word2):
    for i

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

    print("\n########################")
    print("##### SPELLCHECKER #####")
    print("#####     v3.0     #####")
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
        threads.append(Analyser(columns))
    # Prepare progress bars
    for i in range(len(threads)):
        thread = threads[i]
        threads[i] = (thread, ProgressBar(int(width) - len(thread.name) - 9, max_amount=thread.getTotalWork()))
    print("Done")

    # Start analysing
    print("Analysing database...")
    # Start the threads
    for (thread, _) in threads:
        thread.start()

    # Now keep up with the progress bars
    running_threads = len(threads)
    result = {}
    while running_threads > 0:
        print("")
        running_threads = 0
        for (thread, progress_bar) in threads:
            # Update the running status
            if not thread.isDone():
                running_threads += 1
                # Print
                print("{} busy... ".format(thread.name),end="")
                progress_bar.set(thread.getStatus())
                print("")
            else:
                print("{} done    ".format(thread.name),end="")
                progress_bar.set(thread.getStatus())
        # Reset the cursor to the beginning
        for i in range(len(threads)):
            print("\033[F\033[F")
        print("\033[F\033[F")
    print("\n\n\n\n\n\nDone")

    print("Gathering results...")
    # Cross-reference the result to eliminate all doubles
    result = {}
    for (thread, _) in threads:
        thread_result = thread.getResult()
        for res in thread_result:
            if res not in result:
                result[res] = thread_result[res]
            else:
                result[res] += thread_result[res]
    print("Converting results to a more useful format...")
    # Now convert to tuples
    temp_result = []
    for res in result:
        temp_result.append((res, result[res]))
    result = list(temp_result)
    print("Done")

    # Now loop through each word in diff_words, comparing it to other words
    print("Preparing to check spelling...")
    # Now divide over threads
    thread_words = spread(result)
    threads = []
    for words in thread_words:
        threads.append(SpellChecker(words, result))
    # Prepare progress bars
    for i in range(len(threads)):
        thread = threads[i]
        threads[i] = (thread, ProgressBar(int(width) - len(thread.name) - 9, max_amount=thread.getTotalWork()))
    print("Done")

    print("Running spellcheck...")
    # Start the threads
    for (thread, _) in threads:
        thread.start()

    # Now keep up with the progress bars
    running_threads = len(threads)
    result = {}
    while running_threads > 0:
        print("")
        running_threads = 0
        for (thread, progress_bar) in threads:
            # Update the running status
            if not thread.isDone():
                running_threads += 1
                # Print
                print("{} busy... ".format(thread.name),end="")
                progress_bar.set(thread.getStatus())
                print("")
            else:
                print("{} done    ".format(thread.name),end="")
                progress_bar.set(thread.getStatus())
        # Reset the cursor to the beginning
        for i in range(len(threads)):
            print("\033[F\033[F")
        print("\033[F\033[F")
    print("\n\n\n\n\n\nDone")

    print("Gathering spelling errors...")
    # Cross-reference the result to eliminate all doubles
    spelling_errors = []
    for (thread, _) in threads:
        thread_result = thread.getResult()
        for res in thread_result:
            if res not in spelling_errors:
                spelling_errors.append(res)
    print("Done")


    if len(spelling_errors) > 0:
        print("Found {} spelling errors:".format(len(spelling_errors)))
        for (chief_word, error_word) in spelling_errors:
            print(" > {} (probably meant to be {})".format(error_word, chief_word))
    else:
        print("Found no spelling errors.")
    print("Completed spell check.")

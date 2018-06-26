# Claculates correlation between two graphs. Collects graphs by using collect_graphs()
#   from graphs.py

######################## CHANGELOG ########################
###########################################################
## v0.1 (alpha):                                         ##
##   + Begun alpha development                           ##
##   + Imported 'collect_graphs' from graphs.py to do    ##
##     just that                                         ##
##   + Added a way to compute correlation, using np      ##
###########################################################
## v0.2 (beta):                                          ##
##   o Switches to beta development, so we start fixing  ##
##     bugs                                              ##
###########################################################
## v0.3 (beta):                                          ##
##   o Swapped from all-at-once plotting to fancy little ##
##     terminal, so there's more overview                ##
###########################################################
## v1.0 (release):                                       ##
##   o Switches status to release                        ##
###########################################################

import argparse
import pandas as pd
import sys
import os
import time
import bokeh.plotting as plt
import bokeh
import datetime
import random
import numpy as np

from TimsStuff.progressBar import ProgressBar
import graphs


def file_exists (file):
    try:
        f = open(file, "r")
        f.close()
        return True
    except FileNotFoundError:
        return False

# MAin
def main (input_path, pattern):
    # Welcome message
    print("\n################")
    print("## CORRELATOR ##")
    print("##    v1.0    ##")
    print("################\n")

    print("USING PATHS:")
    print("  - Database: {}".format(input_path))

    print("\nReading database...")
    database = pd.read_csv(input_path)
    database.fillna(0)
    print("Done")

    print("Correlating...")
    resulting_graphs, total_tier2, _ = graphs.collect_graphs(database, pattern, True)

    print("\033[K\033[F\033[K", end="")
    print("  - Computing correlation...")
    correlation_pairs = {}
    progress_bar = ProgressBar(max_amount=total_tier2)
    for tier1 in resulting_graphs:
        if tier1 not in correlation_pairs:
            correlation_pairs[tier1] = []
        for tier2 in resulting_graphs[tier1]:
            _, y_list = resulting_graphs[tier1][tier2]
            for tier2_check in resulting_graphs[tier1]:
                if tier2 == tier2_check:
                    continue
                # Make sure we only grab the common part
                _, y_list_check = resulting_graphs[tier1][tier2_check]

                old_y_list = list(y_list)
                old_y_list_check = list(y_list_check)
                y_list = []
                y_list_check = []
                for i in range(len(old_y_list)):
                    if old_y_list[i] > 0 and old_y_list_check[i] > 0:
                        y_list.append(old_y_list[i])
                        y_list_check.append(old_y_list_check[i])

                if len(y_list) > 0:
                    # Save
                    if len(y_list) == 1:
                        corr = "Cannot compute correlation"
                    else:
                        corr = np.corrcoef(y_list, y_list_check)[1][0]
                    correlation_pairs[tier1].append((str(tier2) + " VS " + str(tier2_check), corr))
            progress_bar.update()
    print("Done")
    print("\n##### RESULT #####")
    print("Names:")
    for thing in correlation_pairs:
        print("  - {}".format(thing))
    print("Type the name of which you want to see the correlation (or '/help' for more):")
    while True:
        name = input()
        if name == "/names":
            print("Names:")
            for thing in correlation_pairs:
                print("  - {}".format(thing))
            print("Enter one of the above names (or '/help' for more):")
        elif name == "/h" or name == "/help":
            print("Type '/names' to see a list of the valid names")
            print("Type '/h' or '/help' to see this list")
            print("Type '/q' or '/quit' to quit")
        elif name == "/q" or name == "/quit":
            break
        elif name in correlation_pairs:
            print("Correlations:")
            for tag, correlation in correlation_pairs[name]:
                print("  - {}: {}".format(tag, correlation))
            if len(correlation_pairs[name]) == 0:
                print(" - No correlations in this data (no graphs with overlapping years)")
            print("Enter another name (or '/help' for more):")
        else:
            print("Please type a valid name! (or '/help' for more)")

    print("\nDone.\n")

if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)

    # Do some arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-p", "--pattern", help="The pattern used to define the graphs it will calculate on")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/git/Ignored/foodprices2 unified better.csv"
    pattern = ""
    if args.input_path:
        input_path = args.input_path
    if args.pattern:
        pattern = args.pattern
    else:
        print("Please give a pattern (--pattern <pattern>)!")
        sys.exit()

    if not file_exists(input_path):
        print("File not found ({})".format(input_path))
        print("Please specify another (--input_path <path>)")
        sys.exit()

    try:
        main (input_path, pattern)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit()

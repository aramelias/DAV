# K-MEANS: Use the K-Means algorithm to analyse databases

####################### CHANGELOG #######################
# v1.0 (alpha):                                         #
#   + Begun alpha development                           #
#########################################################


import argparse
import pandas as pd
import sys
import os
import time
import bokeh.plotting as plt
import bokeh.models as bkm
import bokeh.layouts as bkl
import bokeh
import datetime
import random
import numpy as np

from TimsStuff.progressBar import ProgressBar


def main (input_path):
    # Welcoming message
    print("\n#################")
    print("##   K-MEANS   ##")
    print("##    v 0.1    ##")
    print("#################\n")

    # Show the paths
    print("USING PATHS:")
    print("  - Input database: {}".format(input_path))

    # Read database
    print("\nReading database...")
    database = pd.read_csv(input_path)
    print("Done")


if __name__ == "__main__":
    # Do some arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/Ignored/foodprices2 unified better.csv"
    if args.input_path:
        input_path = args.input_path

    try:
        main (input_path)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit()

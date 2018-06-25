# This script takes all the BMI's and adds a column that has no complicated
#   extra range in it

import argparse
import pandas as pd
import sys
import os
import threading

from TimsStuff.progressBar import ProgressBar


# Entry point
if __name__ == "__main__":
    # First, read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the source database")
    parser.add_argument("-o", "--output_path", help="The path of the resulting database")
    args = parser.parse_args()

    input_path = "/home/tim/git/DAV/BMI-Data.csv"
    output_path = "/home/tim/git/DAV/BMI-Data-Less.csv"
    if args.input_path:
        input_path = args.input_path
    if args.output_path:
        output_path = args.output_path

    print("\n#################")
    print("## AVERAGIFYER ##")
    print("##    v 1.0    ##")
    print("#################\n")

    # Read and init DBs
    print("Reading database...")
    in_database = pd.read_csv(input_path)
    out_database = pd.DataFrame()
    print("Done")

    print("Analysing database...")
    for column in in_database:
        new_column = []
        for cell in in_database[column]:
            # See if it has "[" and "]"
            if "[" in cell and "]" in cell:
                cell = cell[:cell.find("[")]
            new_column.append(cell)
        out_database[column] = new_column
    print("Done")
    print("Constructing database...")
    out_database.to_csv(output_path)
    print("Done")

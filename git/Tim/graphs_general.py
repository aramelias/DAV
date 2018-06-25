# A script to make graphs from two columns specified. Additionally, other
#   options can be given.

import argparse
import pandas as pd
import sys
import os
import time
import matplotlib.pyplot as plt
import matplotlib as mpl

from TimsStuff.progressBar import ProgressBar

# Main function
def main (input_path, output_path, compact):



# Entry point
if __name__ == "__init__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-o", "--output_path", help="The path of the resulting database")
    parser.add_argument("-e", "--expanded", action="store_true", help="If given, changes the layout of the script to that of a more extended one.")
    parser.add_argument("-cx", "--column_x", help="The name of the column that will be displayed on the x-axis of the graph. Can be either numbers or strings, if the chosen graph type allows for it.")
    parser.add_argument("-cy", "--column_y", help="The name of the column that will be displayed on the y-axis of the graph. Must be number.")
    parser.add_argument("-g", "--graph_type", help="Sets the graph type. Choose from: plot, scatter or bar")
    parser.add_argument("-m", "--multiple", help="Allows patterns for adding multiple plots into one graph.")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/Ignored/foodprices2 unified.csv"
    output_path = "/Users/Tim/UvA/DAV/Tim/Ignored/graphs"
    expanded = False
    column_x = ""
    column_y = ""
    graph_type = "plot"
    multiple_pattern = []
    if args.input_path:
        input_path = args.input_path
    if args.output_path:
        output_path = args.output_path
    if args.expanded:
        expanded = True
    if args.column_x:
        column_x = args.column_x
    if args.column_y:
        column_y = args.column_y
    if args.graph_type:
        graph_type = args.graph_type
    if args.multiple:
        multiple_pattern = args.multiple.split(",")

    # Run main with KeyboardInterrupt catch
    try:
        main(input_path, output_path, compact)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit()

# K-MEANS: Use the K-Means algorithm to analyse databases

####################### CHANGELOG #######################
# v0.1 (alpha):                                         #
#   + Begun alpha development                           #
#########################################################
# v0.2 (alpha):                                         #
#   + Included an import to scatter_plot.py for easy    #
#     graph collection                                  #
#   + Added first view of the data, non-categorized     #
#########################################################
# v0.3 (alpha):                                         #
#   + Restructed graph generation to accept panda data  #
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
from sklearn import datasets
from sklearn.cluster import KMeans
import sklearn.metrics as sm

from TimsStuff.progressBar import ProgressBar
import scatter_plot

XLABEL = "Price (usd)"
YLABEL = "BMI"

def return_graph (graph_dataset, names_overview, regions_overview, colors_overview):
    # Done, plot
    legend_list = []

    # Create hover tool
    hover = bkm.HoverTool(tooltips=[("Country", "@names"), ("Region", "@regions")])

    # Create figure
    f = plt.figure(title="Plot of Rice price VS BMI", x_axis_label = XLABEL, y_axis_label = YLABEL, tools=[hover, bkm.WheelZoomTool(), bkm.BoxZoomTool(), bkm.PanTool(), bkm.SaveTool(), bkm.ResetTool()], width=900)

    # Plot
    region = regions_overview[0]

    data = {"price":graph_dataset.price, "BMI":graph_dataset.BMI, "names":names_overview, "regions":regions_overview, "colors":colors_overview}
    source = bkm.ColumnDataSource(data=data)
    elem = f.scatter("price", "BMI", source=source, color="colors", muted_color="colors", muted_alpha=0.1, size=10)
    legend_list.append((region, [elem]))

    # Do legend stuff
    legend = bokeh.models.Legend(items=legend_list, location=(0,0), click_policy="mute")

    f.x_range = bkm.DataRange1d(start=-1, end=3)
    f.y_range = bkm.DataRange1d(start=20, end=30)

    # Add legend & save
    f.add_layout(legend, 'right')
    return f

def display_graph (graph_data, names_overview, regions_overview, colors_overview):

    # The total graph info
    plt.output_file("test.html", mode="inline")
    plt.show(return_graph(graph_data, names_overview, regions_overview, colors_overview))

# Main
def main (input_path, input_path_bmi):
    # Welcoming message
    print("\n#################")
    print("##   K-MEANS   ##")
    print("##    v 0.3    ##")
    print("#################\n")

    # Show the paths
    print("USING PATHS:")
    print("  - Price database: {}".format(input_path))
    print("  - BMI database:   {}".format(input_path_bmi))

    # Read database
    print("\nReading database...")
    db_price = pd.read_csv(input_path)
    print("Done, reading BMI database...")
    db_BMI = pd.read_csv(input_path_bmi)
    print("Done")

    # Fill NaN
    db_price = db_price.fillna(0)
    db_BMI = db_BMI.fillna(0)

    # Let's first pan BMI vs PRICE, using collect_graphs derived from scatter_plot.py
    print("Collecting graph...")
    graphs, total_things = scatter_plot.collect_graphs(db_price, db_BMI)
    print("\nDone")

    if "Rice" not in graphs:
        print("Could not get rice data...")
        sys.exit()
    graphs = graphs["Rice"]

    graph_x_overview = []
    graph_y_overview = []
    names_overview = []
    regions_overview = []
    colors_overview = []
    for region in graphs:
        timestamp = 2016
        if timestamp not in graphs[region]:
            print("{} not in graphs...".format(timestamp))
            sys.exit()

        x_list, y_list = graphs[region][timestamp]
        for country in x_list:
            graph_x_overview.append(x_list[country])
            graph_y_overview.append(y_list[country])
            names_overview.append(country)
            regions_overview.append(region)
            R, G, B = scatter_plot.REGION_NAME_2_COLOR[region]
            colors_overview.append(bokeh.colors.RGB(R, G, B))

    # Get a pd dataframe of the data
    new_data = []
    for i in range(len(graph_x_overview)):
        new_data.append([graph_x_overview[i], graph_y_overview[i]])
    x = pd.DataFrame(new_data)
    x.columns = ["price", "BMI"]

    display_graph(x, names_overview, regions_overview, colors_overview)

    print("Performing K-means...")
    # Do K-Means
    model = KMeans(n_clusters=len(scatter_plot.REGION_ID_2_NAME))
    model.fit(x)
    

# Entry point
if __name__ == "__main__":
    # Do some arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-ib", "--input_path_bmi", help="The path to the BMI database")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/Ignored/foodprices2 unified better.csv"
    input_path_bmi = "/Users/Tim/UvA/DAV/BMI-Data-Less.csv"
    if args.input_path:
        input_path = args.input_path
    if args.input_path_bmi:
        input_path_bmi = args.input_path_bmi


    try:
        main (input_path, input_path_bmi)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit()

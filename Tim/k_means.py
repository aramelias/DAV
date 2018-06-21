# K-MEANS: Use the K-Means algorithm to analyse databases

######################## CHANGELOG ########################
###########################################################
## v0.1 (alpha):                                         ##
##   + Begun alpha development                           ##
###########################################################
## v0.2 (alpha):                                         ##
##   + Included an import to scatter_plot.py for easy    ##
##     graph collection                                  ##
##   + Added first view of the data, non-categorized     ##
###########################################################
## v0.3 (alpha):                                         ##
##   + Restructed graph generation to accept panda data  ##
###########################################################
## v0.4 (alpha):                                         ##
##   o Changed color handling to work with a colormap,   ##
##     so that the result of K-means can be interpreted  ##
##   o With that, changed the entire passing of the data ##
##     to construct_graph to accept a single Pandas DF   ##
###########################################################
## v0.5 (alpha):                                         ##
##   o Changed graph representation to one screen with   ##
##     two graphs instead of one                         ##
##   o Slightly modified data passing: now, there should ##
##     be passed a tuple of title and a pandas dataframe ##
###########################################################
## v0.6 (alpha):                                         ##
##   + Added total overview graph of entire database     ##
##     (using t-SNE to reduce dimensions, result         ##
##     pending)                                          ##
###########################################################


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
from sklearn.manifold import TSNE
import sklearn.metrics as sm

from TimsStuff.progressBar import ProgressBar
import scatter_plot

XLABEL = "Price (usd)"
YLABEL = "BMI"

REGION_NAME_2_COLOR_ID = {
    'Noord-Afrika': 0, # Yellow
    'Arabische Wereld': 1, # Orangy
    'Voormalig Sovjet Gebied': 2, # Blue / Purple
    'Zuid Azie': 3, # Dark Green
    'West Afrika': 4,  # Red Orangy
    'Zuid Amerika': 5, # Bluey green
    'Midden Afrika': 6, # Greeny yellow
    'Zuid Oost Azie': 7, # Deep green
    'Midden Amerika': 8, # Bright green
    'Oost Afrika': 9, # Dark Red
    'Zuidelijk Afrika': 10, # Red
    "Eilanden": 11 # Sea blue
}
COLOR_ID_TO_COLOR_RGB = {
    0: (235, 235, 0), # Yellow
    1: (255, 158, 0), # Orangy
    2: (128, 128, 190), # Blue / Purple
    3: (0, 108, 0), # Dark Green
    4: (224, 63, 0),  # Red Orangy
    5: (0, 188, 126), # Bluey green
    6: (178, 203, 0), # Greeny yellow
    7: (0, 178, 0), # Deep green
    8: (0, 255, 0), # Bright green
    9: (100, 0, 0), # Dark Red
    10: (255, 0, 0), # Red
    11: (0, 188, 254) # Sea blue
}
LEGAL_COLUMNS = [
    "country_id",
    "region_id",
    "city_id",
    "product_id",
    "cur_id",
    "sale_id",
    "month",
    "year",
    "standardized_units_ids",
    "standardized_prices"
]

def return_graph (title, graph_dataset):
    # First, let's convert colors
    colors = list(graph_dataset.colors)
    for i, color in enumerate(graph_dataset.colors):
        r,g,b = COLOR_ID_TO_COLOR_RGB[color]
        colors[i] = bokeh.colors.RGB(r, g, b)
    graph_dataset.colors = colors

    # Create hover tool
    hover = bkm.HoverTool(tooltips=[("Country", "@names"), ("Region", "@regions")])

    # Create figure
    f = plt.figure(title=title, x_axis_label = XLABEL, y_axis_label = YLABEL, tools=[hover, bkm.WheelZoomTool(), bkm.BoxZoomTool(), bkm.PanTool(), bkm.SaveTool(), bkm.ResetTool()], width=900)

    # Plot

    data = {"price":graph_dataset.price, "BMI":graph_dataset.bmi, "names":graph_dataset.names, "regions":graph_dataset.regions, "colors":graph_dataset.colors}
    source = bkm.ColumnDataSource(data=data)
    f.scatter("price", "BMI", source=source, color="colors", muted_color="colors", muted_alpha=0.1, size=10)

    f.x_range = bkm.DataRange1d(start=-1, end=3)
    f.y_range = bkm.DataRange1d(start=20, end=30)

    # Add legend & save
    return f

def display_graphs (graphs=[], *graph_datas):
    # Assemble all the graphs
    fs = []
    if graphs == []:
        for title, graph_data in graph_datas:
            fs.append(return_graph(title, graph_data))
    else:
        for title, graph_data in graphs:
            fs.append(return_graph(title, graph_data))

    # Construct a layout
    layout = bkm.layouts.Column(children=fs)

    # Show it
    plt.output_file("test.html", mode="inline")
    plt.show(layout)

# Main
def main (input_path, input_path_bmi):
    # Welcoming message
    print("\n#################")
    print("##   K-MEANS   ##")
    print("##    v 0.6    ##")
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
    print("Creating reference graph...")

    if "Rice" not in graphs:
        print("Could not get rice data...")
        sys.exit()
    graphs = graphs["Rice"]

    data = []
    for region in graphs:
        timestamp = 2016
        if timestamp not in graphs[region]:
            print("{} not in graphs...".format(timestamp))
            sys.exit()

        x_list, y_list = graphs[region][timestamp]
        for country in x_list:
            new_row = {}
            new_row["price"] = x_list[country]
            new_row["bmi"] = y_list[country]
            new_row["names"] = country
            new_row["regions"] = region
            new_row["colors"] = REGION_NAME_2_COLOR_ID[region]
            data.append(new_row)

    complete = pd.DataFrame(data)

    print("Done")


    print("Performing K-means...")

    # Get the dataframe we use for the simple match
    x = pd.DataFrame()
    x["price"] = complete["price"]
    x["bmi"] = complete["bmi"]

    # Do K-Means
    model = KMeans(n_clusters=len(scatter_plot.REGION_ID_2_NAME))
    model.fit(x)
    print("Creating K-Means graph...")
    x["names"] = complete["names"]
    x["regions"] = complete["regions"]
    x["colors"] = model.labels_

    print("Done")

    graphs = [("Price of Rice VS BMI per country", complete), ("Result of K-Means of price of Rice VS BMI per country", x)]

    print("Creating graph of entire database...")

    # Do a general graph
    data = []
    for row in db_price.itertuples():
        new_row = {}
        new_row["country_id"] = row.country_id
        new_row["region_id"] = row.region_id
        new_row["city_id"] = row.city_id
        new_row["product_id"] = row.product_id
        new_row["cur_id"] = row.cur_id
        new_row["sale_id"] = row.sale_id
        new_row["month"] = row.month
        new_row["year"] = row.year
        new_row["standardized_units_ids"] = row.standardized_units_ids
        new_row["standardized_prices"] = row.standardized_prices
        new_row["countries"] = row.country_name
        new_row["regions"] = scatter_plot.REGION_ID_2_NAME[scatter_plot.COUNTRY_2_REGION[row.country_name]]
        data.append(new_row)
    all_data = pd.DataFrame(data)

    x = pd.DataFrame()
    for column in all_data:
        if column != "countries" and column != "regions":
            x[column] = all_data[column]

    print("  - Performing K-Means...")
    model = KMeans(n_clusters = 8)
    model.fit(x)

    print("  - Using TSNE to reduce dimensions...")
    x_embedded = TSNE().fit_transform(x)
    print(x_embedded)
    print("Done")

    # Show the graph
    print("Showing graphs...")
    display_graphs(children=graphs + [("General overview"), x])
    print("Done")

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

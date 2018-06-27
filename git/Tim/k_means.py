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
## v0.7 (alpha):                                         ##
##  - (Temporarily) Removed t-SNE, as this takes endless ##
##    amount of time                                     ##
###########################################################
## v0.8 (alpha):                                         ##
##  o Changed overview graph presentation to a list of   ##
##    all graphs (result pending)                        ##
###########################################################
## v0.9 (alpha):                                         ##
##  o Swapped back to t-SNE dimensionality reduction,    ##
##    bc of better understanding and possible solutions  ##
###########################################################
## v1.0:                                                 ##
##  o Switches dev status to 'released'                  ##
##  o Small improvements, such as graph layout and final ##
##    bug fixes                                          ##
###########################################################
## v1.1:                                                 ##
##  + Added label 'product'                              ##
##  - Fixed label bug                                    ##
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

def is_int (thing):
    try:
        int(thing)
        return True
    except ValueError:
        return False

def file_exists (filename):
    try:
        f = open(filename, "r")
        f.close()
        return True
    except FileNotFoundError:
        return False

def return_graph (title, graph_dataset, columns="price,bmi"):
    # First, let's convert colors
    print("  - Converting colors...",end="")
    colors = list(graph_dataset.colors)
    for i, color in enumerate(graph_dataset.colors):
        r,g,b = COLOR_ID_TO_COLOR_RGB[color]
        colors[i] = bokeh.colors.RGB(r, g, b)
    graph_dataset.colors = colors

    columns = columns.split(",")

    print("\r\033[K  - Creating figure...",end="")

    # Create hover tool
    tooltips = [("Country", "@names"), ("Region", "@regions")]
    if "products" in graph_dataset:
        tooltips.append(("Product", "@products"))
        products = graph_dataset["products"]
    hover = bkm.HoverTool(tooltips=tooltips)

    # Create figure
    f = plt.figure(title=title, x_axis_label = columns[0], y_axis_label = columns[1], tools=[hover, bkm.WheelZoomTool(), bkm.BoxZoomTool(), bkm.PanTool(), bkm.SaveTool(), bkm.ResetTool()], width=900)

    # Plot

    # First, make the graph_dataset unique
    x_list = graph_dataset[columns[0]]
    y_list = graph_dataset[columns[1]]
    names = graph_dataset["names"]
    regions = graph_dataset["regions"]
    colors = graph_dataset["colors"]
    #for i in range(len(graph_dataset[columns[0]])):
    #    elem1 = graph_dataset[columns[0]][i]
    #    elem2 = graph_dataset[columns[1]][i]
    #    if elem1 not in x_list and elem2 not in y_list:
    #        x_list.append(elem1)
    #        y_list.append(elem2)
    #        names.append(graph_dataset["names"][i])
    #        regions.append(graph_dataset["regions"][i])
    #        colors.append(graph_dataset["colors"][i])

    print("\r\033[K  - Plotting...",end="")
    data = {columns[0]:x_list, columns[1]:y_list, "names":names, "regions":regions, "colors":colors}
    if "products" in graph_dataset:
        data["products"] = products
    source = bkm.ColumnDataSource(data=data)
    f.scatter(columns[0], columns[1], source=source, color="colors", muted_color="colors", muted_alpha=0.1, size=10)

    #f.x_range = bkm.DataRange1d(start=-1, end=3)
    #f.y_range = bkm.DataRange1d(start=20, end=30)

    # Add legend & save
    print("\r\033[K  - Done")
    return f

def display_graphs (*graph_datas, graphs=[], columns="price,bmi", path="pricevsbmi.html"):
    # Assemble all the graphs
    fs = []
    if len(graphs) < 1:
        for title, graph_data in graph_datas:
            fs.append(return_graph(title, graph_data, columns=columns))
    else:
        for title, graph_data in graphs:
            fs.append(return_graph(title, graph_data, columns=columns))

    # Construct a layout
    layout = bkm.layouts.Column(children=fs)

    # Show it
    plt.output_file(path, mode="inline")
    plt.show(layout)

# Main
def main (input_path, input_path_bmi, permutation_size, with_colors):
    # Welcoming message
    print("\n#################")
    print("##   K-MEANS   ##")
    print("##    v 1.1    ##")
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


    print("Creating K-Means graph...")
    print("  - Doing K-Means...")

    # Get the dataframe we use for the simple match
    x = pd.DataFrame()
    x["price"] = complete["price"]
    x["bmi"] = complete["bmi"]

    # Do K-Means
    model = KMeans(n_clusters=len(scatter_plot.REGION_ID_2_NAME))
    model.fit(x)
    print("  - Creating K-Means graph...")
    x["names"] = complete["names"]
    x["regions"] = complete["regions"]
    x["colors"] = model.labels_

    print("Done")

    graphs = [("Price of Rice VS BMI per country", complete), ("Result of K-Means of price of Rice VS BMI per country", x)]

    print("Creating graph of entire database...")
    print("  - Collecting data...")

    # Do some preliminairy analysis
    all_data = pd.DataFrame()
    column_names = []
    counter = 0
    for column in db_price:
        if column in LEGAL_COLUMNS:
            all_data[column] = db_price[column]
            column_names.append(column)
            for cell in all_data[column]:
                # Count objects
                counter += 1
    # Add countries and regions
    all_data["names"] = db_price["country_name"]
    all_data["products"] = db_price["product_name"]
    regions = []
    for country in all_data["names"]:
        regions.append(scatter_plot.REGION_ID_2_NAME[scatter_plot.COUNTRY_2_REGION[country]])
    all_data["regions"] = regions

    print("\n\nNames:")
    print(all_data["names"])
    print("Products:")
    print(all_data["products"])
    print("Regions:")
    print(all_data["regions"])

    # Do a random permutation
    rndperm = np.random.permutation(all_data.shape[0])
    x = all_data.loc[rndperm[:permutation_size],:].copy()
    x = x.reset_index()
    names = x["names"].copy()
    regions = x["regions"].copy()
    products = x["products"].copy()
    x = x.drop(["names", "regions", "products"], axis=1)

    # Do K-Means and shit
    print("    (Total number of elements: {})".format(counter))
    print("  - Doing K-Means...")
    path_clusters = "clusters.txt"
    if file_exists(path_clusters):
        print("    - Loading perfect cluster amount...")
        with open(path_clusters, "r") as f:
            n_clusters = int(f.read())
        print("    - Done (using {} clusters)".format(n_clusters))
    else:
        progress_bar = ProgressBar(min_amount=1, max_amount=20)
        inertias = []
        for i in range(1,20):
            progress_bar.update_preceding_text("    - Testing K-Means on n_clusters={}...".format(i))
            model = KMeans(n_clusters = i)
            model.fit(x)
            inertias.append(model.inertia_)
            progress_bar.update()

        # Show the lbow graph
        figure = plt.figure(title="Elbow graph", x_axis_label = "N of clusters", y_axis_label = "Inertia")
        figure.line(range(1, 20), inertias, color="red")
        plt.show(figure)

        print("      Select the good amount of clusters:\n      ",end="")
        n_clusters = input()
        while not is_int(n_clusters) or int(n_clusters) < 1 or int(n_clusters) > 20:
            print("      Enter a number ranging 1-20!\n      ",end="")
            n_clusters = input()
        n_clusters = int(n_clusters)
        print("    - Saving...")
        with open(path_clusters, "w") as f:
            f.write(str(n_clusters))

    print("  - Actually performing K-Means...")
    model = KMeans(n_clusters = n_clusters)
    model.fit(x)

    path_kmeans = "kmeans_result.txt"
    path_tsne = "tsne_result.txt"
    with open(path_kmeans, "w") as f:
        f.write(str(model.labels_))

    # Do colors, if desired
    if with_colors:
        x["colors"] = model.labels_

    print("  - Using TSNE to reduce dimensions...")
    start = time.time()
    x_embedded = TSNE(verbose=2, n_iter=1000).fit_transform(x.values)
    time_taken = time.time() - start
    with open(path_tsne, "w") as f:
        f.write(str(x_embedded))

    print("\n  - Done (took {}m{}s, result saved to {}".format(time_taken // 60, time_taken % 60, path_tsne))

    y = pd.DataFrame()
    y["t-SNE X"] = x_embedded[:,0]
    y["t-SNE Y"] = x_embedded[:,1]
    y["regions"] = regions
    y["names"] = names
    y["products"] = products
    y["colors"] = model.labels_

    print("Done")

    path_html = "t_sne_"
    i = 0
    while file_exists(path_html + str(i) + ".html"):
        i += 1
    path_html += str(i) + ".html"

    # Show the graph
    print("Showing graphs...")
    display_graphs(graphs=graphs)
    print("Showing overview graph...")
    display_graphs(("Overview K-Means", y), columns="t-SNE X,t-SNE Y", path=path_html)
    print("Done.")

# Entry point
if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)

    # Do some arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-ib", "--input_path_bmi", help="The path to the BMI database")
    parser.add_argument("-s", "--sample_size", type=int, help="The number of elements that will be taken from the database.")
    parser.add_argument("-c", "--colours", action="store_true", help="If given, the program will include the labels given by K-Means while reducing dimensions")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/git/Ignored/foodprices2 unified better.csv"
    input_path_bmi = "/Users/Tim/UvA/DAV/git/BMI-Data-Less.csv"
    permutation_size = 10000
    with_colours = False
    if args.input_path:
        input_path = args.input_path
    if args.input_path_bmi:
        input_path_bmi = args.input_path_bmi
    if args.sample_size:
        permutation_size = args.sample_size
    if args.colours:
        with_colours = True


    try:
        main (input_path, input_path_bmi, permutation_size, with_colours)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit()

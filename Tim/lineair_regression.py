# K-MEANS: Use the K-Means algorithm to analyse databases

######################## CHANGELOG ########################
###########################################################
## v0.1 (alpha):                                         ##
##   + Begun alpha development                           ##
###########################################################
## v0.2 (alpha):                                         ##
##   o Used custom collect_graphs instead of using that  ##
##     of scatter_plot.py                                ##
###########################################################
## v0.3 (alpha):                                         ##
##   o Changed two-in-one graph to two seperate graphs   ##
##     for overview (and error avoidance 0:) )           ##
###########################################################
## v1.0:                                                 ##
##   o Switched status to release                        ##
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


def plot_lineair_regression (figure, x, y):
    # Doin' some magic
    X = np.vstack(x)
    X = np.column_stack((X, np.ones(X.shape[0])))

    # Now get out m and b values for our best fit line
    a, b = np.linalg.lstsq(X, y)[0]
    print("Lineair regression result: y = {}x + {}".format(a, b))
    y = []
    for number in x:
        y.append(a * number + b)

    # Plot
    source = bkm.ColumnDataSource(data={"year":x, "value":y})
    linreg = figure.line("year", "value", source=source, color=("red" if range=="Price" else "blue"), muted_color=("red" if range=="Price" else "blue"), muted_alpha=0.2)

    return ("Linear Regression ({})".format(range), [linreg])

def get_random_rgb (RGBs):
    rand = random.randint(0, len(RGBs) - 1)
    to_return = RGBs[rand]
    RGBs = RGBs[:rand] + RGBs[rand + 1:]
    return (to_return, RGBs)

def plot_list (figure, x_list, y_list, country, RGBs):
    country = [country] * len(x_list)
    data = {"year":x_list, "value":y_list, "country":country}
    source = bkm.ColumnDataSource(data=data)

    RGB, RGBs = get_random_rgb(RGBs)
    line = figure.line("year", "value", source=source, color=RGB, alpha=0.5, muted_color=RGB, muted_alpha=0)
    circle = figure.circle("year", "value", source=source, line_color=RGB, alpha=0.5, fill_color="white", muted_line_color=RGB, muted_fill_color="white", muted_alpha=0)

    # Done, return
    return (line, circle, RGBs)

# Hiarchy:
#   product
#       region
#           time
#               (x_list:{"country":10}, y_list:{"country":0.90})
def collect_graphs (db_prices, db_BMI):
    print("  - Collecting info...")
    data_list = {}
    total_things = 0
    progress_bar = ProgressBar(ending_character="", max_amount=len(db_prices), preceding_text="   ")
    for row in db_prices.itertuples():
        country = row.country_name
        timestamp = row.year

        if "rice" not in row.product_name.lower():
            progress_bar.update()
            continue

        if country == "Myanmar" or country == "Syrian Arab Republic":
            progress_bar.update()
            continue

        # Add year
        if timestamp not in data_list:
            data_list[timestamp] = {}

        # Add country
        if country not in data_list[timestamp]:
            data_list[timestamp][country] = {"price":(0,0), "BMI":(0,0)}
            total_things += 1

        # Now get the BMI index of the country at that time
        column_index = str(timestamp) + " - Both sexes"
        row_index = country

        counter_BMI, total_BMI = data_list[timestamp][country]["BMI"]
        counter_price, total_price = data_list[timestamp][country]["price"]

        try:
            new_BMI = db_BMI[column_index][scatter_plot.COUNTRY_2_ID[country]]
        except KeyError as e:
            print("\033[F\033[K  - Collecting info... (Could not read {} from BMI)".format(e))
        else:
            total_BMI += new_BMI
            counter_BMI += 1
            total_price += row.standardized_prices
            counter_price += 1

            data_list[timestamp][country] = {"BMI":(counter_BMI, total_BMI), "price":(counter_price, total_price)}

        progress_bar.update()

    print("\033[K\033[F\033[K", end="")

    # New list array:
    # product
    #   country
    #       ({2016:5, 2017:9}}, {1999:3, 2000:6}) // tuple of X by Y (price by BMI)


    # Now that we have a data_list, convert it into a graph list
    print("  - Constructing graph data...")
    progress_bar = ProgressBar(ending_character="", max_amount=total_things, preceding_text="   ")
    price_list = {}
    BMI_list = {}
    price_year_list = {}
    BMI_year_list = {}
    if not average:
        # If not average, create three lists:
        # price_list / BMI_list: [country:[price1/BMI1, price2/BMI2, ...], ...]
        # year_list: [country:[year1, year2, ...], ...]
        for timestamp in data_list:
            for country in data_list[timestamp]:
                # Make sure the countries are present
                if country not in price_list:
                    price_list[country] = []
                if country not in BMI_list:
                    BMI_list[country] = []
                if country not in price_year_list:
                    price_year_list[country] = []
                if country not in BMI_year_list:
                    BMI_year_list[country] = []
                counter_price, total_price = data_list[timestamp][country]["price"]
                counter_BMI, total_BMI = data_list[timestamp][country]["BMI"]

                if counter_price == 0:
                    counter_price = 1
                if counter_BMI == 0:
                    counter_BMI = 1

                # Add all to the list
                if total_price / counter_price > 0:
                    price_list[country].append(total_price / counter_price)
                    price_year_list[country].append(timestamp)
                if total_BMI / counter_BMI > 0:
                    BMI_list[country].append(total_BMI / counter_BMI)
                    BMI_year_list[country].append(timestamp)
                progress_bar.update()
    else:
        # Else:
        # price_list / BMI_list: ["all":[price1, price2, ...]]
        # year_list: ["all":[year1, year2, ...], ...]
        price_list["all"] = []
        BMI_list["all"] = []
        price_year_list["all"] = []
        BMI_year_list["all"] = []
        for timestamp in data_list:
            year_average_price_total = 0
            year_average_price_counter = 0
            year_average_BMI_total = 0
            year_average_BMI_counter = 0
            for country in data_list[timestamp]:
                counter_price, total_price = data_list[timestamp][country]["price"]
                counter_BMI, total_BMI = data_list[timestamp][country]["BMI"]

                if counter_price == 0:
                    counter_price = 1
                if counter_BMI == 0:
                    counter_BMI = 1

                year_average_price_total += (total_price / counter_price)
                year_average_price_counter += 1
                year_average_BMI_total += (total_BMI / counter_BMI)
                year_average_BMI_counter += 1
                progress_bar.update()

            if year_average_price_total / year_average_price_counter > 0:
                price_list["all"].append(year_average_price_total / year_average_price_counter)
                price_year_list["all"].append(timestamp)
            if year_average_BMI_total / year_average_BMI_counter > 0:
                BMI_list["all"].append(year_average_BMI_total / year_average_BMI_counter)
                BMI_year_list["all"].append(timestamp)

    # Sort on y_list
    for country in price_list:
        if len(price_list[country]) > 0 and len(price_year_list[country]) > 0:
            new_years, new_price = zip(*sorted(zip(price_year_list[country], price_list[country])))
            price_list[country] = list(new_prices)
            price_year_list[country] = list(new_years)
    for country in BMI_list:
        if len(BMI_list[country]) > 0 and len(BMI_year_list[country]) > 0:
            new_years, new_BMI = zip(*sorted(zip(BMI_year_list[country], BMI_list[country])))
            BMI_list[country] = list(new_BMI)
            BMI_year_list[country] = list(new_years)

    return (price_list, BMI_list, price_year_list, BMI_year_list, total_things)

# MAIN
def main (input_path, input_path_bmi, average):
    # Welcoming message
    print("\n############################")
    print("##   LINEAIR REGRESSION   ##")
    print("##          v1.0          ##")
    print("############################\n")

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

    # Custom
    print("Collecting graphs...")
    price, BMI, price_years, BMI_years, total_things = collect_graphs (db_price, db_BMI)
    print("\nDone")

    # Now plot price VS time
    print("Plotting...")

    # Create hover tool
    hover = bkm.HoverTool(tooltips=[("Country", "@country"), ("Year", "@year"), ("Value", "@value")])

    # Create figure
    f_price = plt.figure(title="Price per country, with Lineair Regression", x_axis_label = "Years", y_axis_label = "Price", tools=[hover, bkm.WheelZoomTool(), bkm.BoxZoomTool(), bkm.PanTool(), bkm.SaveTool(), bkm.ResetTool()], width=900)
    f_BMI = plt.figure(title="BMI per country, with Lineair Regression", x_axis_label = "Years", y_axis_label = "BMI", tools=[hover, bkm.WheelZoomTool(), bkm.BoxZoomTool(), bkm.PanTool(), bkm.SaveTool(), bkm.ResetTool()], width=900)

    # Generate random RGB list
    RGBs = []
    N = 8
    for r in range(N):
        for g in range(N):
            for b in range(N):
                if r == g == b == N:
                    # NO WHITE
                    continue
                # Add to the RGBs list
                RGBs.append(bokeh.colors.RGB(int((r / N) * 255), int((g / N) * 255), int((b / N) * 255)))

    legend_list_price = []
    legend_list_BMI = []
    total_x_price = []
    total_x_BMI = []
    total_y_price = []
    total_y_BMI = []
    progress_bar = ProgressBar(max_amount=len(price))
    for country in price:
        price_list = price[country]
        BMI_list = BMI[country]
        price_year_list = price_years[country]
        BMI_year_list = BMI_years[country]

        # Now plot the graph
        line_elem, circle_elem, new_RGBs = plot_list (f_price, price_year_list, price_list, country, RGBs)
        RGBs = list(new_RGBs)
        legend_list_price.append((country + " (price)", [line_elem, circle_elem]))
        # Do the same for BMI
        line_elem, circle_elem, new_RGBs = plot_list (f_BMI, BMI_year_list, BMI_list, country, RGBs)
        RGBs = list(new_RGBs)
        legend_list_BMI.append((country + " (BMI)", [line_elem, circle_elem]))

        # Add to the total_x and total_y
        total_x_price += price_list
        total_x_BMI += BMI_list
        total_y_price += price_year_list
        total_y_BMI += BMI_year_list
        progress_bar.update()

    print("Done")

    # Alright, we're nearly done: only add lineair regression
    print("Doing lineair regression...")
    legend_list_price.append(plot_lineair_regression(f_price, total_y_price, total_x_price))
    legend_list_BMI.append(plot_lineair_regression(f_BMI, total_y_BMI, total_x_BMI))

    # Do legend and show
    legend_price = bkm.Legend(items=legend_list_price, location=(0,0), click_policy="mute")
    legend_BMI = bkm.Legend(items=legend_list_BMI, location=(0,0), click_policy="mute")

    f_price.add_layout(legend_price, "right")
    f_BMI.add_layout(legend_BMI, "right")

    print("Done")

    plt.output_file("lineair_regression.html", mode="inline")
    layout = bokeh.layouts.Column(
        f_price,
        f_BMI
    )
    plt.show(layout)

    print("\nDone.")



# Entry Point
if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)

    # Do some arg parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-ib", "--input_path_bmi", help="The path to the BMI database")
    parser.add_argument("-a", "--average", action="store_true", help="Use the average of the countries to plot one line instead of multiple")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/Ignored/foodprices2 unified better.csv"
    input_path_bmi = "/Users/Tim/UvA/DAV/BMI-Data-Less.csv"
    average = False
    if args.input_path:
        input_path = args.input_path
    if args.input_path_bmi:
        input_path_bmi = args.input_path_bmi
    if args.average:
        average = True


    try:
        main (input_path, input_path_bmi, average)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit()

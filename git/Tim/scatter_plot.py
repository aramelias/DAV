# Makes a scatter plot of BMI vs sales of countries, sorted by time and product,
#   with each country it's own colour for the region it resides in.

##################### CHANGELOG #####################
# v0.1 (alpha):                                     #
#   + Begun Alpha development                       #
#####################################################
# v0.2 (alpha):                                     #
#   o Swapped from using bokeh to genereate PNG's   #
#     and converting those to GIFs, to generating   #
#     interactive HTML-files                        #
#####################################################
# v0.3 (alpha):                                     #
#   o Switched to generating several scatter plots  #
#     to minimize computing power and add labels    #
#####################################################
# v0.4 (alpha):                                     #
#   o Undone last adjustment, due to incompatible   #
#     legend desireables                            #
#####################################################
# v1.0:                                             #
#   o Switched status to released! (All main        #
#     functions are present)                        #
#####################################################
# v2.0:                                             #
#   o Swapped back to generating scatters instead   #
#     of individual circles, as the origin for the  #
#     legend problem was found...                   #
#####################################################

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


callback_code = """
    var slider_value = cb_obj.value;
    for (var i = 0; i < sources.length; i++) {
        var source = sources[i][0];
        var region = sources[i][1];
        var changed = false;
        for (r in all_data) {
            if (r == region) {
                // Right region
                for (year in all_data[r]) {
                    if (year == slider_value) {
                        // Right year
                        source.data = all_data[r][year];
                        changed = true;
                        break;
                    }
                }
            }
        }
        if (!changed) {
            source.data["x"] = 0
            source.data["y"] = 0
        }

        // Update
        source.change.emit();
    }
"""


XLABEL = "Price (usd)"
YLABEL = "BMI"

COUNTRY_2_ID = {
    "Afghanistan":0,
    "Algeria":1,
    "Armenia":2,
    "Azerbaijan":3,
    "Bangladesh":4,
    "Benin":5,
    "Bhutan":6,
    "Bolivia (Plurinational State of)":7,
    "Burkina Faso":8,
    "Burundi":9,
    "Cabo Verde":10,
    "Cambodia":11,
    "Cameroon":12,
    "Central African Republic":13,
    "Chad":14,
    "Colombia":15,
    "Congo":16,
    "Costa Rica":17,
    "Cote d'Ivoire":18,
    "Democratic Republic of the Congo":19,
    "Djibouti":20,
    "Egypt":21,
    "El Salvador":22,
    "Ethiopia":23,
    "Gambia":24,
    "Georgia":25,
    "Ghana":26,
    "Guatemala":27,
    "Guinea":28,
    "Guinea-Bissau":29,
    "Haiti":30,
    "Honduras":31,
    "India":32,
    "Indonesia":33,
    "Iran (Islamic Republic of)":34,
    "Iraq":35,
    "Jordan":36,
    "Kenya":37,
    "Kyrgyzstan":38,
    "Lao People's Democratic Republic":39,
    "Lebanon":40,
    "Lesotho":41,
    "Liberia":42,
    "Madagascar":43,
    "Malawi":44,
    "Mali":45,
    "Mauritania":46,
    "Mozambique":47,
    "Myanmar":48,
    "Nepal":49,
    "Niger":50,
    "Nigeria":51,
    "Pakistan":52,
    "Panama":53,
    "Peru":54,
    "Philippines":55,
    "Rwanda":56,
    "Senegal":57,
    "Somalia":58,
    "Sri Lanka":59,
    "Swaziland":60,
    "Syrian Arab Republic":61,
    "Tajikistan":62,
    "Timor-Leste":63,
    "Turkey":64,
    "Uganda":65,
    "Ukraine":66,
    "United Republic of Tanzania":67,
    "Yemen":68,
    "Zambia":69,
    "Zimbabwe":70
}
REGION_ID_2_NAME = {
    1: 'Noord-Afrika', 2: 'Arabische Wereld', 3: 'Voormalig Sovjet Gebied', 4: 'Zuid Azie', 5: 'West Afrika', 6: 'Zuid Amerika', 7: 'Midden Afrika', 8: 'Zuid Oost Azie', 9: 'Midden Amerika', 10: 'Oost Afrika', 11: 'Zuidelijk Afrika', 12:"Eilanden"
}
COUNTRY_2_REGION = {
    'Afghanistan':1, 'Algeria':1, 'Sudan':1, 'Egypt':1, 'Niger':1, 'Chad':1,
    'Iran  (Islamic Republic of)':2, 'Iraq':2, 'Jordan':2, 'Lebanon':2, 'Pakistan':2, 'Syrian Arab Republic':2, 'Turkey':2, 'Yemen':2, 'State of Palestine':2,
    'Armenia':3, 'Azerbaijan':3, 'Georgia':3, 'Kyrgyzstan':3, 'Tajikistan':3, 'Ukraine':3,
    'Bangladesh':4, 'Bhutan':4, 'India':4, 'Nepal':4,
    'Benin':5, 'Burkina Faso':5, "Cote d'Ivoire":5, 'Gambia':5, 'Ghana':5, 'Guinea-Bissau':5, 'Guinea':5, 'Liberia':5, 'Mali':5, 'Mauritania':5, 'Nigeria':5, 'Senegal':5,
    'Bolivia':6, 'Colombia':6, 'Peru':6,
    'Burundi':7, 'Central African Republic':7, 'Congo':7, 'Democratic Republic of the Congo':7, 'Rwanda':7, 'Uganda':7, 'United Republic of Tanzania':7, 'South Sudan':7,
    'Cambodia':8, 'Myanmar':8, 'Indonesia':8, "Lao People's Democratic Republic":8, 'Timor-Leste':8,
    'Costa Rica':9, 'El Salvador':9, 'Guatemala':9, 'Honduras':9, 'Panama':9,
    'Djibouti':10, 'Ethiopia':10, 'Kenya':10, 'Somalia':10,
    'Lesotho':11, 'Malawi':11, 'Mozambique':11, 'Swaziland':11, 'Zambia':11, 'Zimbabwe':11,
    'Cameroon':12, 'Cape Verde':12, 'Haiti':12, 'Madagascar':12, 'Philippines':12, 'Sri Lanka':12
}
REGION_NAME_2_COLOR = {
    'Noord-Afrika': (235, 235, 0), # Yellow
    'Arabische Wereld': (255, 158, 0), # Orangy
    'Voormalig Sovjet Gebied': (128, 128, 190), # Blue / Purple
    'Zuid Azie': (0, 108, 0), # Dark Green
    'West Afrika': (224, 63, 0),  # Red Orangy
    'Zuid Amerika': (0, 188, 126), # Bluey green
    'Midden Afrika': (178, 203, 0), # Greeny yellow
    'Zuid Oost Azie': (0, 178, 0), # Deep green
    'Midden Amerika': (0, 255, 0), # Bright green
    'Oost Afrika': (100, 0, 0), # Dark Red
    'Zuidelijk Afrika': (255, 0, 0), # Red
    "Eilanden": (0, 188, 254) # Sea blue
}


def do_graph_animation (graph_product, title, path, progress_bar):
    # The total graph info
    plt.output_file(path, mode="inline")

    hover = bkm.HoverTool(tooltips=[("Country", "@names"), ("Region", "@region")])

    f = plt.figure(title=title, x_axis_label = XLABEL, y_axis_label = YLABEL, tools=[hover, bkm.WheelZoomTool(), bkm.BoxZoomTool(), bkm.PanTool(), bkm.SaveTool(), bkm.ResetTool()], width=900)

    legend_list = []

    sources = []
    data = {}
    country_data = {}

    lowest_year = float("inf")
    highest_year = -float("inf")

    lowest_price = float("inf")
    highest_price = -float("inf")

    lowest_BMI = float("inf")
    highest_BMI = -float("inf")

    # Construct the new plot
    for region in graph_product:
        if region not in country_data:
            country_data[region] = {}
        lowest_region_year = float("inf")
        for timestamp in graph_product[region]:
            x_list, y_list = graph_product[region][timestamp]
            # Create the dataset
            data = {"x":[], "y":[], "names":[], "region":[]}
            for country in x_list:
                country_price = x_list[country]
                country_BMI = y_list[country]

                # Take care we get some limits
                if timestamp < lowest_year:
                    lowest_year = timestamp
                if timestamp < lowest_region_year:
                    lowest_region_year = timestamp
                if timestamp > highest_year:
                    highest_year = timestamp
                if country_price < lowest_price:
                    lowest_price = country_price
                if country_price > highest_price:
                    highest_price = country_price
                if country_BMI < lowest_BMI:
                    lowest_BMI = country_BMI
                if country_BMI > highest_BMI:
                    highest_BMI = country_BMI

                # Save the data
                data["x"].append(country_price)
                data["y"].append(country_BMI)
                data["names"].append(country)
                data["region"].append(region)

            # Append country_data
            country_data[region][timestamp] = data


        # Now create a nice source of the data
        data_source = bokeh.models.ColumnDataSource(data=country_data[region][lowest_region_year])
        sources.append([data_source, region])

        # Now plot it
        region_color = REGION_NAME_2_COLOR[region]
        elem = f.scatter("x", "y", source=data_source, color=region_color, muted_color=region_color, muted_alpha=0.1, size=10)

        # Add elem to the legends
        legend_list.append((region, [elem]))


        # Do dat progress bar
        progress_bar.update()
        first_time = False

    legend = bokeh.models.Legend(items=legend_list, location=(0,0), click_policy="mute")

    f.x_range = bkm.DataRange1d(start=lowest_price, end=highest_price)
    f.y_range = bkm.DataRange1d(start=lowest_BMI, end=highest_BMI)

    # Make the slider
    callback = bokeh.models.CustomJS(args=dict(sources=sources, all_data=country_data), code=callback_code)
    slider = bokeh.models.Slider(start=lowest_year, end=highest_year, value=lowest_year, step=1, title="Year")
    slider.js_on_change('value', callback)

    f.add_layout(legend, 'right')

    layout = bokeh.layouts.row(
        f,
        bokeh.layouts.widgetbox(slider)
    )
    plt.save(layout)

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
        product = row.product_name
        country = row.country_name

        if "rice" in product.lower():
            product = "Rice"

        # Now create
        if product not in data_list:
            data_list[product] = {}

        # Add region
        region = REGION_ID_2_NAME[COUNTRY_2_REGION[country]]
        if region not in data_list[product]:
            data_list[product][region] = {}
            total_things += 1

        # Create a datetime object
        timestamp = row.year
        if timestamp not in data_list[product][region]:
            data_list[product][region][timestamp] = {}

        # Add country
        if country not in data_list[product][region][timestamp]:
            data_list[product][region][timestamp][country] = {"BMI":(0, 0), "Price":(0, 0)}


        # Now get the BMI index of the country at that time
        column_index = str(timestamp) + " - Both sexes"
        row_index = country

        counter_BMI, total_BMI = data_list[product][region][timestamp][country]["BMI"]
        counter_price, total_price = data_list[product][region][timestamp][country]["Price"]

        try:
            new_BMI = db_BMI[column_index][COUNTRY_2_ID[country]]
        except KeyError as e:
            print("\033[F\033[K  - Collecting info... (Could not read {} from BMI)".format(e))
        else:
            total_BMI += new_BMI
            counter_BMI += 1
            total_price += row.standardized_prices
            counter_price += 1

            data_list[product][region][timestamp][country] = {"BMI":(counter_BMI, total_BMI), "Price":(counter_price, total_price)}

        progress_bar.update()

    print("\033[K\033[F\033[K", end="")

    # New list array:
    # product
    #   country
    #       ({2016:5, 2017:9}}, {1999:3, 2000:6}) // tuple of X by Y (price by BMI)


    # Now that we have a data_list, convert it into a graph list
    print("  - Constructing graph data...")
    progress_bar = ProgressBar(ending_character="", max_amount=total_things, preceding_text="   ")
    for product in data_list:
        for region in data_list[product]:
            for timestamp in data_list[product][region]:
                x_list = {}
                y_list = {}
                for country in data_list[product][region][timestamp]:
                    counter_BMI, total_BMI = data_list[product][region][timestamp][country]["BMI"]
                    counter_price, total_price = data_list[product][region][timestamp][country]["Price"]
                    if counter_price == 0:
                        counter_price += 1
                    if counter_BMI == 0:
                        counter_BMI += 1
                    x_list[country] = total_price / counter_price
                    y_list[country] = total_BMI / counter_BMI
                # Sort
                data_list[product][region][timestamp] = (x_list, y_list)
                progress_bar.update()
    return (data_list, total_things)


# Run main code
def main (input_path, input_path_bmi, output_path):
    # Do welcome
    print("\n##################")
    print("## SCATTER PLOT ##")
    print("##     v2.0     ##")
    print("##################\n")

    print("USING PATHS:")
    print("  - Prices DB:     {}".format(input_path))
    print("  - BMI DB:        {}".format(input_path_bmi))
    print("  - Output folder: {}".format(output_path))

    # Read DB
    print("\nReading database...")
    db_price = pd.read_csv(input_path)
    print("Done, reading BMI-database...")
    db_bmi = pd.read_csv(input_path_bmi)
    print("Done")

    # Fill NaN
    db_price = db_price.fillna(0)
    db_bmi = db_bmi.fillna(0)

    # Time to convert database to desired scatter_plot format
    print("Creating scatter plots...")
    scatter_plots, total_things = collect_graphs (db_price, db_bmi)

    # Now we have graphs, time to save them to the disk
    print("\033[K\033[F\033[K", end="")
    print("  - Saving graphs...")
    progress_bar = ProgressBar(preceding_text = "   ", ending_character="", max_amount = total_things)
    for product in scatter_plots:
        dir_path = output_path
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        filename = product.replace("/", " or ") + ".html"
        do_graph_animation (scatter_plots[product], "Scatter plot of {} over time".format(product.lower()), dir_path + filename, progress_bar)
    print("\nDone.")


# Entry point
if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-ib", "--input_path_bmi", help="The path to the BMI database.")
    parser.add_argument("-o", "--output_path", help="The path of the resulting database")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/Ignored/foodprices2 unified better.csv"
    input_path_bmi = "/Users/Tim/UvA/DAV/BMI-Data-Less.csv"
    output_path = "/Users/Tim/UvA/DAV/Tim/Ignored/scatter_plots"
    if args.input_path:
        input_path = args.input_path
    if args.input_path_bmi:
        input_path_bmi = args.input_path_bmi
    if args.output_path:
        output_path = args.output_path

    # Make sure output_path exists with a '/'
    if output_path[-1] != "/":
        output_path += "/"

    # Run main with KeyboardInterrupt Handling
    try:
        main(input_path, input_path_bmi, output_path)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit()

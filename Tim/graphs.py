# Makes graphs of the data. More specific, it makes graphs of the price of
#   every product, per product, per country


################# CHANGELOG #################
# v1.0:                                     #
#   + Basic functionality                   #
#############################################
# v3.0:                                     #
#   o Total rewrite, in order to allow for  #
#     bokeh, and easier graph management    #
#############################################


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


XLABEL = "Time (years)"
YLABEL = "Price (usd)"

day_2_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

REGION_ID_2_NAME = {
    1: 'Noord-Afrika', 2: 'Arabische Wereld', 3: 'Voormalig Sovjet Gebied', 4: 'Zuid Azie', 5: 'West Afrika', 6: 'Zuid Amerika', 7: 'Midden Afrika', 8: 'Zuid Oost Azie', 9: 'Midden Amerika', 10: 'Oost Afrika', 11: 'Zuidelijk Afrika', 12:"Eilanden"
}
COUNTRY_2_REGION = {
    'Algeria':1, 'Sudan':1, 'Egypt':1, 'Niger':1, 'Chad':1,
    'Iran  (Islamic Republic of)':2, 'Iraq':2, 'Jordan':2, 'Lebanon':2, 'Pakistan':2, 'Syrian Arab Republic':2, 'Turkey':2, 'Yemen':2, 'State of Palestine':2, 'Afghanistan':2,
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


# Class to style bokeh lines
class LineStylist ():
    def __init__(self, unique_rgbs=8, width=2):
        self.width = width
        self.dash_counter = 0
        self.unique_rgbs = unique_rgbs
        # Generate unique RGB list

        # Check unique_RGB
        if unique_rgbs < 1:
            unique_rgbs = 1

        self.generate_rgb_list()

    def generate_rgb_list (self):
        # Now generate
        self.RGBs = []
        N = self.unique_rgbs
        for r in range(N):
            for g in range(N):
                for b in range(N):
                    if r == g == b == N:
                        # NO WHITE
                        continue
                    # Add to the RGBs list
                    self.RGBs.append((int((r / N) * 255), int((g / N) * 255), int((b / N) * 255)))

    # Return a random RGB colour from the list generated on init
    def get_random_rgb (self):
        rand = random.randint(0, len(self.RGBs) - 1)
        to_return = self.RGBs[rand]
        self.RGBs = self.RGBs[:rand] + self.RGBs[rand + 1:]
        return to_return

    # Return a line style, based on current counter
    def get_line_style (self):
        line_dash = [2, 0]
        for i in range(self.dash_counter):
            if i % 2:
                line_dash[0] += 2
            else:
                line_dash[1] += 2
        self.dash_counter = (self.dash_counter + 1) % 8
        return line_dash

    def reset (self):
        self.dash_counter = 0

    # Style a line
    def style(self, figure, x_list, y_list, legend_label, color="", legend=True):
        # Draw the line with fixed width, legend
        if color == "":
            color = self.get_random_rgb()
        if legend:
            figure.line(x_list, y_list, line_width=self.width, legend=legend_label, color=color, line_dash=self.get_line_style())
        else:
            figure.line(x_list, y_list, line_width=self.width, color=color, line_dash=self.get_line_style())

        # Filled circle
        figure.circle(x_list, y_list, line_color=color, fill_color=color, size=4)



def is_int (x):
    try:
        int(x)
        return True
    except ValueError:
        return False


# Function to return a list of graphs:
#   {"sort_1":{"sort_2":[[1,2],[3,4]]}}
#   <       First sorted              >
#             <     Second sorted    >
#                      <   Graphs   >
#                        <GRF> <GRF>
# TODO: Add year / month timescale
def collect_graphs (db, mode, use_years):
    print("  - Collecting {} info...".format(mode))
    data_list = {}
    total_things = 0
    progress_bar = ProgressBar(ending_character="", max_amount=len(db), preceding_text="   ")
    for row in db.itertuples():
        # Set the first and second order sorting
        if mode == "products":
            first_order = row.product_name
            secnd_order = row.country_name
        elif mode == "countries":
            first_order = row.country_name
            secnd_order = row.product_name
        elif mode == "regions":
            # Now create

            # Quickly eliminate all rice things
            if "rice" not in row.product_name.lower() or row.country_name == "Myanmar":
                # Shame, kys
                progress_bar.update()
                continue

            region = REGION_ID_2_NAME[COUNTRY_2_REGION[row.country_name]]
            if region not in data_list:
                data_list[region] = {}
            if row.country_name not in data_list[region]:
                data_list[region][row.country_name] = {}
                total_things += 1

            # Create datetime object
            if use_years:
                timestamp = datetime.date(row.year, 12, 31)
            else:
                timestamp = datetime.date(row.year, row.month, day_2_month[row.month - 1])
            if timestamp not in data_list[region][row.country_name]:
                data_list[region][row.country_name][timestamp] = (0, 0)

            counter, total = data_list[region][row.country_name][timestamp]
            data_list[region][row.country_name][timestamp] = (counter + 1, total + row.standardized_prices)
            progress_bar.update()
        else:
            print("Pattern {} is unknown, skipping...".format(mode))
            return False

        if mode != "regions":
            # Now create
            if first_order not in data_list:
                data_list[first_order] = {}
            if secnd_order not in data_list[first_order]:
                data_list[first_order][secnd_order] = {}
                total_things += 1
            if "unit" not in data_list[first_order][secnd_order]:
                data_list[first_order][secnd_order]["unit"] = row.standardized_units

            # Create a datetime object
            if use_years:
                timestamp = datetime.date(row.year, 12, 31)
            else:
                timestamp = datetime.date(row.year, row.month, day_2_month[row.month - 1])

            if timestamp not in data_list[first_order][secnd_order]:
                data_list[first_order][secnd_order][timestamp] = (0, 0)

            counter, total = data_list[first_order][secnd_order][timestamp]
            data_list[first_order][secnd_order][timestamp] = (counter + 1, total + row.standardized_prices)
            progress_bar.update()

    print("\033[K\033[F\033[K", end="")

    # Now that we have a data_list, convert it into a graph list
    print("  - Constructing graph data...")
    progress_bar = ProgressBar(ending_character="", max_amount=total_things, preceding_text="   ")
    all_dates = []
    for first_order in data_list:
        for secnd_order in data_list[first_order]:
            x_list = []
            y_list = []
            for timestamp in data_list[first_order][secnd_order]:
                if timestamp != "unit":
                    x_list.append(timestamp)
                    counter, total = data_list[first_order][secnd_order][timestamp]
                    y_list.append(total / counter)
                    if timestamp not in all_dates:
                        all_dates.append(timestamp)
            # Sort
            x_list, y_list = (list(t) for t in zip(*sorted(zip(x_list, y_list))))
            data_list[first_order][secnd_order] = (x_list, y_list)
            progress_bar.update()
    all_dates = sorted(all_dates)

    print("\033[K\033[F\033[K", end="")

    # Now make all the graphs the same size, to avoid confusion
    print("  - Fixating graph length...")
    progress_bar = ProgressBar(ending_character="", max_amount=total_things, preceding_text="   ")
    for first_order in data_list:
        for secnd_order in data_list[first_order]:
            x_list, y_list = data_list[first_order][secnd_order]
            for timestamp in all_dates:
                if timestamp not in x_list:
                    x_list, y_list = insert_sorted(timestamp, x_list, y_list)
            data_list[first_order][secnd_order] = (x_list, y_list)
            progress_bar.update()
    return (data_list, total_things, all_dates)

# Insert an element into both list, so list1 is still sorted
def insert_sorted (element, list1, list2):
    pre_list1 = []
    aft_list1 = list1
    pre_list2 = []
    aft_list2 = list2
    while len(aft_list1) > 0 and element > aft_list1[0]:
        pre_list1 += [aft_list1[0]]
        aft_list1 = aft_list1[1:]
        pre_list2 += [aft_list2[0]]
        aft_list2 = aft_list2[1:]
    return (pre_list1 + [element] + aft_list1, pre_list2 + [(0 if use_years else np.nan)] + aft_list2)

# Saves or shows a graph
def do_graph (tier1, graphs, path, title):
    # User wants to see an overview
    plt.output_file(path, mode="inline")

    f = plt.figure(title=title.format(tier1), x_axis_label=XLABEL, y_axis_label=YLABEL, x_axis_type="datetime", plot_width = 800)

    line_stylist = LineStylist()
    for tier2 in graphs[tier1]:
        color = line_stylist.get_random_rgb()
        x_list, y_list = graphs[tier1][tier2]
        line_stylist.style(f, x_list, y_list, tier2, color=color)
        line_stylist.reset()

    # Save the graph instead
    plt.save(f)

def do_graph_singular (x_list, y_list, title, path):
    # Save the graph
    plt.output_file(path, mode="inline")
    f = plt.figure(title=title, x_axis_label = XLABEL, y_axis_label = YLABEL, x_axis_type="datetime", plot_width = 800)
    line_stylist = LineStylist()
    line_stylist.style(f, x_list, y_list, title, legend=False)
    plt.save(f)


# Main function
def main (input_path, output_path, use_years, overview_graphs, overview_only, sort_by):
    # Make sure it ends with "/"
    if output_path[-1] != "/":
        output_path += "/"

    # Welcome message
    print("\n############")
    print("## GRAPHS ##")
    print("##  v3.0  ##")
    print("############\n")

    if use_years:
        print("Timescale: years\n")
    else:
        print("Timescale: months")
        print("(use '--years' to use years)\n")

    # Read DB
    print("Reading database...")
    database = pd.read_csv(input_path)
    print("Done")

    # Time 2 create sum graphs
    print("Creating specific graphs...")
    total_graphs = 0
    if overview_only:
        print("  - Skipping because of given flag...")
    else:
        graphs, total_tier2, all_dates = collect_graphs(database, sort_by, use_years)
        print("\033[K\033[F\033[K", end="")
        print("  - Saving graphs...")
        progress_bar = ProgressBar(ending_character="", preceding_text="   ", max_amount=total_tier2)
        for tier1 in graphs:
            # Update text as flavour
            print("\033[F\033[K  - Saving graphs... ({})".format(tier1))
            # Path to the folder
            dir_path = output_path + "specific/" + ("years/" if use_years else "months/") + tier1.replace("/", " or ") + "/"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for tier2 in graphs[tier1]:
                file_name = tier2.replace("/", " or ") + ".html"
                x_list, y_list = graphs[tier1][tier2]
                # Write it
                do_graph_singular(x_list, y_list, tier2, path=dir_path + file_name)
                progress_bar.update()
                total_graphs += 1
    print("\nDone")

    # Now that we've got the specific graphs, time to go to the overview
    if len(overview_graphs) == 0:
        print("")
        sys.exit()

    print("Creating overview graphs...")
    for pattern in overview_graphs:
        graphs, total_tier2, all_dates = collect_graphs(database, pattern, use_years)
        print("\033[K\033[F\033[K", end="")
        print("  - Saving graphs...")
        progress_bar = ProgressBar(ending_character="", preceding_text="   ", max_amount=total_tier2 + (1 if pattern == "regions" else 0))
        for tier1 in graphs:
            # Update text as flavour
            print("\033[F\033[K  - Saving graphs... ({})".format(tier1))
            # Path to the folder
            dir_path = output_path + "overview/" + ("years/" if use_years else "months/") + pattern.replace("/", " or ") + "/"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for tier2 in graphs[tier1]:
                file_name = tier1.replace("/", " or ") + ".html"
                if pattern == "regions":
                    title = "Average price of rice between countries in {}".format(tier1)
                else:
                    title = "Price of {}".format(tier1)
                do_graph (tier1, graphs, dir_path + file_name, title)
                progress_bar.update()
                total_graphs += 1
        if pattern == "regions":
            # Do a seperate, large overview graph
            print("\033[F\033[K  - Saving graphs... (regions overview)")
            dir_path = output_path + "overview/" + ("years/" if use_years else "months/") + pattern.replace("/", " or ") + "/"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            # First, take the average of each region to plot as graph
            file_name = "region_overview.html"
            plt.output_file(dir_path + file_name, mode="inline")
            f = plt.figure(title="Overview of average rice price between regions", x_axis_label = XLABEL, y_axis_label = YLABEL, x_axis_type="datetime", plot_width=800)

            legend_list = []

            for region in graphs:
                region_graphs = {"counter":0, "data":{}}
                for country in graphs[region]:
                    x_list, y_list = graphs[region][country]
                    for i, year in enumerate(x_list):
                        price = y_list[i]
                        # Now we have those, add 'em to the regional average
                        region_graphs["counter"] += 1
                        if year not in region_graphs["data"]:
                            region_graphs["data"][year] = 0
                        region_graphs["data"][year] += price

                # Time to ploottt
                counter = region_graphs["counter"]
                data = region_graphs["data"]
                # Quickly construct list
                x_list = []
                y_list = []
                for year in data:
                    x_list.append(year)
                    # Add average
                    y_list.append(data[year] / counter)

                # Time 2 plot it, bruh
                region_color = REGION_NAME_2_COLOR[region]
                line = f.line(x_list, y_list, line_width=2, color=region_color, muted_color=region_color, muted_alpha=0.2)
                circles = f.circle(x_list, y_list, line_color=region_color, fill_color="white", size=4, muted_line_color=region_color, muted_fill_color="white", muted_alpha=0.2)
                legend_list.append((region, [line, circles]))

            # Create the legend
            legend = bokeh.models.Legend(items=legend_list, location=(0,0), click_policy="mute")

            f.add_layout(legend, 'right')

            # Save the graph
            plt.save(f)
            progress_bar.update()
        print("\nDone")

    print("\nSuccessfully created {} graphs.\n".format(total_graphs))


# Entry point
if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-o", "--output_path", help="The path of the resulting database")
    parser.add_argument("-y", "--years", action="store_true", help="If given, the program creates graphs with only years on it's timescale instead of also months")
    parser.add_argument("-og", "--overview_graphs", help="Specify the overview graphs that should be created as well. Used can be: 'products' (to make a graph comparing all countries which share a certain product over time), 'countries' (to make a graph comparing all products a country produces) and 'regions' (to show how regions differ and how each country in a region compares to each other, based on a general rice price), seperated by commas")
    parser.add_argument("-ov", "--overview_only", action="store_true", help="Skip the normal graph generation, do the overview graphs only (this has only use if overview_graphs have been given)")
    parser.add_argument("-s", "--sort_by", help="Changes the way the specific graphs are sorted (default: 'countries', but can also be 'products')")
    args = parser.parse_args()

    input_path = "/home/tim/git/DAV/foodprices2 unified.csv"
    output_path = "/home/tim/git/DAV/Tim/Ignored/Graphs"
    use_years = False
    overview_graphs = []
    overview_only = False
    sort_by = "countries"
    if args.input_path:
        input_path = args.input_path
    if args.output_path:
        output_path = args.output_path
    if args.years:
        use_years = True
    if args.overview_graphs:
        overview_graphs = args.overview_graphs.split(",")
    if args.overview_only and len(overview_graphs) > 0:
        overview_only = True
    if args.sort_by:
        sort_by = args.sort_by if (args.sort_by == "products" or args.sort_by == "countries") else "countries"

    try:
        main(input_path, output_path, use_years, overview_graphs, overview_only, sort_by)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit()

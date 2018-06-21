# Script to actually compare two things from the database, checking for
#   eventual connections


################# CHANGELOG #################
# v1.0:                                     #
#   + Basic functionality                   #
#############################################
# v2.0:                                     #
#   + Added option to view graphs of the    #
#     groups directly                       #
#   + Added option to save all new graphs   #
#     to a folder                           #
#############################################
# v2.1:                                     #
#   o Changed way legends are handled, to   #
#     increase readability for saved        #
#     graphs (no solution found yet for     #
#     real-time shown graphs)               #
#############################################
# v2.2:                                     #
#   + Added ability to match graphs on a    #
#     more thorough yet slower way          #
#############################################
# v2.3:                                     #
#   o Minor asthetics update                #
#############################################
# v2.4:                                     #
#   - Fixed a bug with the random color     #
#     generation                            #
#############################################
# v2.5:                                     #
#   o Changed the way random colors are     #
#     generated to get more distinct colors #
#############################################
# v3.0:                                     #
#   + Added the possibilities to output     #
#     the specific graphs (obsoleting       #
#     graphs.py)                            #
#   o Changed graph generation from pyplot  #
#     to bokeh                              #
#############################################
# v3.1:                                     #
#   o Minor bug fixes                       #
#   - Removed functionality to output       #
#     specific graphs, as this has been     #
#     moved back to graphs.py               #
#############################################

import argparse
import pandas as pd
import sys
import os
import time
import math
import bokeh.plotting as plt
import bokeh
import random
import numpy as np
import copy
import colorsys

from TimsStuff.progressBar import ProgressBar
from TimsStuff.progressBar import WaitIndicator

XLABEL = "Time (years)"
YLABEL = "Price (usd)"

# Terminal colors!
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
        self.generate_rgb_list()

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




# Handy class to divide things in similarity groups
class GroupTracker ():

    # A glorified list, if you like
    class Group ():
        # INit
        def __init__(self, initial_entry, initial_entry_label, margin, deep):
            self.group = {initial_entry_label:initial_entry}
            self.spokesperson = initial_entry
            self.spokesperson_score = 1
            self.margin = margin
            self.deep = deep

        # Handler for len(Group())
        def __len__(self):
            return len(self.group)


        # Update the spokesperson based on people in the group
        #   Wat is the spokesperson, you ask? It is simply an entry that is
        #   'most' representative (has the most matches to other elements)
        # NOTE: if this is not accurate enough, try comparing to each member
        #       everytime there has to be compared.
        def update_spokesperson (self):
            new_spokesperson = self.spokesperson
            new_spokesperson_score = self.spokesperson_score
            for label in self.group:
                person = self.group[label]
                total_matches = 0
                for label2 in self.group:
                    to_test = self.group[label2]
                    if cosine_similarity(person, to_test) >= self.margin:
                        total_matches += 1
                if total_matches > new_spokesperson_score:
                    new_spokesperson = person
                    new_spokesperson_score = total_matches
            self.spokesperson = new_spokesperson
            self.spokesperson_score = new_spokesperson_score

        # Add a person to the group
        def add (self, element, element_label):
            self.group[element_label] = element
            # We have added it, check to see if we should appoint a new spokesperson
            if not self.deep:
                self.update_spokesperson()

        # Compare if a person would fit in this group
        def is_match (self, element):
            if not self.deep:
                return cosine_similarity(element, self.spokesperson) >= self.margin

            # Aha! Time for some deep matching
            is_match = True
            for label in self.group:
                person = self.group[label]
                if cosine_similarity(element, person) < self.margin:
                    is_match = False
                    break
            return is_match

        # Return the inner list, but replace each element with it's label
        def return_group (self):
            to_return = []
            for person in self.group:
                to_return.append((person, self.group[person]))
            return to_return

    # INit
    def __init__(self, margin=0.8, deep=False):
        self.margin = margin
        self.deep = deep

        # Create groups
        self.groups = []

    # Add element to the group, based in it's similarity to others.
    #   element_label is the label the element will get once returned.
    def add (self, element, element_label):
        # Time to start checking in which group it belongs
        for group in self.groups:
            if group.is_match(element):
                # It is, let's add
                group.add(element, element_label)
                return
        # We haven't added, create new group
        self.groups.append(self.Group(element, element_label, self.margin, self.deep))

    # Return all groups, but replace each element with it's label first
    def return_groups (self):
        to_return = []
        for group in self.groups:
            to_return.append(group.return_group())
        return to_return

# Resizes a string by add spaces in the precedings
def fix_length (text, size):
    while len(text) < size:
        text = " " + text
    return text

# Calculate the cosine similarity
def cosine_similarity(v1,v2):
    # compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

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
    return (pre_list1 + [element] + aft_list1, pre_list2 + [0] + aft_list2)

# Function to return a string, only so that it is breaked off with a certain
#   indentation
def break_off (text, first_indentation="", indentation=""):
    if first_indentation == "":
        first_indentation = indentation
    words = text.split()
    line = first_indentation
    end_text = ""
    # Get screen width
    _, screen_width = os.popen('stty size', 'r').read().split()
    screen_width = int(screen_width)
    while len(words) > 0:
        word = words[0]
        words = words[1:]
        if len(indentation + word) > screen_width:
            # Create two new words, and try again
            end_text += line[:-1] + "\n"
            line = indentation
            words = [word[:screen_width - len(indentation)]] + [word[screen_width - len(indentation):]] + words
        elif len(line + word) > screen_width:
            end_text += line[:-1] + "\n"
            line = indentation
            words = [word] + words
        else:
            # We good to go
            line += word + " "
    # Add remaining line
    end_text += line
    return end_text

# Saves or shows a graph
def do_graph (group_name, grouped, all_years, mode, path=""):
    # User wants to see an overview
    plt.output_file(path, mode="inline")
    f = plt.figure(title="Price of {}".format(group_name), x_axis_label=XLABEL, y_axis_label=YLABEL)
    j = 1
    line_stylist = LineStylist()
    for group in grouped[group_name]:
        k = 0
        color = line_stylist.get_random_rgb()
        for label, data in group:
            plot_label = label + " (group {})".format(j)
            line_stylist.style(f, all_years, data, plot_label, color=color)
            k += 1
        line_stylist.reset()
        j += 1

    # We're done, show
    if mode == "show":
        # Show the graph
        plt.show(f)
    elif mode == "save":
        # Save the graph instead
        plt.save(f)

def do_graph_singular (x_list, y_list, title, path=""):
    # Save the graph
    plt.output_file(path, mode="inline")
    f = plt.figure(title=title, x_axis_label = XLABEL, y_axis_label = YLABEL)
    line_stylist = LineStylist()
    line_stylist.style(f, x_list, y_list, title, legend=False)
    plt.save(f)

# Function to return a list of graphs:
#   {"sort_1":{"sort_2":[[1,2],[3,4]]}}
#   <       First sorted              >
#             <     Second sorted    >
#                      <   Graphs   >
#                        <GRF> <GRF>
def collect_graphs (db, mode):
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
        else:
            print("Pattern {} is unknown, skipping...".format(mode))
            return False

        # Now create
        if first_order not in data_list:
            data_list[first_order] = {}
        if secnd_order not in data_list[first_order]:
            data_list[first_order][secnd_order] = {}
            total_things += 1
        if "unit" not in data_list[first_order][secnd_order]:
            data_list[first_order][secnd_order]["unit"] = row.standardized_units
        if row.year not in data_list[first_order][secnd_order]:
            data_list[first_order][secnd_order][row.year] = (0, 0)

        counter, total = data_list[first_order][secnd_order][row.year]
        data_list[first_order][secnd_order][row.year] = (counter + 1, total + row.standardized_prices)
        progress_bar.update()

    print("\033[K\033[F\033[K", end="")

    # Now that we have a data_list, convert it into a graph list
    print("  - Constructing graph data...")
    progress_bar = ProgressBar(ending_character="", max_amount=total_things, preceding_text="   ")
    all_years = []
    for first_order in data_list:
        for secnd_order in data_list[first_order]:
            x_list = []
            y_list = []
            for year in data_list[first_order][secnd_order]:
                if year != "unit":
                    x_list.append(year)
                    counter, total = data_list[first_order][secnd_order][year]
                    y_list.append(total / counter)
                    if year not in all_years:
                        all_years.append(year)
            # Sort
            x_list, y_list = (list(t) for t in zip(*sorted(zip(x_list, y_list))))
            data_list[first_order][secnd_order] = (x_list, y_list)
            progress_bar.update()
    all_years = sorted(all_years)

    print("\033[K\033[F\033[K", end="")

    # Now make all the graphs the same size, to avoid confusion
    print("  - Fixating graph length...")
    progress_bar = ProgressBar(ending_character="", max_amount=total_things, preceding_text="   ")
    for first_order in data_list:
        for secnd_order in data_list[first_order]:
            x_list, y_list = data_list[first_order][secnd_order]
            for year in all_years:
                if year not in x_list:
                    x_list, y_list = insert_sorted(year, x_list, y_list)
            data_list[first_order][secnd_order] = (x_list, y_list)
            progress_bar.update()
    return (data_list, total_things, all_years)

# Main function
def main(input_path, output_path, analyser_patterns, use_years, margin, deep, generate_specifics):
    # Welcome message
    print("\n{}##############".format(bcolors.BOLD))
    print("## ANALYSER ##")
    print("##   v3.1   ##")
    print("##############{}\n".format(bcolors.ENDC))

    wait_indicator = WaitIndicator(WaitIndicator.SpinAnimation, automatic=True, preceding_text="Reading database... ", end_text="Reading database... Done", refresh_rate=0.2)
    wait_indicator.start()
    database = pd.read_csv(input_path)
    wait_indicator.stop()

    for i, pattern in enumerate(analyser_patterns):
        # Time 2 analyse dat products
        print("Analysing {}...".format(pattern))
        graphs, tier2_length, all_years = collect_graphs(database, pattern)
        if graphs == False:
            # Skip
            continue

        if generate_specifics:
            if os.path.exists(output_path + "specific_enhanced/"):
                print("A folder highly likely to contain specifics already exists ({}). Overwrite? (y/n)".format(output_path + "specific_enhanced/"))
                yn = input().lower()
                if yn == "y" or yn == "yes":
                    # ...but before we continue, generate all normal graphs first
                    print("\033[K\033[F\033[K", end="")
                    print("  - Generating specific graphs, sorted by {}...".format(pattern))
                    progress_bar = ProgressBar(ending_character="", max_amount=tier2_length, preceding_text = "   ")
                    # Folder path
                    for tier1 in graphs:
                        print("\033[F  - Generating specific graphs, sorted by {}...".format(pattern))
                        dir_path = output_path + "specific_enhanced/" + pattern + "/" + tier1.replace("/", " or ") + "/"
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)
                        for tier2 in graphs[tier1]:
                            x_list, y_list = graphs[tier1][tier2]
                            filename = tier2.replace("/", " or ") + ".html"
                            do_graph_singular(x_list, y_list, "Price of {}".format(tier2), path=dir_path + filename)
                            progress_bar.update()
                    generate_specifics = False

        # Time to start grouping graphs based on similarity
        print("\033[K\033[F\033[K", end="")
        print("  - Grouping graphs based on similarity...")
        progress_bar = ProgressBar(ending_character="", max_amount=tier2_length, preceding_text="   ")
        grouped = {}
        for tier1 in graphs:
            # Now the trick is to compare each and every product in the country
            group_tracker = GroupTracker(margin=margin, deep=deep)
            for tier2 in graphs[tier1]:
                x_list, y_list = graphs[tier1][tier2]
                group_tracker.add(y_list, tier2)
                progress_bar.update()
            grouped[tier1] = group_tracker.return_groups()

        # Save the graphs if we have to
        if len(output_path) > 0:
            print("\033[K\033[F\033[K", end="")
            print("  - Saving graphs...")
            progress_bar = ProgressBar(ending_character="", max_amount=len(grouped), preceding_text="   ")
            for tier1 in grouped:
                print("\033[F\033[K  - Saving graphs... ({})\n".format(tier1), end="")
                dir_path = output_path + "overview_enhanced/" + pattern + "/"
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                file_name = tier1.replace("/", " or ") + ".html"
                do_graph (tier1, grouped, all_years, "save", path=dir_path + file_name)
                progress_bar.update()

        print("\nDone")

        # We have groups, return them
        _, screen_width = os.popen('stty size', 'r').read().split()
        screen_width = int(screen_width)
        print("\n" + ("#" * int((screen_width - 10) / 2)) + " RESULT " + ("#" * int((screen_width - 10) / 2)))
        print("Each country in which a product has appeared has been grouped as follows:")
        for tier1 in grouped:
            print("{}:".format(tier1))
            num_size = len(str(len(grouped)))
            num = 1
            for group in grouped[tier1]:
                j = 0
                to_print = ""
                for element_label, _ in group:
                    if j > 0 and j < len(group) - 1:
                        to_print += ", "
                    elif j == len(group) - 1 and len(group) > 1:
                        to_print += " and "
                    to_print += element_label
                    j += 1
                print(break_off(to_print, first_indentation="   " + fix_length(str(num), num_size) + ") ", indentation= "    " + " " * (num_size - len(str(num))) + "  "))
                num += 1
        print("#" * screen_width + "\n")

        # Let the user see sum graphs
        print("Type the name of one of the {} to see their graph".format(pattern))
        subtext = "(or leave empty to "
        if i < len(analyser_patterns) - 1:
            subtext += "continue to the next pattern)"
        else:
            subtext += "complete the script)"
        print(subtext)
        group_name = input()
        while group_name != "":
            if group_name in grouped:
                # Show the graph
                do_graph (group_name, grouped, all_years, "show")
                print("Enter another group to see:")
                print(subtext)
            else:
                print("That group isn't present, please enter another:")
                print(subtext)
            group_name = input()
        if i == len(analyser_patterns) - 1:
            print("\n{}Done.{}\n".format(bcolors.OKGREEN, bcolors.ENDC))

if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--std_path", action="store_true", help="Returns the standard input path, and quits the program afterwards.")
    parser.add_argument("--analyser_pattern", action="store_true", help="Returns the possible analyser_pattern strings and their description.")
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-o", "--output_path", help="If given, specifies the path to which all graphs will be saved. If absent, graphs will not be saved.")
    parser.add_argument("-p", "--use_pattern", help="Strings to give the pattern to direct the analyser. Use --analyser_patterns to see them. Seperate by commas, invalid entries will be ignored.")
    parser.add_argument("-y", "--years", action="store_true", help="If this flag is present, the program will use an average of available months in a year to use years as a timescale instead of months.")
    parser.add_argument("-m", "--margin", type=float, help="The margin of which two graphs have to be similar to be grouped")
    parser.add_argument("-d", "--deep", action="store_true", help="If given, the script will use a much thorougher but slower method of checking if a graph is part of a group")
    parser.add_argument("-s", "--generate_specifics", action="store_true", help="If given, the script will also write each specific graph it creates")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/Ignored/foodprices2 unified better.csv"
    output_path = ""
    analyser_pattern = []
    use_years = False
    margin = 0.8
    deep = False
    generate_specifics = False
    if args.std_path:
        print("Standard input path: '{}'".format(input_path))
        sys.exit()
    if args.analyser_pattern:
        print("Analyser patterns currently available:")
        print(" - 'products': Analyse the price of a product in all countries is is sold in.")
        print(" - 'countries': Analyse the price of products within a country.")
        sys.exit()
    if args.input_path:
        input_path = args.input_path
    if args.output_path:
        output_path = args.output_path
    if args.use_pattern:
        analyser_pattern = args.use_pattern.split(",")
    if args.years:
        use_years = True
    if args.margin:
        margin = args.margin
    if args.deep:
        deep = True
    if args.generate_specifics:
        generate_specifics = True

    # Make sure output_path is concluded by '/'
    if len(output_path) > 0 and output_path[-1] != "/":
        output_path += "/"

    # Run main() with KeyboardInterrupt catch
    try:
        main(input_path, output_path, analyser_pattern, use_years, margin, deep, generate_specifics)
    except KeyboardInterrupt:
        print("\n\033[K{}Interrupted by user{}".format(bcolors.OKBLUE, bcolors.ENDC))
        sys.exit()

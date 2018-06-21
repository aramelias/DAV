import pandas as pd
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

# read data
data = pd.read_csv("Data/foodprices2.csv")

# calculate mean for each country
def calcmeans(data):

    means = []
    i = 1
    row = 0
    total = 0
    prevcountry = 0

    for country in data["country_id"]:

        # if value belongs to same country, add corresponding price
        if country == prevcountry:
            i += 1
            total += data["price_usd"][row]

        # if country is finished, calculate mean
        else:
            mean = total / i

            # check if mean is really a numerical value (float)
            if not math.isnan(mean):

                # create tuple that binds country and mean
                means.append((country, mean))

            # reset for next country
            i = 1
            total = 0
        
        # move to next row    
        prevcountry = country
        row += 1

    # return means except first (doesn't belong to any country)
    return(means[1:])

# plot results in a normal and zoomed box plot
def plot(results):

    # create arrays with only means
    means = []
    zoomed = []

    for tup in results:

        # regular boxplot
        means.append(tup[1])

        # zoomed boxplot (with cap of 6)
        if tup[1] < 6:
            zoomed.append(tup[1])

    # sort arrays
    means = sorted(means, key=float)
    zoomed = sorted(zoomed, key=float)

    # create regular box plot
    fig = plt.figure(1, figsize = (6, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(means)
    fig.savefig("plot.png", bbox_inches = "tight")

    # create zoomed box plot
    fig = plt.figure(2, figsize = (6, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(zoomed)
    fig.savefig("zoom.png", bbox_inches = "tight")

# call main function
plot(calcmeans(data))

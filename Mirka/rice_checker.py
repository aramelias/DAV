import pandas as pd
import numpy as np
import itertools
import time
import sys

data = pd.read_csv("../../foodprices2 unified better.csv")

rice_data = data["product_name"].str.contains("Rice")

all_rice_data = data[rice_data]

rice_grouped_country = all_rice_data["product_name"].groupby(all_rice_data["country_name"])

grouped_country_and_product = all_rice_data.groupby(["country_name", "product_name"])
means = grouped_country_and_product["standardized_prices"].mean()
different_sorts = 0
x = 0
prices_all_countries = []

for country, empty in rice_grouped_country:
    price_country = []
    for rice in rice_grouped_country.unique()[country]:
        price_country.append([means[x], rice])
        x += 1
    prices_all_countries.append([country, price_country])

for group in prices_all_countries:
    prices_list = []
    if len(group[1]) > 1:
        prices = group[1]
        for price in prices:
            new_price = price[0]
            prices_list.append(new_price)
    prices_list.sort()
    if prices_list != []:
        difference_f_l = prices_list[len(prices_list)-1] - prices_list[0]
        if difference_f_l > 0.5:
            print("current country:", group[0])
            print("list of prices:", prices_list)
            print("difference between the first and the last element:")
            print(difference_f_l)
            print("difference between every next element in the list:")
            print(np.diff(prices_list))
            print("----------------------------------------------------")

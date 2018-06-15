import pandas as pd


data = pd.read_csv("../foodprices2 unified better.csv")

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


print(prices_all_countries)






"""
print(grouped_country.describe())

for country in all_rice_data["country_name"].unique():
    new_data = all_rice_data[all_rice_data["country_name"] == country]
    print(country)
    print(new_data["product_name"].value_counts())
print(len(all_rice_data["country_name"].unique()))
"""

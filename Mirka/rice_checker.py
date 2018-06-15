import pandas as pd


data = pd.read_csv("../foodprices2 unified better.csv")

rice_data = data["product_name"].str.contains("Rice")

all_rice_data = data[rice_data]

rice_grouped_country = all_rice_data["product_name"].groupby(all_rice_data["country_name"])

for country, x in rice_grouped_country:
    print(country)
    print(len(rice_grouped_country.unique()[country]))

grouped_country_and_product = all_rice_data.groupby(["country_name", "product_name"])
means = grouped_country_and_product["standardized_prices"].mean()




"""
print(grouped_country.describe())

for country in all_rice_data["country_name"].unique():
    new_data = all_rice_data[all_rice_data["country_name"] == country]
    print(country)
    print(new_data["product_name"].value_counts())
print(len(all_rice_data["country_name"].unique()))
"""

from bokeh.plotting import figure
from bokeh.io import output_file, show
import pandas as pd

data_food = pd.read_csv("../../foodprices2 unified better.csv")
data_BMI = pd.read_csv("../BMI-Data-Less.csv")

rice_data_food = data_food["product_name"].str.contains("Rice")


all_rice_data_food = data_food[rice_data_food]


years = list(set(all_rice_data_food["year"].unique()))
years.pop()


for year in years:
    year_rice_data_food = all_rice_data_food[all_rice_data_food["year"] == year]

    output_file_list = ["BMI_vs_Price_", str(year)]
    output = "".join(output_file_list)

    BMI_search = [str(year), " – Both sexes"]
    year_data_BMI = data_BMI[["Country", "".join(BMI_search)]]

    country_list_BMI = year_data_BMI["Country"].unique().tolist()
    country_list_food = year_rice_data_food["country_name"].unique().tolist()
    for country_BMI in country_list_BMI:
        if country_BMI not in country_list_food:
            year_data_BMI = year_data_BMI[year_data_BMI["Country"] != country_BMI]
    for country_food in country_list_food:
        if country_food not in country_list_BMI:
            year_rice_data_food = year_rice_data_food[year_rice_data_food["country_name"] != country_food]

    year_rice_data_food = year_rice_data_food.groupby("country_name")
    year_rice_data_food = year_rice_data_food["standardized_prices"].mean()

    print(year_rice_data_food)
    print(year_data_BMI)

    #scatterplotter_BMI_Price(year_rice_data_food, year_BMI_data_food, output)



def scatterplotter_BMI_Price(X_axis, Y_axis, output, Sizes=None, colors=None):
    ouptu_file(output)

    f = figure(plot_width = 1000, plot_height=650)

    f.title.text = output
    f.title.text_font_size="25px"
    f.title.align="center"

    f.xaxis.axis_label="Petal Length"
    f.yaxis.axis_label="Petal Width"

    f.circle(x=X_axis, y=Y_axis, size=sizes,
         fill_alpha=0.2, color=colors)





"""
rice_grouped_country = all_rice_data_food["product_name"].groupby(all_rice_data_food["country_name"])

grouped_country_and_product = all_rice_data_food.groupby(["country_name", "product_name"])
#print(grouped_country_and_product.describe())
means = grouped_country_and_product["standardized_prices"].mean()
#print(rice_grouped_country.unique())
different_sorts = 0
x = 0
prices_all_countries = []

for country, empty in rice_grouped_country:
    price_country = []
    for rice in rice_grouped_country.unique()[country]:
        price_country.append([means[x], rice])
        x += 1
    prices_all_countries.append([country, price_country])

"""

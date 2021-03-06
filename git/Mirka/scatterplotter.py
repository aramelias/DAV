from bokeh.io import output_file, show, export_png
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label, DataRange1d, HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool, SaveTool, Legend
import pandas as pd


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
COUNTRY_2_REGION = {
    "Afghanistan":1, "Algeria":1, "Sudan":1, "Egypt":1, "Niger":1, "Chad":1,
    "Iran  (Islamic Republic of)":2, "Iraq":2, "Jordan":2, "Lebanon":2, "Pakistan":2, "Syrian Arab Republic":2, "Turkey":2, "Yemen":2, "State of Palestine":2,
    "Armenia":3, "Azerbaijan":3, "Georgia":3, "Kyrgyzstan":3, "Tajikistan":3, "Ukraine":3,
    "Bangladesh":4, "Bhutan":4, "India":4, "Nepal":4,
    "Benin":5, "Burkina Faso":5, "Cote d'Ivoire":5, "Gambia":5, "Ghana":5, "Guinea-Bissau":5, "Guinea":5, "Liberia":5, "Mali":5, "Mauritania":5, "Nigeria":5, "Senegal":5,
    "Bolivia":6, "Colombia":6, "Peru":6,
    "Burundi":7, "Central African Republic":7, "Congo":7, "Democratic Republic of the Congo":7, "Rwanda":7, "Uganda":7, "United Republic of Tanzania":7, "South Sudan":7,
    "Cambodia":8, "Myanmar":8, "Indonesia":8, "Lao People's Democratic Republic":8, "Timor-Leste":8,
    "Costa Rica":9, "El Salvador":9, "Guatemala":9, "Honduras":9, "Panama":9,
    "Djibouti":10, "Ethiopia":10, "Kenya":10, "Somalia":10,
    "Lesotho":11, "Malawi":11, "Mozambique":11, "Swaziland":11, "Zambia":11, "Zimbabwe":11,
    "Cameroon":12, "Cape Verde":12, "Haiti":12, "Madagascar":12, "Philippines":12, "Sri Lanka":12
}
REGION_ID_2_NAME = {
    1: "Noord-Afrika", 2: "Arabische Wereld", 3: "Voormalig Sovjet Gebied", 4: "Zuid Azie", 5: "West Afrika", 6: "Zuid Amerika", 7: "Midden Afrika", 8: "Zuid Oost Azie", 9: "Midden Amerika", 10: "Oost Afrika", 11: "Zuidelijk Afrika", 12:"Eilanden"
}
REGION_ID_2_COLOR = {
    1: "yellow",
    2: "orange",
    3: "darkmagenta",
    4: "green",
    5: "violet",
    6: "cyan",
    7: "greenyellow",
    8: "dimgray",
    9: "limegreen",
    10: "deeppink",
    11: "red",
    12: "aqua"
}


data_food = pd.read_csv("../../../foodprices2 unified better.csv")
data_BMI = pd.read_csv("../BMI-Data-Less.csv")

rice_data_food = data_food["product_name"].str.contains("Rice")


all_rice_data_food = data_food[rice_data_food]


years = list(set(all_rice_data_food["year"].unique()))
years.pop()


for year in years:
    year_rice_data_food = all_rice_data_food[all_rice_data_food["year"] == year]

    output_file_list = ["BMI_vs_Price_", str(year)]
    output = "".join(output_file_list)

    BMI_search = [str(year), " - Both sexes"]
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


    regions = [COUNTRY_2_REGION[y] for y in year_rice_data_food.index.tolist()]
    color_list = [REGION_ID_2_COLOR[x] for x in regions]

    region_names = [REGION_ID_2_NAME[z] for z in regions]


    output_file("".join([output, ".html"]))

    rice_data_list = []
    for element in year_rice_data_food:
        rice_data_list.append(element)

    BMI_data_list = []
    for element in year_data_BMI["".join(BMI_search)]:
        BMI_data_list.append(element)

    new_country_list = year_data_BMI["Country"].unique().tolist()

    print(new_country_list)
    print("_______________________________________________")

    source = ColumnDataSource(data=dict(x=rice_data_list, y=BMI_data_list, countries=new_country_list, color=color_list, region=region_names))

    hover = HoverTool(tooltips=[("Country", "@countries"), ("Region", "@region")])
    tools = [hover, WheelZoomTool(), PanTool(), BoxZoomTool(), ResetTool(), SaveTool()]

    f = figure(tools=tools, plot_width = 1000, plot_height=650)



    f.title.text = output
    f.title.text_font_size="25px"
    f.title.align="center"

    f.yaxis[0].axis_label="BMI"
    f.xaxis[0].axis_label="Prices per KG rice"

    f.x_range=DataRange1d(start=0, end=3.5)

    f.scatter(x="x", y="y", size = 8, color="color", source=source, legend="region")


    save(f)

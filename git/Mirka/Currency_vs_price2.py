from bokeh.io import output_file, show, export_png
from bokeh.layouts import row, widgetbox
from bokeh.plotting import figure, show, output_file, save
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label, DataRange1d, HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool, SaveTool
from bokeh.models import CustomJS, Slider, ColumnDataSource, Range1d, LabelSet, Label, DataRange1d, HoverTool, WheelZoomTool, PanTool, BoxZoomTool, ResetTool, TapTool, SaveTool
import pandas as pd

def reading_databases():
    print("reading databases")
    data_food = pd.read_csv("../../../foodprices2 unified better.csv")
    data_currency = pd.read_csv("newcurrency2.csv")
    return data_food, data_currency

def filtering_currencies(data1, data2):
    print("filtering out currencies")
    currencies_list1 = data1["cur_name"].unique().tolist()
    currencies_list2 = data2["cur_name"].unique().tolist()

    for cur_list1 in currencies_list1:
        if cur_list1 not in currencies_list2:
            data1 = data1[data1["cur_name"] != cur_list1]
    for cur_list2 in currencies_list2:
        if cur_list2 not in currencies_list1:
            data2 = data2[data2["cur_name"] != cur_list2]

    return data1, data2

def normalisation_gathering_currencies(currency_data):
    print("gathering normalisation data")
    dict_cur = {}
    for cur in currency_data["cur_name"].unique().tolist():
        currency = currency_data[currency_data["cur_name"] == cur]

        cur_list = currency.values[0][9:]
        cur_list = list(filter(lambda a: str(a) != "nan", cur_list))
        dict_cur[cur] = [max(cur_list), min(cur_list)]
    return(dict_cur)

def normalisation_gathering_food(food_data):
    print("gathering normalisation data")
    years = list(set(food_data["year"].unique()))
    months = list(set(food_data["month"].unique()))

    dict_food = {}
    for cur in data_food["cur_name"].unique().tolist():
        food_by_cur = food_data[food_data["cur_name"] == cur]
        list1 = []
        for year in years:
            food_by_cur_year = food_by_cur[food_by_cur["year"] == year]
            for month in months:
                food_by_cur_month = food_by_cur_year[food_by_cur_year["month"] == month]
                food_by_cur_month_group = food_by_cur_month.groupby("cur_name")
                placeholder = food_by_cur_month_group["standardized_prices"].mean().values
                if len(placeholder) > 0:
                    list1.append(placeholder[0])
        dict_food[cur] = [max(list1), min(list1)]

    return dict_food

def normalise(data_list, min_max_dict, key):
    output_list = []
    minimum = min_max_dict[key][1]
    maximum = min_max_dict[key][0]
    for element in data_list:
        if str(element) == "nan":
            output_list.append("nan")
        elif maximum - minimum == 0:
            output_list.append(1)
        else:
            element = (element - minimum) / (maximum - minimum)
            output_list.append(element)
    return output_list


def graph_plotter(ylist1, ylist2, xlist3, name):
    print("plotting graph: ", name)
    output_file("".join(["currency2:_", name,".html"]))
    source1 = ColumnDataSource(data=dict(x=xlist3, y=ylist1))
    source2 = ColumnDataSource(data=dict(x=xlist3, y=ylist2))

    f = figure(plot_width = 1000, plot_height=650)

    f.title.text = name
    f.title.text_font_size="25px"
    f.title.align="center"

    f.yaxis[0].axis_label="Normalized prices and exchange rate"
    f.xaxis[0].axis_label="year and month"

    f.line(x="x", y="y", line_width=2, color = "red", legend= "Exchange rate", source=source1)
    f.line(x="x", y="y", line_width=2, color = "Blue", legend= "Product prices", source=source2)
    f.legend.location = "bottom_right"


    save(f)



def creating_graphs(data_food, data_currency, normal_cur_dict, normal_food_dict):
    years = [1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
    months = [1,2,3,4,5,6,7,8,9,10,11,12]

    for cur in data_food["cur_name"].unique().tolist():
        data_of_currency = data_currency[data_currency["cur_name"] == cur]
        data_of_food = data_food[data_food["cur_name"] == cur]
        data_food_all = []
        data_years_all = []
        for year in years:
            data_of_food_year = data_of_food[data_of_food["year"] == year]
            for month in months:
                data_of_food_month = data_of_food_year[data_of_food_year["month"] == month]
                data_of_food_month = data_of_food_month[["cur_name", "standardized_prices"]]
                data_of_food_month = data_of_food_month.groupby("cur_name")
                placeholder = data_of_food_month["standardized_prices"].mean().values
                if len(placeholder) > 0:
                    data_food_all.append(placeholder[0])
                else:
                    data_food_all.append("nan")
                if month < 10:
                    data_years_all.append(int("".join([str(year), "0", str(month)])))
                else:
                    data_years_all.append(int("".join([str(year), str(month)])))

        data_currency_all = data_of_currency.values[0][9:312+9]

        data_currency_all = normalise(data_currency_all, normal_cur_dict, cur)
        data_food_all = normalise(data_food_all, normal_food_dict, cur)

        i = 0
        while i < len(data_currency_all):
            if str(data_currency_all[i]) == "nan":
                data_currency_all.pop(i)
                data_food_all.pop(i)
                data_years_all.pop(i)
                i -= 1
            i += 1

        i = 0
        while i < len(data_food_all):
            if str(data_food_all[i]) == "nan":
                data_currency_all.pop(i)
                data_food_all.pop(i)
                data_years_all.pop(i)
                i -= 1
            i += 1

        name = "".join([cur, "_development2"])

        graph_plotter(data_currency_all, data_food_all, data_years_all, name)











if __name__ == "__main__":
    data_food, data_currency = reading_databases()
    data_food = data_food[data_food["product_name"].str.contains("Rice")]
    data_food, data_currency = filtering_currencies(data_food, data_currency)
    normal_cur_dict = normalisation_gathering_currencies(data_currency)
    normal_food_dict = normalisation_gathering_food(data_food)
    creating_graphs(data_food, data_currency, normal_cur_dict, normal_food_dict)

import pandas as pd

data = pd.read_csv("../foodprices2 unified.csv")

def get_empty(database):
    list_empty = []
    rows = len(database.index)
    for column in database:
        x = 0
        while x < rows:
            placeholder = database[column].loc[x]
            if str(placeholder) == "nan":
                list_empty.append([[x, column]])
            x += 1
    return list_empty

empty_cells = get_empty(data)

with open("empty_columns.txt", "w" ) as f:
    for datapoint in empty_cells:
        f.write(str(datapoint)+"\n")

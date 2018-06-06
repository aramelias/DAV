import pandas as pd

data = pd.read_csv("WFPVAM_FoodPrices_05-12-2017.csv")

def get_misspelled(datas):
    listwrong = []
    for column in datas:
        print(datas[column].dtype)
        if datas[column].dtype == "object":
            x = 0
            while x < 783788:
                placeholder = datas[column].loc[x]
                if str(placeholder) == "nan":
                    placeholder = "Not-specified"
                new = list(placeholder)
                if x > 0:
                    y = check_same(new, last)
                    if y == 0:
                        listwrong.append([x, column])
                last = new
                x += 1
    return(listwrong)



def check_same(newest, latest):
    if newest != latest:
        length = 0
        if len(newest) > len(latest):
            length = len(latest)
        else:
            length = len(newest)
        dissimilarity = 0
        z = 0
        while z < length:
            if newest[z] != latest[z]:
                dissimilarity += 1
            z += 1
        if dissimilarity == 1:
            return 0
        else:
            return 1


get_misspelled(data)

import pandas as pd

data = pd.read_csv("WFPVAM_FoodPrices_05-12-2017.csv")


"""
Check if for all the rows if two words are supposed to be the same if they
are they same
"""
def get_misspelled(datas):
    listwrong = []
    for column in datas:
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
                        listwrong.append([x, column, "".join(new), "".join(last)])
                last = new
                x += 1
    return listwrong


"""
check for two lists if they differ by one element
"""
def check_same(list1, list2):
    if list1 != list2:
        l_list1 = len(list1)
        l_list2 = len(list2)
        if l_list1 != l_list2:
            return 1
        length = l_list1
        if l_list1 > l_list2:
            length = l_list2
        dissimilarity = 0
        z = 0
        while z < length:
            if list1[z] != list2[z]:
                dissimilarity += 1
            z += 1
        if dissimilarity == 1:
            return 0
        else:
            return 1


print(get_misspelled(data))

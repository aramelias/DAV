import pandas as pd
import numpy as np

with open("foodprices.csv") as fIn, open("foodprices2.csv", "w") as fOut:
    foodlist = pd.read_csv("foodprices.csv")
    currencys = pd.read_csv("newcurrency2.csv")
    lines = fIn.readline()
    usd = []
    allCurrencys = []

    for i in range(len(currencys)):
        allCurrencys.append(currencys['cur_name'][i])

    for i in range(len(foodlist)): 
        print(i, ",", (i/len(foodlist))*100, "%")
        if foodlist['cur_name'][i] in allCurrencys:
            currencyrows = (currencys.index[currencys["cur_name"] == foodlist['cur_name'][i]])
            index = int(currencyrows[0])
            datum = "-".join((str(foodlist['mp_year'][i]), str(foodlist['mp_month'][i]).zfill(2)))
            usd_ex = currencys[datum][index]
            new_usd = foodlist['mp_price'][i] / usd_ex
            usd.append(new_usd)
        else:
            usd.append(None)

    foodlist["price_usd"] = usd
    foodlist.to_csv("foodprices2.csv", index=False)

    print("Bestand", fIn.name, "succesvol opgeslagen als", fOut.name)
#rewriter2.py

import pandas as pd

with open("newcurrency.csv") as fIn, open("newcurrency2.csv", "w") as fOut:
    df = pd.read_csv("newcurrency.csv")
    df.drop(df.columns[9:df.columns.get_loc("1992-01")], axis=1, inplace=True)
    df.drop(df.columns[df.columns.get_loc("1791"):], axis=1, inplace=True)
    df.to_csv("newcurrency2.csv", index=False)


print("Bestand", fIn.name, "succesvol opgeslagen als", fOut.name)
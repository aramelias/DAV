#rewrite currency's

import pandas as pd

with open("currency.csv") as fIn, open("newcurrency.csv", "w") as fOut:
    df = pd.read_csv("currency.csv")
    lines = fIn.readlines()
    fOut.write(lines[0])

    for i in range(len(df)):
        if df['FREQ'][i] == "M" and df['COLLECTION'][i] == "A":
            fOut.write(lines[i+1])


print("Bestand", fIn.name, "succesvol opgeslagen als", fOut.name)
# TRY THIS AT HOME:
# Welcome to the test file for Tim! Do here whatever your heart desires.

import pandas as pd

df = pd.DataFrame()
df["Names"] = ["Anne", "Aram", "Mirka", "Tim"]
df["Awesomeness"] = [1, 1, 1, 1]
print(df)
print("----")
print(df["Names"])
print("----")
for elem in df["Names"]:
    print(elem)

# TRY THIS AT HOME:
# Welcome to the test file for Tim! Do here whatever your heart desires.

import pandas as pd
from TimsStuff.progressBar import ProgressBar

df = pd.DataFrame()
df["Names"] = ["Anne", "Aram", "Mirka", "Tim"]
df["Awesomeness"] = [1, 1, 1, 1]
print(df)
print("----")
print(df["Names"])
print("----")
for elem in df["Names"]:
    print(elem)

progress_bar = ProgressBar(30, max_amount=99999)
for i in range(100000):
    progress_bar.set(i)
progress_bar.end()

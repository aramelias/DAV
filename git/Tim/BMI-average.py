
import argparse
import pandas as pd
import sys
import os
import time
import bokeh.plotting as plt
import bokeh.models as bkm
import bokeh.layouts as bkl
import bokeh
import datetime
import random
import numpy as np
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import sklearn.metrics as sm

from TimsStuff.progressBar import ProgressBar

# LOAD DB
print("Reading DB...")
database = pd.read_csv("/Users/Tim/UvA/DAV/git/Ignored/foodprices2 unified better.csv")
database = database.fillna(-1)

REGION_ID_2_NAME = {
    1: 'Noord-Afrika', 2: 'Arabische Wereld', 3: 'Voormalig Sovjet Gebied', 4: 'Zuid Azie', 5: 'West Afrika', 6: 'Zuid Amerika', 7: 'Midden Afrika', 8: 'Zuid Oost Azie', 9: 'Midden Amerika', 10: 'Oost Afrika', 11: 'Zuidelijk Afrika', 12:"Eilanden"
}
COUNTRY_2_REGION = {
    'Algeria':1, 'Sudan':1, 'Egypt':1, 'Niger':1, 'Chad':1,
    'Iran  (Islamic Republic of)':2, 'Iraq':2, 'Jordan':2, 'Lebanon':2, 'Pakistan':2, 'Syrian Arab Republic':2, 'Turkey':2, 'Yemen':2, 'State of Palestine':2, 'Afghanistan':2,
    'Armenia':3, 'Azerbaijan':3, 'Georgia':3, 'Kyrgyzstan':3, 'Tajikistan':3, 'Ukraine':3,
    'Bangladesh':4, 'Bhutan':4, 'India':4, 'Nepal':4,
    'Benin':5, 'Burkina Faso':5, "Cote d'Ivoire":5, 'Gambia':5, 'Ghana':5, 'Guinea-Bissau':5, 'Guinea':5, 'Liberia':5, 'Mali':5, 'Mauritania':5, 'Nigeria':5, 'Senegal':5,
    'Bolivia':6, 'Colombia':6, 'Peru':6,
    'Burundi':7, 'Central African Republic':7, 'Congo':7, 'Democratic Republic of the Congo':7, 'Rwanda':7, 'Uganda':7, 'United Republic of Tanzania':7, 'South Sudan':7,
    'Cambodia':8, 'Myanmar':8, 'Indonesia':8, "Lao People's Democratic Republic":8, 'Timor-Leste':8,
    'Costa Rica':9, 'El Salvador':9, 'Guatemala':9, 'Honduras':9, 'Panama':9,
    'Djibouti':10, 'Ethiopia':10, 'Kenya':10, 'Somalia':10,
    'Lesotho':11, 'Malawi':11, 'Mozambique':11, 'Swaziland':11, 'Zambia':11, 'Zimbabwe':11,
    'Cameroon':12, 'Cape Verde':12, 'Haiti':12, 'Madagascar':12, 'Philippines':12, 'Sri Lanka':12
}

print("Specify the region:")
region = input()

total = {}
counter = {}
progress_bar = ProgressBar(max_amount=len(database))
for row in database.itertuples():
    if "rice" not in row.product_name.lower() or row.year not in [2008, 2010, 2011, 2014] or row.country_name in ["Nigeria"]:
        progress_bar.update()
        continue
    curr_region = REGION_ID_2_NAME[COUNTRY_2_REGION[row.country_name]]
    if curr_region == region:
        if row.year not in total:
            total[row.year] = {}
            counter[row.year] = {}
        if row.country_name not in total[row.year]:
            total[row.year][row.country_name] = 0
            counter[row.year][row.country_name] = 0
        if row.standardized_prices > -1:
            total[row.year][row.country_name] += row.standardized_prices
            counter[row.year][row.country_name] += 1
    progress_bar.update()
for year in total:
    print("{}:".format(year))
    year_total = 0
    year_counter = 0
    for country in total[year]:
        print("  - {}: {}".format(country, total[year][country] / counter[year][country]))
        year_total += total[year][country] / counter[year][country]
        year_counter += 1
    print("Regional average: {}".format(year_total / year_counter))

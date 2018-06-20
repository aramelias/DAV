# TRY THIS AT HOME:
# Welcome to the test file for Tim! Do here whatever your heart desires.

import pandas as pd
import os
import datetime
import bokeh.plotting as plt
import bokeh
from TimsStuff.progressBar import ProgressBar

# Function to return a string, only so that it is breaked off with a certain
#   indentation
def break_off (text, indentation=""):
    words = text.split()
    line = indentation
    end_text = ""
    # Get screen width
    _, screen_width = os.popen('stty size', 'r').read().split()
    screen_width = int(screen_width)
    while len(words) > 0:
        word = words[0]
        words = words[1:]
        if len(indentation + word) > screen_width:
            # Create two new words, and try again
            end_text += line[:-1] + "\n"
            line = indentation
            words = [word[:screen_width - len(indentation)]] + [word[screen_width - len(indentation):]] + words
        elif len(line + word) > screen_width:
            end_text += line[:-1] + "\n"
            line = indentation
            words = [word] + words
        else:
            # We good to go
            line += word + " "
    # Add remaining line
    end_text += line
    return end_text

print(break_off("test" * 25, indentation="    "))

def resize (text, length):
    while len(text) < length:
        text = " " + text
    return text

print("'" + resize("123", 3) + "'")

to_do = """Afghanistan,
Algeria,
Armenia,
Azerbaijan,
Bangladesh,
Benin,
Bhutan,
Bolivia (Plurinational State of),
Burkina Faso,
Burundi,
Cabo Verde,
Cambodia,
Cameroon,
Central African Republic,
Chad,
Colombia,
Congo,
Costa Rica,
Cote d'Ivoire,
Democratic Republic of the Congo,
Djibouti,
Egypt,
El Salvador,
Ethiopia,
Gambia,
Georgia,
Ghana,
Guatemala,
Guinea,
Guinea-Bissau,
Haiti,
Honduras,
India,
Indonesia,
Iran (Islamic Republic of),
Iraq,
Jordan,
Kenya,
Kyrgyzstan,
Lao People's Democratic Republic,
Lebanon,
Lesotho,
Liberia,
Madagascar,
Malawi,
Mali,
Mauritania,
Mozambique,
Myanmar,
Nepal,
Niger,
Nigeria,
Pakistan,
Panama,
Peru,
Philippines,
Rwanda,
Senegal,
Somalia,
Sri Lanka,
Swaziland,
Syrian Arab Republic,
Tajikistan,
Timor-Leste,
Turkey,
Uganda,
Ukraine,
United Republic of Tanzania,
Yemen,
Zambia,
Zimbabwe"""

for i, word in enumerate(to_do.split("\n")):
    word = word.replace(",", "")
    print("\"{}\":{},".format(word, i))

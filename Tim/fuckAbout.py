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

f = plt.figure()
f.scatter([1, 2, 3], [4, 5, 6], color=[bokeh.colors.RGB(255, 0, 0), bokeh.colors.RGB(0, 255, 0), bokeh.colors.RGB(0, 0, 255)])
plt.show(f)

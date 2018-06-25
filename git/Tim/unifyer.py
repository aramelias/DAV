# This script takes all the units as presented in WFPVAM_FoodPrices_05, and converts
#   them to standardized versions of themselves, updating the prices (e.g. "50 KG"
#   become "KG", and the price is divided by 50)

import argparse
import pandas as pd
import sys
import os
import time

from TimsStuff.progressBar import ProgressBar



# Entry point
if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", help="The path to the to be checked database")
    parser.add_argument("-o", "--output_path", help="The path of the resulting database")
    args = parser.parse_args()

    input_path = "/Users/Tim/UvA/DAV/Anne/foodprices2.csv"
    output_path = "/Users/Tim/UvA/DAV/Ignored/foodprices2 unified better.csv"
    if args.input_path:
        input_path = args.input_path
    if args.output_path:
        output_path = args.output_path


    # Intro message
    print("\n##################")
    print("## UNIT UNIFYER ##")
    print("##     v1.1     ##")
    print("##################\n")

    # Read DB
    print("Reading database...")
    db = pd.read_csv(input_path)
    print("Done")

    # Unit conversion table:
    #   Each unit point to the ground unit, and how much of the ground unit it is
    units = {
        "KG": ("KG", 1),
        "G": ("KG", 0.001),
        "Pound": ("KG", 0.453592),
        "MT": ("KG", 1000),

        "L": ("L", 1),
        "ML": ("L", 0.001),
        "Cubic meter": ("L", 1000),
        "Gallon": ("L", 4.54609),

        "pcs": ("pcs", 1),
        "Dozen": ("pcs", 12),

        "Bunch": ("Bunch", 1),
        "Unit": ("Unit", 1),
        "Sack": ("Sack", 1),
        "Loaf": ("Loaf", 1),
        "Package": ("Package", 1),
        "Packet": ("Packet", 1),

        "kWh": ("kWh", 1),

        "Day": ("Day", 1),
        "Month": ("Day", "?"),

        "USD/LCU": ("USD/LCU", 1),
        "Head": ("Head", 1),
        "Libra": ("Libra", 1),
        "Tubers": ("Tubers", 1),
        "Marmite": ("Marmite", 1),
        "Course": ("Course", 1),
        "Cuartilla": ("Cuartilla", 1)
    }
    # Base unit ID table:
    #   Each unit is refered to it's unique id
    base_unit_ids = {
        "KG": 1,

        "L": 2,

        "pcs": 3,

        "Bunch": 4,
        "Unit": 5,
        "Sack": 6,
        "Loaf": 7,
        "Package": 8,
        "Packet": 9,

        "kWh": 10,

        "Day": 11,

        "USD/LCU": 12,
        "Head": 13,
        "MT": 14,
        "Libra": 15,
        "Tubers": 16,
        "Marmite": 17,
        "Course": 18,
        "Cuartilla": 19
    }
    # Month-day table
    #   Each month number is refered to the number of days in that specific month
    month_days = {
        1:31,
        2:28,
        2.5:29,
        3:31,
        4:30,
        5:31,
        6:30,
        7:31,
        8:31,
        9:30,
        10:31,
        11:30,
        12:31
    }
    # Month-name table
    #   Refers month number to month name, for debugging
    month_names = {
        1:"January",
        2:"February",
        3:"March",
        4:"April",
        5:"May",
        6:"June",
        7:"July",
        8:"August",
        9:"September",
        10:"October",
        11:"November",
        12:"December"
    }

    # For each row, check if there's a unit modyifier (e.g. >10< KG) and if so,
    #   change price column. Prices are in a new column.
    print("Standardizing...")
    new_price_column = []
    new_unit_column = []
    new_unit_id_column = []
    _, screen_width = os.popen('stty size', 'r').read().split()
    progress_bar = ProgressBar(int(screen_width), max_amount=len(db))
    for row in db.itertuples():
        # First clear progress bar
        unit_modyifier = -1
        unit = []
        price = row.price_usd
        for elem in row.unit_name.split():
            try:
                # We have found a unit modyifier
                unit_modyifier = float(elem)
            except ValueError:
                # No, not it
                unit.append(elem)
        unit = ' '.join(unit)

        # Now, convert to the base unit of itself (e.g. G -> KG)
        base_unit, conversion_ratio = units[unit]

        if conversion_ratio == "?":
            # Special action required, convert as needed
            if unit == "Month":
                # Month-to-day conversion
                if row.month == 2 and row.year % 4 == 0:
                    # February, leap year
                    no_of_days = month_days[2.5]
                else:
                    no_of_days = month_days[row.month]
                conversion_ratio = 1 / no_of_days
                print("\033[K",end="\r")
                print("SPECIAL CONVERTION: {} {} -> {} days".format(month_names[row.month], row.year, no_of_days),end="")
                if row.year % 4 == 0:
                    print(" (leap year)")
                else:
                    print("")

        # If there's a modyifier, now's the time to include that in the ratio
        if unit_modyifier != -1:
            # Tweak the conversion ratio to match the unit_modyifier
            conversion_ratio = unit_modyifier * conversion_ratio

        price = price / conversion_ratio
        # Write away in the new columns
        new_unit_column.append(base_unit)
        new_unit_id_column.append(base_unit_ids[base_unit])
        new_price_column.append(price)
        # Update progress_bar
        progress_bar.update()
    print("Done")
    print("Saving new database...")
    db["standardized_units_ids"] = new_unit_id_column
    db["standardized_units"] = new_unit_column
    db["standardized_prices"] = new_price_column
    db.to_csv(output_path)
    print("Done")
    print("\nSuccessfully standardized database\n")

import pandas as pd
import numpy as np
import argparse
import os
import sys


def rating_cal(data):


    five = 0
    four = 0
    three = 0
    two = 0
    one = 0


    for i, k in data.iterrows():

        if int(float(k["Rating"])) == 5:
            five += 1
        elif int(float(k["Rating"])) == 4:
            four += 1
        elif int(float(k["Rating"])) == 3:
            three += 1
        elif int(float(k["Rating"])) == 2:
            two += 1
        elif int(float(k["Rating"])) == 1:
            one += 1
        else:
            pass
    rating_1 = (five * 5) + (four * 4) + (three * 3) + (two * 2) + (one * 1)
    rating_2 = five + four + three + two + one

    rating = round((rating_1 / rating_2),2)

    return rating




# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     required_args = parser.add_argument_group()
#     required_args.add_argument("-i", "--input_file", dest="input_file", required=True)
#     arguments = parser.parse_args()
#     main(arguments.input_file)
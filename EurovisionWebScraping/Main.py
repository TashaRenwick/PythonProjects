import eurovision_functions as f
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

from langdetect import detect, DetectorFactory


years = [str(x) for x in range(1992, 2022)]
base_url = 'https://eurovisionworld.com/eurovision/'

big_df = f.results_df(f.get_soups(years, base_url, 'voting_table'))
big_df['round'] = 'final'

big_df.to_csv("lists.csv")

# big_df = pd.read_csv("lists.csv", index_col=0, header=0)
# big_df = f.add_lyrics(big_df)
# big_df.to_csv("lists.csv")


# DetectorFactory.seed = 0
#
# print(detect("Love, shine a light in every corner of my heart"))

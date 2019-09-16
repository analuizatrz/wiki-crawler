import pandas as pd
from pandas.io.json import json_normalize
import os
import csv


def save_dataframe(df, filename):
    df.to_csv(f"{filename}.csv", index=None, header=True, quoting=csv.QUOTE_NONNUMERIC)


def run_stats(input_folder, df):
    i = len(df)
    for filename in os.listdir(input_folder):
        try:
            data = pd.read_csv(f"{input_folder}/{filename}")
            #revision_count = len(set(data['revision.timestamp'].values))
            revision_count = len(data['revision.timestamp'].values)

            df.loc[i, 'title'] = filename
            df.loc[i, 'distinct_revisions'] = revision_count
            i += 1
            #print(f"{filename}, {revision_count}")
        except:
            print(f"erro {filename}")
    return df


def calc_stats(df):
    return pd.DataFrame(
        [["média", df["distinct_revisions"].mean()],
        ["min", df["distinct_revisions"].min()],
        ["max", df["distinct_revisions"].max()],
        ["std", df["distinct_revisions"].std()]], columns=["métrica", "valor"]
    )

input_file = "stats2.csv"
df = pd.read_csv(input_file)
# df = pd.DataFrame(columns=['title', 'distinct_revisions'])

base_folder = "/home/ana/Documents/tcc-web-crawler"
# input_folder = f"{base_folder}/collected_data/revision_info_200701-200901/data"

# run_stats(input_folder, df)

# input_folder = f"{base_folder}/collected_data/revision_info_200701-200901-errors/data"
# run_stats(input_folder, df)

# save_dataframe(df, f"{base_folder}/stats2")

df_metrics = calc_stats(df)
save_dataframe(df_metrics, f"{base_folder}/stats_metrics")

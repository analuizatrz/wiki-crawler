import os
import csv
import pandas as pd

def join_all(datasets_folder):
    li=[]
    titles = os.listdir(datasets_folder)
    for index, title in enumerate(titles):
        df = pd.read_csv(f"{datasets_folder}/{title}")
        df["title"] = title
        li.append(df)

    return pd.concat(li, axis=0, ignore_index=True)

def df_first_columns(df, columns):
    cols = columns + [col for col in df if col not in columns]
    return df[cols]

base_folder = "/home/ana/Documents/tcc-collected-data/data"
category_folder = f"{base_folder}/info_and_category_200701-200901/data" 

features = pd.read_csv(f"{base_folder}/features/data/raw_dataset.csv", sep=";")
category = join_all(category_folder)
category.columns = ['access', 'category', 'pageid', 'raw_category', 'revision.anon',
       'revision.comment', 'revision.commenthidden', 'revision.parentid',
       'revision.revid', 'timestamp', 'revision.user', 'title']

merged = pd.merge(category, features, how='inner').sort_values(by=['title','timestamp'], ascending=[True, False])

df_first_columns(merged,['title','timestamp']).to_csv(f"features.csv", index=None, header=True, quoting=csv.QUOTE_NONNUMERIC)

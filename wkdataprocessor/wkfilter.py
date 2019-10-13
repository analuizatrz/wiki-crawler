import pandas as pd

def where_not_in(df, column, values):
    for value in values:
        df = df[df[column] != value]
    return df

def split_valid_invalid(df):
    valid_categories = ['A','B','C','FA','GA','Start','Stub']

    invalid = where_not_in(df, 'category', valid_categories)
    valid = df.drop(invalid.index)

    return valid, invalid

if __name__ == "__main__":

    base_folder = "/home/ana/Documents/tcc-web-crawler/data"
    joined_df = pd.read_csv(f"{base_folder}/join_features.csv")
    
    valid, invalid = split_valid_invalid(joined_df)

    invalid.to_csv(f"{base_folder}/join_features-invalid-categories.csv")
    valid.to_csv(f"{base_folder}/join_features-valid-categories.csv")

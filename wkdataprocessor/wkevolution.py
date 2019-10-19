import sys
sys.path.insert(1, "/home/ana/Documents/tcc-web-crawler/wkdatacollector")

from wkio import save_dataframe
import pandas as pd
import csv
import os

import datetime
import dateutil.parser


def parse_date(date):
    """Parse date from ISO 8601 format to datetime
 
    Parameters:
        date (str): date in the format ISO 8601: 2001-01-15T14:56:00Z
        
    Returns:
        date (datetime): date parsed

    """
    return dateutil.parser.parse(date)


def days_between_dates(start, end):
    date =  parse_date(end) - parse_date(start)
    return date.days


def build_row(actual, past, diff_columns, info_columns, date_columns):
    row = {}
    for column in info_columns:
        row[f"past_{column}"] = past[column]
        row[f"actual_{column}"] = actual[column]

    for column in date_columns:
        row[f"past_{column}"] = past[column]
        row[f"actual_{column}"] = actual[column]
        row[f"delta_{column}"] = days_between_dates(past[column], actual[column])

    for column in diff_columns:
        row[f"past_{column}"] = past[column]
        row[f"actual_{column}"] = actual[column]
        row[f"delta_{column}"] = actual[column] - past[column]

    return row

def build_columns(commom_columns, diff_columns, info_columns, date_columns):
    columns = commom_columns
    for column in info_columns:
        columns += [f"past_{column}",f"actual_{column}"]
    for column in date_columns:
        columns += [f"past_{column}",f"actual_{column}",f"delta_{column}"]
    for column in diff_columns:
        columns += [f"past_{column}",f"actual_{column}",f"delta_{column}"]
    return columns

def build_dataset(dataset, diff_columns, info_columns, date_columns):
    commom_columns = ['title', 'pageid']
    columns = build_columns(commom_columns, diff_columns, info_columns, date_columns)
    df = pd.DataFrame(columns=columns)

    row_iterator = revision_dataset.iterrows()
    _, actual = next(row_iterator)

    for i, row in row_iterator:
        if(row['title'] == actual['title']):
            new_row = build_row(actual, row, diff_columns, info_columns, date_columns)
            #print(new_row)
            df.at[i-1,:] = new_row
            df.at[i-1,'title'] = row['title']
            df.at[i-1,'pageid'] = row['pageid']
        actual = row
    return df
   

if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-web-crawler/data"
    output_folder = "/home/ana/Documents/tcc-web-crawler/data"

    filename = f"{base_folder}/5-join_multiple_class_without_C-reduced"

    revision_dataset = pd.read_csv(f"{filename}.csv")

    info_columns = ['access', 'category', 'raw_category', 'revision.anon', 'revision.comment', 'revision.commenthidden', 'revision.parentid', 'revision.revid', 'revision.user']

    feature_columns = ['Section count', 'Subsection count', 'Complete URL link count', 'Complete URL link count per section',
                       'Complete URL link count per length', 'Relative URL link count', 'Relative URL link count per section',
                       'Relative URL link count per length', 'Same page link count', 'Same page link count per section',
                       'Same page link count per length', 'Mean section size', 'Mean subsection size', 'Largest section size',
                       'Shortest section size', 'Standard deviation of the section size', 'Images count', 'Images per length', 'Images per section',
                       'Images per subsection', 'Phrase count', 'Large phrase count', 'Paragraph count', 'Large paragraph count',
                       'Largest phrase size', 'Large phrase rate', 'Short phrase rate', 'Char Count', 'Word Count', 'Articles count',
                       'Auxiliary verbs count', 'Coordination conjunctions count', 'Correlative conjunctions count', 'Indefinite pronouns count',
                       'Interrogative pronouns count', 'Prepositions count', 'Pronouns count', 'Relative pronoums count',
                       'Subordinating conjunctions count', 'To be verbs count', 'Sentences starting with articles',
                       'Sentences starting with auxiliary verbs', 'Sentences starting with coordination conjunctions',
                       'Sentences starting with correlative conjunctions', 'Sentences starting with indefinite pronouns',
                       'Sentences starting with interrogative pronouns', 'Sentences starting with prepositions', 'Sentences starting with pronouns',
                       'Sentences starting with relative pronoums', 'Sentences starting with subordinating conjunctions',
                       'Sentences starting with to be verbs', 'ARI readability feature', 'Coleman-Liau readability feature',
                       'Flesch Reading Ease Readability Feature', 'Flesch Kincaid Readability Feature', 'Gunning Fog Index readability feature',
                       'Lasbarhetsindex readability feature', 'SMOG Grading readability feature'
                    ]

    result = build_dataset(revision_dataset, feature_columns , info_columns, ['timestamp'])
    save_dataframe(result, f"{filename}-evolution.csv")
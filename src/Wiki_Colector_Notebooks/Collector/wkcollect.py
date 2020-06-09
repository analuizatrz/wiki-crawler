from wkrequest import get_revisions_info, get_titles_from_id, get_revision_content, get_page_links
from wkio import create_folder_if_does_not_exist, create_file_if_does_not_exist, read_json, write_json, append_file, write_file, save_dataframe
from wkparse import parse_revision_content, parse_revisions_info_monthly, parse_revision_category_content, parse_page_links
from wkutils import Timer
import time
import csv
import os

from pandas.io.json import json_normalize
import pandas as pd

# TODO: refactor to be a foreach_run
def collect_all(titles, collect_callback, collect_callback_params, output_folder, log):
    file_collected = f"{output_folder}/collected.json"
    file_error = f"{output_folder}/errors.csv"
    folder_data = f"{output_folder}/data"

    status = {}
    try:
        status = read_json(file_collected)
    except IOError:
        status = {"collected_pages": []}

    create_file_if_does_not_exist(file_error)
    create_folder_if_does_not_exist(folder_data)

    already_collected_pages = set(status["collected_pages"])
    remaning_to_collect = [article for article in titles if article not in already_collected_pages]

    objTime = Timer(log)

    clear_limit = 100
    total_printed = 0
    while(len(remaning_to_collect) > 0):
        if(total_printed == clear_limit):
            os.system("clear")
            total_printed = 0
        title = remaning_to_collect.pop(0)
        objTime.log_delta(f"Remaining: {len(remaning_to_collect)+1} collecting now: '{title}'")
        total_printed += 1
        try:
            collect_callback(title, collect_callback_params, folder_data, log)
            status["collected_pages"].append(title)
            write_json(file_collected, status)
        except Exception as e:
            append_file(file_error, title)
            log(f"ERROR:{title} {str(e)}\n")
            #time.sleep(1)
        #time.sleep(1)
    log(f"Tempo total : {objTime.total_time}")


def collect_titles(ids, folder_data, articles_per_request=50, log=print):
    remaining = ids

    while(len(remaining) > 0):
        to_request = remaining[:articles_per_request]
        remaining = remaining[articles_per_request:]
        response = get_titles_from_id(to_request)
        pages = list(response["query"]["pages"].values())
        for page in pages:
            if "missing" in page:
                append_file(f"{folder_data}/errors.csv", page["pageid"])
            else:
                append_file(f"{folder_data}/titles.csv", f'{page["pageid"]}, {page["title"]}')


def collect_revisions_info(title, params, folder_data, log):
    date_start, date_end = params.date_start, params.date_end
    response = get_revisions_info(title, date_start, date_end)
    revisions_info, is_complete, next_date = parse_revisions_info_monthly(response, date_start, date_end)

    while not is_complete and next_date is not None and next_date > date_end and "continue" in response:
        response = get_revisions_info(title, date_start, date_end, response["continue"]["rvcontinue"])
        new_revisions_info, is_complete, next_date = parse_revisions_info_monthly(response, next_date, date_end)
        revisions_info = revisions_info + new_revisions_info

    if next_date is not None and next_date > date_end:
        log(f"ERROR:{title} não coletado até o final\n")

    result = json_normalize(revisions_info)

    result.insert(0, 'title', title)
    result.insert(0, 'pageid', list(response["query"]["pages"])[0])

    result.to_csv(f"{folder_data}/{title}", index=None, header=True, quoting=csv.QUOTE_NONNUMERIC)


def collect_content(title, params, folder_data, log):
    data = pd.read_csv(f"{params.input_folder}/{title}")
    revision_timestamps = set(data['revision.timestamp'].values)

    for access_date in revision_timestamps:
        response = get_revision_content(title, access_date)
        content = parse_revision_content(response)
        write_file(f"{folder_data}/{title}|{access_date}", content)


def collect_category(title, params, folder_data, log):
    df = pd.read_csv(f"{params.input_folder}/{title}")

   # collected = pd.read_csv(f"{folder_data}/{title}")
    collected_timestamps = []
    for index, row in df.iterrows():
        date = row["revision.timestamp"]
        if date not in collected_timestamps:
            collected_timestamps.append(date)
            response = get_revision_content(f"Talk:{title}", date)
            try:
                content = parse_revision_content(response)
                raw, category = parse_revision_category_content(content)
                log(f"{date} {category} {raw}")
                df.at[index, "category"] = category
                df.at[index, "raw_category"] = str(raw)
            except Exception as e:
                log(f"ERRO: categoria de '{title}' {date} {category} {str(raw)}: {str(e)}")
    save_dataframe(df, f"{folder_data}/{title}")

def collect_page_links(title, folder_data):   
    response = get_page_links(title)
    links = parse_page_links(response)
    
    while "continue" in response:
        response = get_page_links(title, response["continue"]["plcontinue"])
        new_links = parse_page_links(response)
        links += new_links
    if( title == "Wikipedia:Good_articles/all"):
        title = "Wikipedia:Good_articles"
    save_dataframe(pd.DataFrame(links), f"{folder_data}/{title}")

if __name__ == "__main__":
    params = {"date_start": "2010-01-15T14:56:00Z", "date_end": "2011-01-15T14:56:00Z"}

    collect_revisions_info("Sherlock_Holmes",params,".",print)

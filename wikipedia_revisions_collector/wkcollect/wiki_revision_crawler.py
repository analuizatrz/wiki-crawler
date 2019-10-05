import pandas as pd
import time
from pandas.io.json import json_normalize
from datetime import datetime
from wkrequest import get_revisions_info, get_titles_from_id, get_revision_content
from wikiutils import date_range, date_range_monthly, match_dates_and_revisions
from wkio import create_folder_if_does_not_exist, create_file_if_does_not_exist, read_json, write_json, append_file, write_file
import csv
##
import os
##
file_log = "log.csv"


def log(str):
    print(str)
    append_file(file_log, str)


class Params(object):
    pass


class CheckTime(object):
    def __init__(self):
        self.time = datetime.now()
        self.total_time = 0
        self.delta_count = 0

    def finish_time(self):
        delta = datetime.now()-self.time
        self.time = datetime.now()
        return delta

    def log_delta(self, task):
        delta = self.finish_time()
        self.total_time += delta.total_seconds()
        self.delta_count += 1
        log(task+" done in "+str(delta.total_seconds())+" average: "+str(self.total_time/self.delta_count))

# TODO unit test this method

def parse_revisions_info_monthly(revisions_info_response, date_start, date_end):
    """Parses revisions info response returning a discretized list of revisions as if the article were accessed and collected monthly.

    Parameters:
        revisions_info_response (json): raw result of revisions info request

    Returns:
        response (json): revisions as if they were monthly accessed
        is_complete (bool): all dates have been comtemplated
        next_date: first date which was not contemplated
    """
    page = list(revisions_info_response["query"]["pages"].values())[0]
    revisions = page["revisions"]
    dates = date_range_monthly(date_end, date_start)

    return match_dates_and_revisions(dates, revisions)


def parse_revision_content(response):
    page = list(response["query"]["pages"])[0]
    revision = list(page["revisions"])[0]
   # return (page["pageid"], page["title"], revision["user"], revision["timestamp"], revision["comment"], revision["slots"]["main"]["content"])
    return revision["slots"]["main"]["content"]

def collect_titles(ids, folder_data, articles_per_request=50):
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
                append_file(f"{folder_data}/titles.csv",f'{page["pageid"]}, {page["title"]}')

def collect_revisions_info(title, params, folder_data):
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

def collect_content(title, params, folder_data):
    data = pd.read_csv(f"{params.input_folder}/{title}")
    revision_timestamps = set(data['revision.timestamp'].values)

    for access_date in revision_timestamps:
        response = get_revision_content(title, access_date)
        content = parse_revision_content(response)
        write_file(f"{folder_data}/{title}|{access_date}",content)

def collect_all(titles, collect_callback, collect_callback_params, output_folder):
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
    create_file_if_does_not_exist(file_log)

    already_collected_pages = set(status["collected_pages"])
    remaning_to_collect = [article for article in titles if article not in already_collected_pages]

    objTime = CheckTime()

    while(len(remaning_to_collect) > 0):
        title = remaning_to_collect.pop(0)
        objTime.log_delta(f"Remaining: {len(remaning_to_collect)+1} collecting now: '{title}'")

        try:
            collect_callback(title, collect_callback_params, folder_data)
            # TODO: refatorar isso
            #result.to_csv(f"{folder_data}/{title}", index=None, header=True, quoting=csv.QUOTE_NONNUMERIC)
            status["collected_pages"].append(title)
            write_json(file_collected, status)
        except:
            append_file(file_error, title)
            log(f"ERROR:{title}\n")
            time.sleep(2)
        time.sleep(1)
    log(f"Tempo total : {objTime.total_time}")

def run_collect_all_revision_info_2009_2007(base_folder):
    params = Params()
    params.date_start = "2009-01-03T00:00:00Z"
    params.date_end = "2007-01-03T00:00:00Z"

    output_folder = f"{base_folder}/data/revision_info_{params.date_end[0:4]}{params.date_end[5:7]}-{params.date_start[0:4]}{params.date_start[5:7]}"
    input_file = f"{base_folder}/wikipedia_dataset_hasan/wikipedia_reduced.csv"

    create_folder_if_does_not_exist(output_folder)

    dataset = pd.read_csv(input_file)
    titles = list(pd.DataFrame(dataset, columns=['page_title'])['page_title'].values)

    collect_all(titles, collect_revisions_info, params, output_folder)


def run_collect_all_revision_info_2009_2007_errors(base_folder):
    params = Params()
    params.date_start = "2009-01-03T00:00:00Z"
    params.date_end = "2007-01-03T00:00:00Z"

    output_folder = f"{base_folder}/data/revision_info_{params.date_end[0:4]}{params.date_end[5:7]}-{params.date_start[0:4]}{params.date_start[5:7]}-errors"
    input_file = f"{base_folder}/data/revision_info_200701-200901/errors.csv"
    create_folder_if_does_not_exist(output_folder)
    titles = open(input_file, "r").read().split('\n')[:-1]

    collect_all(titles, collect_revisions_info, params, output_folder)


def run_collect_all_content_2009_2007(base_folder):
    params = Params()
    params.date_start = "2009-01-03T00:00:00Z"
    params.date_end = "2007-01-03T00:00:00Z"

    output_folder = f"{base_folder}/data/content_{params.date_end[0:4]}{params.date_end[5:7]}-{params.date_start[0:4]}{params.date_start[5:7]}-errors"
    input_folder = f"{base_folder}/data/revision_info_200701-200901/data"
    create_folder_if_does_not_exist(output_folder)

    params.input_folder = input_folder
    titles = os.listdir(input_folder)

    collect_all(titles, collect_content, params, output_folder)

def collect_all_titles(base_folder):
    output_folder = f"{base_folder}/data/titles"
    input_file = f"{base_folder}/ids.csv"
    create_folder_if_does_not_exist(output_folder)

    ids = open(input_file, "r").read().split('\n')

    collect_titles(ids, output_folder)


def run_test(base_folder):
    title = "Dypsis onilahensis"
    params = Params()
    params.date_start = "2009-01-03T00:00:00Z"
    params.date_end = "2007-01-03T00:00:00Z"

    collect_revisions_info(title, params, f"{base_folder}/test/"), 

if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-web-crawler"
    # collect_all_titles(base_folder)
    run_collect_all_revision_info_2009_2007(base_folder)
    # run_collect_all_content_2009_2007(base_folder)

    #run_collect_all_revision_info_2009_2007_errors(base_folder)
    #run_test(base_folder)
    
    # error_file = "/home/ana/Documents/tcc-web-crawler/data/revision_info_2007-2009/errors.csv"
    # titles = open(error_file, "r").read().split('\n')[:-1]
    # print(len(titles))

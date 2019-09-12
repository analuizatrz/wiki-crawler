import pandas as pd
import json
import time
from pandas.io.json import json_normalize
from datetime import datetime
import requests
import os
import csv

file_log = "log.csv"


def log(str):
    print(str)
    append_file(file_log, str)


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


def date_range_monthly(date_start, date_end):
    return pd.date_range(date_start, date_end, freq='MS').strftime("%Y-%m-%dT%H:%M:%SZ").tolist()[::-1]


def match_dates_and_revisions(dates, revisions):
    """ For each date finds the max possible revision less or equal then the date.
        Assumes that dates and revisions are ordered descending

    Parameters:
        dates (str): dates
        revisions (object): which contain dates 

    Returns:
        result (list): list of tuples
        is_complete (bool): all dates have been comtemplated
        next_date: first date which was not contemplated
    """
    date_idx = 0
    revision_idx = 0
    result = []

    while date_idx < len(dates) and revision_idx < len(revisions):
        if(revisions[revision_idx]["timestamp"] <= dates[date_idx]):
            result.append(build_revision(dates[date_idx], revisions[revision_idx]))
            date_idx += 1
        else:
            revision_idx += 1

    is_complete = date_idx == len(dates)
    return result, is_complete, None if is_complete else dates[date_idx]


def build_revision(date, revision):
    result = {
        "access": date,
        "revision": revision
    }
    return result


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


S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"


def get_revisions_info(title, date_start, date_end, rvcontinue=None):
    """Resquest revisions info of a wikipedia article by its title, in a period determined by start and end dates

    Parameters:
        title (str): The title of the article
        date_start (str): The start date of querying in the format ISO 8601: 2001-01-15T14:56:00Z
        date_end (str): The end date of querying in the format ISO 8601: 2001-01-15T14:56:00Z

    Returns:
        response (json): raw result of the request
    """
    params = {
        "action": "query",
        "prop": "revisions",
        "format": "json",
        "titles": title,
        "rvlimit": 500,
        "rvprop": "ids|timestamp|user|comment",
        "rvstart": date_start,
        "rvend": date_end,
        "rvdir": "older",
    }
    if rvcontinue is not None:
        params["rvcontinue"] = rvcontinue

    response = S.get(url=URL, params=params)

    return response.json()


def read_json(file_name):
    with open(file_name, 'r') as fp:
        return json.load(fp)


def write_json(file_name, dict):
    with open(file_name, 'w') as fp:
        json.dump(dict, fp)


def append_file(file_name, line):
    with open(file_name, 'a') as fp:
        fp.write(f"{line}\n")


def create_file_if_does_not_exist(file_name):
    try:
        open(file_name, 'r')
    except IOError:
        open(file_name, 'w')


def create_folder_if_does_not_exist(folder):
    os.makedirs(folder, exist_ok=True)


def collect(title, date_start, date_end):
    response = get_revisions_info(title, date_start, date_end)
    revisions_info, is_complete, next_date = parse_revisions_info_monthly(response, date_start, date_end)

    while not is_complete and next_date is not None and next_date > date_end and "continue" in response:
        response = get_revisions_info(title, date_start, date_end, response["continue"]["rvcontinue"])
        new_revisions_info, is_complete, next_date = parse_revisions_info_monthly(response, next_date, date_end)
        revisions_info = revisions_info + new_revisions_info

    if next_date is not None and next_date > date_end:
        log(f"ERROR:{title} não coletado até o final\n")

    return json_normalize(revisions_info)


def collect_all(titles, date_start, date_end, folder_to_save):
    file_collected = f"{folder_to_save}/collected.json"
    file_error = f"{folder_to_save}/errors.csv"
    folder_data = f"{folder_to_save}/data"

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
            result = collect(title, date_start, date_end)
            result.to_csv(f"{folder_data}/{title}", index=None, header=True, quoting=csv.QUOTE_NONNUMERIC)
            status["collected_pages"].append(title)
            write_json(file_collected, status)
        except:
            append_file(file_error, title)
            log(f"ERROR:{title}\n")
            time.sleep(2)
        time.sleep(1)
    log(f"Tempo total : {objTime.total_time}")


def run_collect_all_revision_info():
    date_start = "2009-01-03T00:00:00Z"
    date_end = "2007-01-03T00:00:00Z"

    base_folder = "/home/ana/Documents/tcc-web-crawler"
    folder_to_save = f"{base_folder}/collected_data/revision_info_{date_end[0:4]}{date_end[5:7]}-{date_start[0:4]}{date_start[5:7]}"
    input_file = f"{base_folder}/poc_wikimedia_revision/wikipedia_dataset_hasan/wikipedia.csv"

    create_folder_if_does_not_exist(folder_to_save)

    dataset = pd.read_csv(input_file)
    titles = list(pd.DataFrame(dataset, columns=['page_title'])['page_title'].values)
    # error_file = "/home/ana/Documents/tcc-web-crawler/collected_data/revision_info_2007-2009/errors.csv"
    # titles = open(error_file, "r").read().split('\n')[:-1]

    collect_all(titles, date_start, date_end, folder_to_save)


def run_test():
    title = "Dypsis onilahensis"
    date_start = "2009-01-03T00:00:00Z"
    date_end = "2007-01-03T00:00:00Z"
    collect(title, date_start, date_end)


if __name__ == "__main__":
    run_collect_all_revision_info()
    # error_file = "/home/ana/Documents/tcc-web-crawler/collected_data/revision_info_2007-2009/errors.csv"
    # titles = open(error_file, "r").read().split('\n')[:-1]
    # print(len(titles))

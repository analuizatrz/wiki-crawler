from wkrequest import get_revisions_info, get_titles_from_id, get_revision_content, get_page_links
from wkio import create_folder_if_does_not_exist, create_file_if_does_not_exist, read_json, write_json, append_file, write_file, save_dataframe
from wkparse import parse_revision_content, parse_revisions_info_monthly, parse_revision_category_content, parse_page_links
from wkutils import Timer
import time
import csv

from pandas.io.json import json_normalize
import pandas as pd

def foreach_run_save_log(titles, run, run_params, output_folder, log=print):
    """
    Run function for each title and save results in the output folder. The output folder 
    will be populated with the files collected (in folder data), errors (file errors.csv) and
    log (collected.json). If the output_folder has data, the process will proceed ignoring
    already collected files. The collected files are considered from log (collected.json). If
    the process crash it will begin collecting from where it stopped before crashing.
    
    Parameters:
        titles(array of str): titles to be processed
        run(function): function to be executed foreach title, with the parameter run_params.
                        the function signature is run(title, run_params, folder_data, log)
        run_params(Params): parameters necessary to execute the function, for all titles
        output_folder(str): folder where will be saved the data, errors and logs
        log(function): output log, maybe console or file. By default print
    """
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

    while(len(remaning_to_collect) > 0):
        title = remaning_to_collect.pop(0)
        objTime.log_delta(f"Remaining: {len(remaning_to_collect)+1} collecting now: '{title}'")

        try:
            run(title, run_params, folder_data, log)
            status["collected_pages"].append(title)
            write_json(file_collected, status)
        except Exception as e:
            append_file(file_error, title)
            log(f"ERROR:{title} {str(e)}\n")
            #time.sleep(1)
        #time.sleep(1)
    log(f"Tempo total : {objTime.total_time}")


def collect_revisions_info(title, params, folder_data, log):
    """
    Colect metadata of a article and save in a csv named as the title (<title>.csv)
    
    Parameters:
        title(str): title of the article
        params: must contain params.date_start and params.date_end, which defines the period 
                of the revisions colected
        folder_data(str): folder where the file "<title>.csv will be saved
        log(function):  output log, maybe console or file. By default print
    """
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


def collect_content(title, params, folder_data, log=print):
    """
    Colect content of a article and save in a csv named as the title (<title>.csv). 
    Metadata collector must have be run before.
    
    Parameters:
        title(str): title of the article
        params: must contain params.input_folder, which defines from where to read the titles. Must be
                a folder from metadata collector "collect_revisions_info".
        folder_data(str): folder where the file "<title>.csv will be saved
        log(function):  output log, maybe console or file. By default print
    """
    data = pd.read_csv(f"{params.input_folder}/{title}")
    revision_timestamps = set(data['revision.timestamp'].values)

    for access_date in revision_timestamps:
        response = get_revision_content(title, access_date)
        content = parse_revision_content(response)
        write_file(f"{folder_data}/{title}_{access_date}", content)


def collect_category(title, params, folder_data, log=print):
    """
    Colect category of a article and save in a csv named as the title (<title>.csv).
    Metadata collector must have be run before.
    
    Parameters:
        title(str): title of the article
        params: must contain params.input_folder, which defines from where to read the titles. Must be
                a folder from metadata collector "collect_revisions_info".
        folder_data(str): folder where the file "<title>.csv will be saved
        log(function):  output log, maybe console or file. By default print
    """
    df = pd.read_csv(f"{params.input_folder}/{title}")

   # collected = pd.read_csv(f"{folder_data}/{title}")

    for index, row in df.iterrows():
        date = row["revision.timestamp"]
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

def collect_category_single_rev(articles_filename, timestamp_date, log=print):
    """
    Colect category of articles in file and save in a csv named (<articles_file>_<timestamp_date>_class.csv)
    
    Parameters:
        articles_file(str): article file (one article per line)
        timestamp_date: timestamp in the format ISO 8601: 2001-01-15T14:56:00Z
        log(function):  output log, maybe console or file. By default print
    """
    with open(articles_filename) as articles_file, open(f"{articles_filename.split('.')[0]}_quality.csv","w") as output:
        writer_quality = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        for article_title in articles_file:

            response = get_revision_content(f"Talk:{article_title}", timestamp_date)
            try:
                content = parse_revision_content(response)
                raw, category = parse_revision_category_content(content)
                log(f"{timestamp_date} {category} {raw}")
                writer_quality.writerow([article_title, category, raw])
            except Exception as e:
                log(f"ERRO: categoria de '{article_title}' {timestamp_date} {category} {str(raw)}: {str(e)}")


def collect_page_links(title, folder_data):
    """
    Colect and save titles referenced by a article especified by title
    
    Parameters:
        title(str): title of the article
        folder_data(str): folder where the file "<title>.csv will be saved
    """ 
    response = get_page_links(title)
    links = parse_page_links(response)

    while "continue" in response:
        response = get_page_links(title, response["continue"]["plcontinue"])
        new_links = parse_page_links(response)
        links += new_links
    save_dataframe(pd.DataFrame(links), f"{folder_data}/{title}")


def collect_titles(ids, folder_data, articles_per_request=50, log=print):
    """
    Colect and save titles given ids
    
    Parameters:
        ids (array of str): ids of pages
        folder_data (str): folder path where the data will be saved
        articles_per_request(number): Quantity of articles sent per request. Default 50.
        log(function):  output log, maybe console or file. Default print.
    """
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

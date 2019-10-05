import pandas as pd
from wkio import create_folder_if_does_not_exist, create_file_if_does_not_exist, read_json, write_json, append_file, write_file
from wkcollect import collect_all, collect_content, collect_revisions_info, collect_titles

##
import os
##

def create_logger(folder="."):
    filename = f"{folder}/log.csv"
    create_file_if_does_not_exist(filename)
    def function(str):
        print(str)
        append_file(filename, str)
    return function

class Params(object):
    pass

def run_collect_all_revision_info_2009_2007(base_folder):
    params = Params()
    params.date_start = "2009-01-03T00:00:00Z"
    params.date_end = "2007-01-03T00:00:00Z"

    output_folder = f"{base_folder}/data/revision_info_{params.date_end[0:4]}{params.date_end[5:7]}-{params.date_start[0:4]}{params.date_start[5:7]}"
    input_file = f"{base_folder}/wikipedia_dataset_hasan/wikipedia_reduced.csv"

    create_folder_if_does_not_exist(output_folder)

    dataset = pd.read_csv(input_file)
    titles = list(pd.DataFrame(dataset, columns=['page_title'])['page_title'].values)

    collect_all(titles, collect_revisions_info, params, output_folder, create_logger(output_folder))


def run_collect_all_revision_info_2009_2007_errors(base_folder):
    params = Params()
    params.date_start = "2009-01-03T00:00:00Z"
    params.date_end = "2007-01-03T00:00:00Z"

    output_folder = f"{base_folder}/data/revision_info_{params.date_end[0:4]}{params.date_end[5:7]}-{params.date_start[0:4]}{params.date_start[5:7]}-errors"
    input_file = f"{base_folder}/data/revision_info_200701-200901/errors.csv"
    create_folder_if_does_not_exist(output_folder)
    titles = open(input_file, "r").read().split('\n')[:-1]

    collect_all(titles, collect_revisions_info, params, output_folder, create_logger(output_folder))


def run_collect_all_content_2009_2007(base_folder):
    params = Params()
    params.date_start = "2009-01-03T00:00:00Z"
    params.date_end = "2007-01-03T00:00:00Z"

    output_folder = f"{base_folder}/data/content_{params.date_end[0:4]}{params.date_end[5:7]}-{params.date_start[0:4]}{params.date_start[5:7]}-errors"
    input_folder = f"{base_folder}/data/revision_info_200701-200901/data"
    create_folder_if_does_not_exist(output_folder)

    params.input_folder = input_folder
    titles = os.listdir(input_folder)

    collect_all(titles, collect_content, params, output_folder, create_logger(output_folder))

def collect_all_titles(base_folder):
    output_folder = f"{base_folder}/data/titles"
    input_file = f"{base_folder}/ids.csv"
    create_folder_if_does_not_exist(output_folder)

    ids = open(input_file, "r").read().split('\n')
    collect_titles(ids, output_folder, create_logger(output_folder))

if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-web-crawler"
    # collect_all_titles(base_folder)
    run_collect_all_revision_info_2009_2007(base_folder)
    run_collect_all_content_2009_2007(base_folder)

    #run_collect_all_revision_info_2009_2007_errors(base_folder)
    
    # error_file = "/home/ana/Documents/tcc-web-crawler/data/revision_info_2007-2009/errors.csv"
    # titles = open(error_file, "r").read().split('\n')[:-1]
    # print(len(titles))

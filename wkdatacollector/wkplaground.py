import pandas as pd
from wkio import create_folder_if_does_not_exist
from wkcollect import collect_all, collect_content, collect_revisions_info, collect_titles, collect_category, collect_page_links
from wkutils import create_logger, Params
import os

def run_collect_all_revision_info(input_file, output_folder, params):
    create_folder_if_does_not_exist(output_folder)
    titles = list(pd.read_csv(input_file)["page_title"])
    collect_all(titles, collect_revisions_info, params, output_folder, create_logger(output_folder))

def run_collect_all_revision_info_errors(input_file, output_folder, params):
    create_folder_if_does_not_exist(output_folder)
    titles = open(input_file, "r").read().split('\n')[:-1]
    collect_all(titles, collect_revisions_info, params, output_folder, create_logger(output_folder))

def run_collect_all_content(input_folder, output_folder, params):
    create_folder_if_does_not_exist(output_folder)
    params.input_folder = input_folder
    titles = os.listdir(input_folder)
    collect_all(titles, collect_content, params, output_folder, create_logger(output_folder))

def run_collect_all_categories(input_folder, output_folder, params):
    create_folder_if_does_not_exist(output_folder)
    params.input_folder = input_folder
    titles = os.listdir(input_folder)
    collect_all(titles, collect_category, params, output_folder, create_logger(output_folder))

def collect_titles_by_id(input_file, output_folder):
    create_folder_if_does_not_exist(output_folder)
    ids = open(input_file, "r").read().split('\n')
    collect_titles(ids, output_folder, create_logger(output_folder))

def collect_titles_feature_articles(output_folder):
    create_folder_if_does_not_exist(output_folder)
    title = "Wikipedia:Featured_articles"
    #title = "Wikipedia:Good_articles/all"
    collect_page_links(title, output_folder)

if __name__ == "__main__":
    date_start = "2009-01-03T00:00:00Z"
    date_end = "2007-01-03T00:00:00Z"
    base_folder = "/home/ana/Documents/tcc-collected-data/data"

    params = Params()
    params.date_start = date_start
    params.date_end = date_end
    date_range = f"{date_end[0:4]}{date_end[5:7]}-{date_start[0:4]}{date_start[5:7]}"
   
    collect_titles_feature_articles(f"{base_folder}/artigos-FA")
    # output_folder = f"{base_folder}/titles"
    # input_file = f"{base_folder}/ids.csv"
    # collect_titles_by_id(base_folder)

    #############collect revision_info
    ### -
    # input_file_info = f"{base_folder}/../wikipedia_dataset_hasan/wikipedia_reduced-.csv"
    # output_folder_info = f"{base_folder}/revision_info_byid_{date_range}"
    #
    ### revision_info_by_id
    # input_file_info = "~/Documents/data/titles/titles.csv"
    # output_folder_info = f"{base_folder}/revision_info_{date_range}"
    #
    ### errors
    # input_file_info = f"{base_folder}/revision_info_{date_range}/errors.csv"
    output_folder_info = f"{base_folder}/revision_info_{date_range}-errors"
    #
    # run_collect_all_revision_info(input_file_info, output_folder_info, params)


    ############collect_content
    output_folder_content = f"{base_folder}/content_{date_range}-errors"
    run_collect_all_content(f"{output_folder_info}/data", output_folder_content, params)

    ###########collect_category
    # output_folder_category = f"{base_folder}/info_and_category_{date_range}"
    # run_collect_all_categories(f"{output_folder_info}/data", output_folder_category, params)

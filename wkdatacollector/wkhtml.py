# wkhrmlConverterEntryPoint running required
from py4j.java_gateway import JavaGateway
import os
from wkcollect import foreach_run_save_log
from wkio import write_file, create_folder_if_does_not_exist, create_file_if_does_not_exist, append_file
from wkutils import create_logger, Params
from wkglobals import base_folder
import pandas as pd


gateway = JavaGateway()

converter = gateway.entry_point.getConverter()
gateway.jvm.java.lang.System.out.println('Conectado !')

def convert_content(title, params, folder_data, log):
    """
    Convert Wkhtml into html of an article which content was previously collected

    Parameters:
        title(str): title of the article
        params(Params): Must have params.input_folder(str) which is the folder of the content data collect
        folder_data(str): folder where features will be saved
        log(function): output log, may be console or file. By default print
    """
    input = open(f"{params.input_folder}/{title}").read()
    html = converter.convert(input)
    write_file(f"{folder_data}/{title}.html", html)

def convert_all(input_folder, output_folder, params):
    """
    Convert all files of a folder from Wkhtml into html

    Parameters:
        input_folder(str): folder where content collected was saved
        params(Params): Must have params.input_folder(str) which is the folder
        folder_data(str): folder where features will be saved
        log(function): output log, may be console or file. By default print
    """
    create_folder_if_does_not_exist(output_folder)
    params.input_folder = input_folder
    titles = os.listdir(input_folder)
    foreach_run_save_log(titles, convert_content, params, output_folder, create_logger(output_folder))

if __name__ == "__main__":
    output_folder = f"{base_folder}/content_200701_200901_html"
    input_folder = f"{base_folder}/content_200701-200901-errors/data"
    titles = os.listdir(input_folder)
    convert_all(input_folder, output_folder, Params())
    #input = open(f"{input_folder}/{titles[0]}", "r").read()



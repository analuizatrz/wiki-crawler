from py4j.java_gateway import JavaGateway
import os
from wkcollect import collect_all
from wkio import write_file, create_folder_if_does_not_exist, create_file_if_does_not_exist, append_file


def create_logger(folder="."):
    filename = f"{folder}/log.csv"
    create_file_if_does_not_exist(filename)
    def function(str):
        print(str)
        append_file(filename, str)
    return function

import pandas as pd

class Params(object):
    pass

gateway = JavaGateway()

converter = gateway.entry_point.getConverter()
gateway.jvm.java.lang.System.out.println('Conectado !')

def convert_content(title, params, folder_data, log):
    input = open(f"{params.input_folder}/{title}").read()
    html = converter.convert(input)
    write_file(f"{folder_data}/{title}.html", html)

def convert_all(input_folder, output_folder, params):
    create_folder_if_does_not_exist(output_folder)
    params.input_folder = input_folder
    titles = os.listdir(input_folder)
    collect_all(titles, convert_content, params, output_folder, create_logger(output_folder))

if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-collected-data/data"
    output_folder = f"{base_folder}/content_200701_200901_html"
    input_folder = f"{base_folder}/content_200701-200901-errors/data"
    titles = os.listdir(input_folder)
    convert_all(input_folder, output_folder, Params())
    #input = open(f"{input_folder}/{titles[0]}", "r").read()



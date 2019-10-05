import json
import os


def create_folder_if_does_not_exist(folder):
    os.makedirs(folder, exist_ok=True)


def create_file_if_does_not_exist(file_name):
    try:
        open(file_name, 'r')
    except IOError:
        open(file_name, 'w')


def read_json(file_name):
    with open(file_name, 'r') as fp:
        return json.load(fp)


def write_json(file_name, dict):
    with open(file_name, 'w') as fp:
        json.dump(dict, fp)


def append_file(file_name, line):
    with open(file_name, 'a') as fp:
        fp.write(f"{line}\n")


def write_file(file_name, content):
    with open(file_name, 'w') as fp:
        fp.write(content)


def append_file(file_name, line):
    with open(file_name, 'a') as fp:
        fp.write(f"{line}\n")

def create_file_if_does_not_exist(file_name):
    try:
        open(file_name, 'r')
    except IOError:
        open(file_name, 'w')

def create_logger(folder="."):
    """ Creates a logger that prints on the terminal and writes on a log file

    Parameters:
        folder (str): folder to save log file
    Returns:
        logger (function): the function which logs
    """
    filename = f"{folder}/erros.csv"
    create_file_if_does_not_exist(filename)
    def function(str):
        print(str)
        append_file(filename, str)
    return function
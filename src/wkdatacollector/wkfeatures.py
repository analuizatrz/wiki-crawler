import sys

# Hasan's project wiki-quality required
sys.path.insert(1, "/home/ana/Documents/wiki-quality/wiki-quality")

from wkutils import create_logger, Params
from wkcollect import foreach_run_save_log
from wkio import append_file, create_file_if_does_not_exist, create_folder_if_does_not_exist
from utils.basic_entities import LanguageEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum
from feature.feature_factory.feature_factory import FeatureFactory
from feature.featureImpl.style_features import WordCountFeature, CharacterCountFeature
from feature.features import FeatureVisibilityEnum, FeatureCalculator, Document
import os


output_file = "raw_dataset.csv"


def compute_features(arr_features, format=FormatEnum.HTML):
    """
    Generate function to compute features given title and content

    Parameters:
        arr_features(array of Features): features which will be computed.
        format: format of content. Default FormatEnum.HTML.
    
    Returns:
        feature_computer(function(str,str)): function which computes features given title(str) and content(str)
    """
    def F(title, content):
         """
        Compute features given title and content

        Parameters:
            title(str): title of article
            content(str): content from which features will be generated
        """
        document = Document(1, title, content)
        return FeatureCalculator.featureManager.computeFeatureSet(document, arr_features, format)
    return F


def split_title(filename, log):
    """
    Split filename with separator '_', into title and date

    Parameters:
        filename(str): name which will be splitted
        log(function): output log, may be console or file. By default print

    Returns:
        title
        date
    """
    info = filename.split("_")

    if len(info) == 2:
        return f'"{info[0]}";"{info[1][:-5]}"'
    else:
        log(f"Erro no nome do arquivo{filename}")
        return f"{filename};"

def create_features(title, params, folder_data, log):
    """
    Create and save features for title

    Parameters:
        title(str): title of the article
        params(Params): Must have params.input_folder(str) and params.compute_features(function)
        folder_data(str): folder where features will be saved
        log(function): output log, may be console or file. By default print
    """
    content = open(f"{params.input_folder}/{title}", "r").read()
    arr_resultado = params.compute_features(title, content)
    append_row(f"{folder_data}/{output_file}", title, arr_resultado, log)

def create_features_all(input_folder, output_folder):
    """
    Create and save features for all files of input_folder

    Parameters:
        input_folder(str): folder where the metadata is
        output_folder(str): folder where features will be saved
    """
    arr_features = load_all_features()
    write_header(f"{output_folder}/data/{output_file}", arr_features)

    titles = os.listdir(input_folder)

    params = Params()
    params.input_folder = input_folder
    params.compute_features = compute_features(arr_features, format=FormatEnum.HTML)

    foreach_run_save_log(titles, create_features, params, output_folder, create_logger(output_folder))


def load_all_features(language=LanguageEnum.en):
    """
    Load all features. Necessary Hasan's project wiki-quality

    Parameters:
        language(LanguageEnum): language of the content from which features will be extrated. Default LanguageEnum.en.

    Returns:
        features(array of Features): features.
    """
    arr_features = []

    for sub_class in FeatureFactory.__subclasses__():
        feature_factory = None

        if(sub_class.IS_LANGUAGE_DEPENDENT):
            feature_factory = sub_class(language)
        else:
            feature_factory = sub_class()

        # caso a feature não esteja em desenvolvimento, anexar (podem ter features que ainda não fizemos os testes)
        if(not sub_class.DEVELOPMENT):
            arr_features.extend(feature_factory.createFeatures())

    return arr_features

def write_header(file, arr_features):
    """
    Append on file header based on features

    Parameters:
        file(str)
        arr_features(array of Features)
    """
    arr_features_name = '"title";"timestamp";' + ";".join([f'"{f.name}"' for f in arr_features])
    append_file(file, arr_features_name)

def append_row(file, title, arr_resultado, log):
    """
    Append on file title and results

    Parameters:
        file(str)
        title(str)
        arr_resultado(array of Features values)
        log()

    """
    arr_resultado_values = split_title(title, log) + ";" + ";".join([str(r) for r in arr_resultado])
    append_file(file, arr_resultado_values)


if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-collected-data/data"
    input_folder = f"{base_folder}/content_200701_200901_html/data"
    output_folder = f"{base_folder}/features"
   
    create_folder_if_does_not_exist(output_folder)
    create_folder_if_does_not_exist(f"{output_folder}/data")
    create_file_if_does_not_exist(f"{output_folder}/data/{output_file}")

    create_features_all(input_folder, output_folder)

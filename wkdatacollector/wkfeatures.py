import sys
sys.path.insert(1, "/home/ana/Documents/wiki-quality/wiki-quality")

from wkutils import create_logger, Params
from wkcollect import collect_all
from wkio import append_file, create_file_if_does_not_exist, create_folder_if_does_not_exist
from utils.basic_entities import LanguageEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum
from feature.feature_factory.feature_factory import FeatureFactory
from feature.featureImpl.style_features import WordCountFeature, CharacterCountFeature
from feature.features import FeatureVisibilityEnum, FeatureCalculator, Document
import os


output_file = "raw_dataset.csv"


def compute_features(arr_features, format=FormatEnum.HTML):
    def F(title, content):
        document = Document(1, title, content)
        return FeatureCalculator.featureManager.computeFeatureSet(document, arr_features, format)
    return F


def split_title(title, log):
    info = title.split("|")

    if len(info) == 2:
        return f'"{info[0]}";"{info[1][:-5]}"'
    else:
        log(f"Erro no nome do arquivo{title}")
        return f"{title};"

def create_features(title, params, folder_data, log):
    content = open(f"{params.input_folder}/{title}", "r").read()
    arr_resultado = params.compute_features(title, content)
    append_row(f"{folder_data}/{output_file}", title, arr_resultado, log)

def create_features_all(input_folder, output_folder, params):
    arr_features = load_all_features()
    write_header(f"{output_folder}/data/{output_file}", arr_features)

    titles = os.listdir(input_folder)
    
    params.input_folder = input_folder
    params.compute_features = compute_features(arr_features, format=FormatEnum.HTML)

    collect_all(titles, create_features, params, output_folder, create_logger(output_folder))


def load_all_features(language=LanguageEnum.en):
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
    arr_features_name = '"title";"timestamp";' + ";".join([f'"{f.name}"' for f in arr_features])
    append_file(file, arr_features_name)

def append_row(file, title, arr_resultado, log):
    arr_resultado_values = split_title(title, log) + ";" + ";".join([str(r) for r in arr_resultado])
    append_file(file, arr_resultado_values)


if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-collected-data/data"
    input_folder = f"{base_folder}/content_200701_200901_html/data"
    output_folder = f"{base_folder}/features"
   
    create_folder_if_does_not_exist(output_folder)
    create_folder_if_does_not_exist(f"{output_folder}/data")
    create_file_if_does_not_exist(f"{output_folder}/data/{output_file}")

    params = Params()
    create_features_all(input_folder, output_folder, params)

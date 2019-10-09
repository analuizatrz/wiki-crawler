import sys,os
print(sys.path)
sys.path.insert(1, "/home/ana/Documents/wiki-quality/wiki-quality")


from feature.features import FeatureVisibilityEnum, FeatureCalculator, Document
from feature.featureImpl.style_features import WordCountFeature, CharacterCountFeature
from feature.feature_factory.feature_factory import FeatureFactory
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum
from utils.basic_entities import LanguageEnum
from wkio import append_file, create_file_if_does_not_exist, create_folder_if_does_not_exist
from wkcollect import collect_all
from wkplaground import create_logger, Params

output_file = "raw_dataset.csv"
def compute_features(arr_features, format=FormatEnum.HTML):
    def F(content):
        return FeatureCalculator.featureManager.computeFeatureSet(content, arr_features, format)
    return F

def create_features(title, params, folder_data, log):
    content = open(f"{params.input_folder}/{title}", "r").read()
    document = Document(1,title,content)
    arr_resultado = params.compute_features(document)
    info = title.split("|")
    columns = ""
    if len(info) == 2:
        columns = f'"{info[0]}";"{info[1][:-5]}"'
    else:
        columns = f"{title};"
        log(f"Erro no nome do arquivo{title}")
    arr_resultado_values = columns +";" + ";".join([str(r) for r in arr_resultado])
    append_file(f"{folder_data}/{output_file}", arr_resultado_values)


def create_features_all(input_folder, output_folder, arr_features):
    params = Params()
    create_folder_if_does_not_exist(output_folder)
    params.input_folder = input_folder
    params.compute_features = compute_features(arr_features, format=FormatEnum.HTML)
    titles = os.listdir(input_folder)
    collect_all(titles, create_features, params, output_folder, create_logger(output_folder))

def load_all_features(language = LanguageEnum.en):
    arr_features = []
    
    for sub_class in FeatureFactory.__subclasses__():
        feature_factory = None

        if(sub_class.IS_LANGUAGE_DEPENDENT):
            feature_factory = sub_class(language)
        else:
            feature_factory = sub_class()

        #caso a feature não esteja em desenvolvimento, anexar (podem ter features que ainda não fizemos os testes)
        if(not sub_class.DEVELOPMENT):
            arr_features.extend(feature_factory.createFeatures())

    return arr_features

def texts_iterator():
    #collection = "content_200701_200901_html"
    base_folder = f"/home/ana/Downloads"
    #input_folder = [f"{base_folder}/Zygiella x-notata|2007-04-26T21:09:26Z", f"{base_folder}/Zygiella x-notata|2007-04-26T21:09:26Z"]
    input_folder = [f"{base_folder}/Two Worlds (video game)_2008-03-29T06_26_10Z", f"{base_folder}/Toyota Aurion (XV40)_2007-12-29T10_35_56Z"]
    for file in input_folder:
        content = open(file, "r").read()
        yield Document(1,file,content)

def poc():
    arr_features = load_all_features()
    print(arr_features_name)
    arr_features_name = '"title";' + ";".join([f'"{f.name}""' for f in arr_features])
    for text in texts_iterator():
        arr_resultado = FeatureCalculator.featureManager.computeFeatureSet(text, arr_features, FormatEnum.HTML)
        arr_resultado_values = text.str_doc_name +";" + ";".join([str(r) for r in arr_resultado])
        print(arr_resultado_values)
        print()


if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-collected-data/data"
    input_folder = f"{base_folder}/content_200701_200901_html/data"
    output_folder = f"{base_folder}/features"
    create_folder_if_does_not_exist(output_folder)

    arr_features = load_all_features()
    arr_features_name = '"title";"timestamp";' + ";".join([f'"{f.name}"' for f in arr_features])
    create_folder_if_does_not_exist(f"{output_folder}/data")
    create_file_if_does_not_exist(f"{output_folder}/data/{output_file}")
    append_file(f"{output_folder}/data/{output_file}", arr_features_name)

    create_features_all(input_folder, output_folder, arr_features)

    

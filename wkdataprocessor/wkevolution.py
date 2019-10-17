import sys
sys.path.insert(1, "/home/ana/Documents/tcc-web-crawler/wkdatacollector")

from wkio import save_dataframe
import pandas as pd
import csv
import os


# def generate_evolution_dataset(df, feature_columns):


if __name__ == "__main__":
    base_folder = "/home/ana/Documents/tcc-web-crawler/data"
    output_folder = "/home/ana/Documents/tcc-web-crawler/data"

    filename = f"{base_folder}/5-join_multiple_class_without_C-reduced.csv"
    # revision_dataset_single = pd.read_csv(f"{base_folder}/data/5-join_multiple_class_without_C.csv")
    # revision_dataset_multiple = pd.read_csv(f"{base_folder}/data/5-join-single-class-without-C.csv")

    revision_dataset = pd.read_csv(filename)

    info_columns = ['Unnamed: 0', 'title', 'timestamp', 'access', 'category', 'pageid', 'raw_category', 'revision.anon',
                    'revision.comment', 'revision.commenthidden', 'revision.parentid', 'revision.revid', 'revision.user']
    
    # revision_dataset_multiple.columns #['title', 'timestamp', 'access', 'category', 'pageid', 'raw_category', 'revision.anon', 'revision.comment', 'revision.commenthidden', 'revision.parentid', 'revision.revid', 'revision.user', 'Section count', 'Subsection count', 'Complete URL link count', 'Complete URL link count per section', 'Complete URL link count per length', 'Relative URL link count', 'Relative URL link count per section', 'Relative URL link count per length', 'Same page link count', 'Same page link count per section', 'Same page link count per length', 'Mean section size', 'Mean subsection size', 'Largest section size', 'Shortest section size', 'Standard deviation of the section size', 'Images count', 'Images per length', 'Images per section', 'Images per subsection', 'Phrase count', 'Large phrase count', 'Paragraph count', 'Large paragraph count', 'Largest phrase size', 'Large phrase rate', 'Short phrase rate', 'Char Count', 'Word Count', 'Articles count', 'Auxiliary verbs count', 'Coordination conjunctions count', 'Correlative conjunctions count', 'Indefinite pronouns count', 'Interrogative pronouns count', 'Prepositions count', 'Pronouns count', 'Relative pronoums count', 'Subordinating conjunctions count', 'To be verbs count', 'Sentences starting with articles', 'Sentences starting with auxiliary verbs', 'Sentences starting with coordination conjunctions', 'Sentences starting with correlative conjunctions', 'Sentences starting with indefinite pronouns', 'Sentences starting with interrogative pronouns', 'Sentences starting with prepositions', 'Sentences starting with pronouns', 'Sentences starting with relative pronoums', 'Sentences starting with subordinating conjunctions', 'Sentences starting with to be verbs', 'ARI readability feature', 'Coleman-Liau readability feature', 'Flesch Reading Ease Readability Feature', 'Flesch Kincaid Readability Feature', 'Gunning Fog Index readability feature', 'Lasbarhetsindex readability feature', 'SMOG Grading readability feature']
    
    feature_columns = [
                       'Section count', 'Subsection count', 'Complete URL link count', 'Complete URL link count per section',
                       'Complete URL link count per length', 'Relative URL link count', 'Relative URL link count per section',
                       'Relative URL link count per length', 'Same page link count', 'Same page link count per section',
                       'Same page link count per length', 'Mean section size', 'Mean subsection size', 'Largest section size',
                       'Shortest section size', 'Standard deviation of the section size', 'Images count', 'Images per length', 'Images per section',
                       'Images per subsection', 'Phrase count', 'Large phrase count', 'Paragraph count', 'Large paragraph count',
                       'Largest phrase size', 'Large phrase rate', 'Short phrase rate', 'Char Count', 'Word Count', 'Articles count',
                       'Auxiliary verbs count', 'Coordination conjunctions count', 'Correlative conjunctions count', 'Indefinite pronouns count',
                       'Interrogative pronouns count', 'Prepositions count', 'Pronouns count', 'Relative pronoums count',
                       'Subordinating conjunctions count', 'To be verbs count', 'Sentences starting with articles',
                       'Sentences starting with auxiliary verbs', 'Sentences starting with coordination conjunctions',
                       'Sentences starting with correlative conjunctions', 'Sentences starting with indefinite pronouns',
                       'Sentences starting with interrogative pronouns', 'Sentences starting with prepositions', 'Sentences starting with pronouns',
                       'Sentences starting with relative pronoums', 'Sentences starting with subordinating conjunctions',
                       'Sentences starting with to be verbs', 'ARI readability feature', 'Coleman-Liau readability feature',
                       'Flesch Reading Ease Readability Feature', 'Flesch Kincaid Readability Feature', 'Gunning Fog Index readability feature',
                       'Lasbarhetsindex readability feature', 'SMOG Grading readability feature'
                    ]
    #[f for f in revision_dataset.columns if f not in info_columns]
    #list(set(revision_dataset.columns) - set(info_columns))

    print(feature_columns)
    # merged = pd.merge(category, features, how='inner').sort_values(by=['title', 'timestamp'], ascending=[True, False])

    # df_first_columns(merged, ['title', 'timestamp']).to_csv(f"{output_folder}/join_features.csv", index=None, header=True, quoting=csv.QUOTE_NONNUMERIC)

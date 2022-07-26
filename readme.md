# Wikipedia Collector

This project aims to colect wikipedia pages and their quality category and process them to create datasets. From Wikipedia pages quality features and classification are extracted, and this data can be used for creating automatic assessment of Wikipedia Articles by applying Machine Learning models.

## Executing the algorithm

### 1. Metadata crawling

Input: Wikipedia article titles, date range
Ouput: Article's metadata represented by title, date and revision comment. This information is saved in a specific folder provided through configuration.

### 2. Content crawling (article)

Input: Metadata crawling output folder
Output: A set of files each containing the article's content in wkhtml format. This information is saved in a specific folder provided through configuration.

### 3. Talk page crawling

Input: Metadata crawling output folder
Output: A set of files each containing the article's talk page content in wkhtml format. From each page the article's quality class is extracted and saved in a structured CSV file.

### 4. Wkhtml to Html conversion

Input: Content crawling output folder
Output: A set of files each containing the article's content in html format. 

It's necessary to run the project wkhtmlConverterEntryPoint and a python script.

### 5. Feature engineering

Input: Wkhtml to Html conversion output folder
Output: A set of CSV files each containing the article's set of features for each revision. This algorithm depends on https://github.com/daniel-hasan/webfeatures to extract the features.

## Project Organization

This folder is organized in the following folders
```
.
├── analysis
│   ├── (...)
├── old
│   ├── (...)
├── Playground.ipynb
├── readme.md
├── Results crawler.ipynb
├── wiki_api_poc.ipynb
├── WikiHtmlConverter
├── wikipedia_dataset_hasan
│   ├── (...)
├── wkdatacollector
│   ├── wkcollect.py
│   ├── wkfeatures.py
│   ├── wkhtml.py
│   ├── wkio.py
│   ├── wkparse.py
│   ├── wkparse_test.py
│   ├── wkplaground.py
│   ├── wkrequest.py
│   ├── wkutils.py
│   └── wkutils_test.py
├── wkdataprocessor
└── wkhtmlConverterEntryPoint
    ├── bin
    │   └── core
    │       ├── Converter.class
    │       ├── EntryPoint.class
    │       └── Render.class
    ├── externalLibs
    │   ├── bliki-core-3.0.19.jar
    │   └── py4j-0.8.1.jar
    └── src
        └── core
            ├── Converter.java
            ├── EntryPoint.java
            └── Render.java
```


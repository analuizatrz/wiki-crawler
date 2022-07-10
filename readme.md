# Wikipedia Collector

Este projeto visa a coleta de páginas da wikipédia e sua classe/categoria de qualidade. Além disso, com a utilização do Projeto do Hasan pode-se extrair as classes de qualidade dos artigos e aplicar métodos de classificação automáticos.

## Estrutura

Estrutura do projeto. Algumas pastas foram omitidas (...) para uma melhor visualização.
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

## Tecnologias utilizadas

python 3.7.4, miniconda, vscode entre outros ...

### Miniconda

O [Miniconda](https://docs.conda.io/en/latest/miniconda.html) é um versão compactada do Anaconda. Ambos são plataformas para datascience e possuem gerenciador de pacotes e ambientes virtuais. O Miniconda foi escolhido por vir mais enxuto, sendo os pacotes necessários instalados manualmente.


#### Utilizando ambiente virtual 

```
conda activate base
conda activate <env>
conda deactivate
conda install <name>
```

#### Alguns dos pacotes utilizados

```bash
conda install jupyter
conda install pandas
conda install matplotlib
conda install scipy
conda install sklearn
```

### tools

 - refactoring with rope
 - unit testing with unittest
 - formatting with autopep8
 - linting with pylint

### Rodando testes

Para rodar os testes que estão sendo executados na POC basta seguir o comando abaixo
python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions

## Executando uma coleta

### 1. Coleta de metadados
Entrada: titulos dos artigos

salva revisões relativas a um artigo.
título, data, comentário
wkplaground

### 2. Coleta de conteúdo (artigo)
Entrada: pasta de metadados(1)

para cada metadado é coletada o conteúdo do artigo em formato próprio da wikipédia (wkhtml)
wkplaground

### 3. Coleta de página de discussão (talk page)
Entrada: pasta de metadados(1)

para cada metadado é coletada o conteúdo da página de discussão. Neste processo ocorre também a extração da classe de qualidade
wkplaground

You can obtain the class by using two different methods, for different porpouses: 

- for each article, the quality category for a given timestamp

```python
import sys
sys.path.append("src/wkdatacollector")
from wkcollect import collect_category_single_rev
file_articles = "data/articles_quality_categories/single_rev_mini.txt"
timestamp = "2022-07-01T00:00:00Z"
collect_category_single_rev(file_articles, timestamp)

```

The input and output of this example can be seen at [`data/articles_quality_categories/single_rev_mini.txt`](data/articles_quality_categories/single_rev_mini.txt) and [`data/articles_quality_categories/single_rev_mini_quality.csv`](data/articles_quality_categories/single_rev_mini_quality.csv), respectively. The input need to have one article per line and the output presents, for each article, 
its title, quality category and the string used to extract the quality category. 

- The class categrory in each revision timestamp in the article reviews metadata

### 4. Conversão de conteúdo em html
Entrada: pasta de conte údo de artigos(4)

cada conteúdo é convertido de wkhtml para html.
É necessário rodar o projeto wkhtmlConverterEntryPoint, em java.

### 5. Extração de features
Entrada: pasta de conteúdo em html(5)

de cada conteúdo html são extraídas as features.
É necessário ter o projeto wiki-quality do Hasan


# Trabalho de Conclusão de Curso II
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

## TODO

- [x] fazer uma poc da api da wikipedia
- [x] coletar páginas usando api da wikipedia
- [x] fazer poc do redirect
- [x] coletar redirects das páginas com erro
- [x] implementar redirect
- [x] coletar os arquivos com erro no redirect
- [x] incorporar o redirect na coleta automaticamente
- [x] coletar os conteúdos
- [x] transformação dos conteúdos em html
- [x] estudar a extração de features
- [x] criar o extrator de features 
- [x] extrair features
- [x] fazer uma poc do modelo
- [ ] estruturar informações
- [ ] treinar o modelo 1
- [ ] fazer análise dos resultados 1
- [ ] treinar o modelo 2
- [ ] fazer análise dos resultados 2
- [ ] Refatorar
    - [x] separar código em arquivos
    - [ ] gerar documentação pendente
    - [ ] isolar wkfeatures e wkhtml para wkdataprocessor
    - [ ] isolar a logica da função "collect_all" para um "foreach_execute"
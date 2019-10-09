# Trabalho de Conclusão de Curso II

## Tecnologias utilizadas

jupyter notebooks
python

## Instalação

Será utilizado o Python 3.6.8. Em ambiente linux:
sudo apt install python3 python3-pip jupyter

### Ambiente Virtual

sudo pip3 install virtualenv
python3 -m virtualenv tcc2
source tcc2/bin/activate

### Utilizando o conda

conda activate base
conda activate tcc
conda install <name>

### tools

refactoring with rope
unit testing with unittest
formatting with autopep8
linting with pylint

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
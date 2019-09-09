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

### Rodando testes
Para rodar os testes que estão sendo executados na POC basta seguir o comando abaixo
python -m wiki_revision_crawler_test TestWikiParser.test_match_dates_revisions
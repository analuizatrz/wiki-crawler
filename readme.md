# Crawler de classes da wikipedia

## Como rodar
Para rodar a versão original:

```
python3.6 original/get_wiki_pages.py example/politicos_usa_a.csv
```

Sendo o arquivo `politicos_usa_a.csv` um exemplo de arquivo de entrada, que contém apenas uma coluna, ou seja, lista das páginas.

para um arquivo `politicos_usa_a.txt` são gerados os seguintes arquivos de saída:
1. `politicos_usa_a.txt_error.log` : contém os erros
2. `politicos_usa_a.txt_crawl_status.json` : contém as páginas coletadas até o momento
3. `politicos_usa_a_classes.csv` : contém a saída resultado, que no caso são as páginas e suas classes.

Para rodar a versão nova, desenvolvida para ser modular:

```
python3.6 src/wiki_crawler.py example/politicos_usa_a.csv
```

## Refatorando o código

Primeiro está sendo refatorado os nomes de variáveis para o padrão do python, minusculo_separado_por_underscore. Os nomes de classes são no padrão CamelCase. Outros detalhes podem ser verificados nessas duas fontes:

https://www.python.org/dev/peps/pep-0008/

https://google.github.io/styleguide/pyguide.html


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
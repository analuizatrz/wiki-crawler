# Crawler de classes da wikipedia

## Como rodar

```
python3 get_wiki_pages.py politicos_usa_a.csv
```

Sendo o arquivo `politicos_usa_a.csv` um exemplo de arquivo de entrada, que contém apenas uma coluna, ou seja, lista das páginas.

para um arquivo `politicos_usa_a.txt` são gerados os seguintes arquivos de saída:
1. `politicos_usa_a.txt_error.log` : contém os erros
2. `politicos_usa_a.txt_crawl_status.json` : contém as páginas coletadas até o momento
3. `politicos_usa_a_classes.csv` : contém a saída resultado, que no caso são as páginas e suas classes.

## Refatorando o código

Primeiro está sendo refatorado os nomes de variáveis para o padrão do python, minusculo_separado_por_underscore.
Os nomes de classes são no padrão CamelCase.

https://www.python.org/dev/peps/pep-0008/